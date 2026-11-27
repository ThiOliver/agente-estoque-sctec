"""Recebe perguntas do n8n por HTTP e entrega ao mesmo agente do terminal."""
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from agente.contratos import Entrada
from agente.state_graph import executar

load_dotenv(Path(__file__).resolve().parent / '.env')
app = FastAPI(title='Assistente de estoque SCTEC')


@app.get('/health')
def verificar_servidor():
    # Apenas verifica se o servidor está ligado; não chama o Gemini.
    return {'status': 'ok', 'servico': 'agente-estoque'}


@app.post('/perguntar')
def perguntar(entrada: Entrada):
    # O FastAPI valida o JSON usando o contrato Entrada antes de chamar o grafo.
    return executar(entrada.pergunta)
