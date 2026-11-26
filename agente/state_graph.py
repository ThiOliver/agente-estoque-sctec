"""Grafo separado: interpretar → consultar (se necessário) → responder → fim."""
import os
import re
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from .contratos import Decisao, Entrada
from .ferramentas import consultar_produto, FalhaConsulta
from .llm import interpretar


class Estado(TypedDict, total=False):
    # Esta é a "ficha" compartilhada entre as etapas do agente.
    pergunta: str
    decisao: dict
    produto: dict
    erro: str
    tipo_erro: str
    resposta: str
    consultou_api: bool


def criar_grafo(decidir=interpretar, consultar=consultar_produto):
    """Dependências podem ser substituídas nos testes, sem acessar o Gemini."""
    def interpretar_pedido(estado):
        # O Gemini decide se é uma consulta, um conceito ou um pedido fora do escopo.
        try:
            decisao = Decisao.model_validate(decidir(estado['pergunta']))
            if decisao.acao == 'consultar':
                codigos = re.findall(r'\bPRD-[0-9]{3}\b', estado['pergunta'].upper())
                if len(set(codigos)) != 1 or decisao.codigo not in codigos:
                    return {'erro': 'Informe um único código, no formato PRD-001.'}
            return {'decisao': decisao.model_dump()}
        except Exception as exc:
            # Não expor mensagens do SDK: podem conter detalhes da requisição.
            return {'erro': 'Não foi possível interpretar a solicitação. Verifique a configuração e tente novamente.', 'tipo_erro': type(exc).__name__}

    def consultar_estoque(estado):
        # Só chegamos aqui quando a decisão pede uma consulta válida.
        try:
            produto = consultar(estado['decisao']['codigo'], os.getenv('ESTOQUE_API_URL', 'http://127.0.0.1:8000'))
            return {'produto': produto.model_dump(), 'consultou_api': True}
        except FalhaConsulta as exc:
            return {'erro': str(exc), 'consultou_api': True}

    def responder(estado):
        # Números de estoque são comparados em Python, sem pedir ao LLM para calculá-los.
        if estado.get('erro'):
            return {'resposta': estado['erro']}
        if estado.get('produto'):
            p = estado['produto']
            quantidade, minimo = p['quantidade_atual'], p['estoque_minimo']
            if quantidade == 0:
                situacao = 'esgotado'
            elif quantidade <= minimo:
                situacao = 'baixo (no limite mínimo)' if quantidade == minimo else 'baixo'
            else:
                situacao = 'normal (acima do mínimo)'
            return {'resposta': f"{p['codigo']} — {p['nome']}: {quantidade} {p['unidade']} disponíveis; mínimo {minimo}. Estoque {situacao}. Fonte: API de estoque."}
        d = estado['decisao']
        if d['acao'] == 'fora_escopo':
            return {'resposta': 'Posso consultar estoque e explicar conceitos. Não altero nem cadastro produtos.'}
        return {'resposta': d['resposta'] or 'Informe um código de produto ou uma pergunta conceitual sobre estoque.'}

    def escolher_caminho(estado):
        # Esta função implementa a transição condicional exigida pelo projeto.
        if not estado.get('erro') and estado['decisao']['acao'] == 'consultar':
            return 'consultar'
        return 'responder'

    grafo = StateGraph(Estado)
    # Montagem do caminho: três nós, uma escolha e um ponto final.
    grafo.add_node('interpretar', interpretar_pedido)
    grafo.add_node('consultar', consultar_estoque)
    grafo.add_node('responder', responder)
    grafo.add_edge(START, 'interpretar')
    grafo.add_conditional_edges('interpretar', escolher_caminho, {'consultar': 'consultar', 'responder': 'responder'})
    grafo.add_edge('consultar', 'responder')
    grafo.add_edge('responder', END)
    return grafo.compile()


def executar(pergunta: str):
    entrada = Entrada(pergunta=pergunta)
    return criar_grafo().invoke({'pergunta': entrada.pergunta, 'consultou_api': False}, {'recursion_limit': 8})
