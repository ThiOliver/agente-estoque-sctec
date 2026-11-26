# Assistente de estoque — SCTEC

Projeto avaliativo de agentes de IA: Python, LLM, LangGraph, API de estoque do professor e automação complementar no n8n.

## Objetivo

Responder à pergunta: “Como está o estoque do produto PRD-001?”, consultando os dados reais da API simulada e comparando quantidade disponível e estoque mínimo. Também tratar produtos inexistentes e responder perguntas conceituais sem consulta desnecessária.

## Estado atual

Repositório criado e primeira consulta HTTP à API do professor realizada com sucesso. O agente e a integração n8n ainda não foram implementados. Docker e configuração do LLM permanecem pendentes.

## Executar a API de apoio

Em uma pasta ao lado deste projeto:

```bash
git clone https://github.com/wangsouza/api-estoque.git api-estoque-professor
cd api-estoque-professor
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abra http://127.0.0.1:8000/docs para explorar a API. Em outro terminal:

```bash
curl --fail --silent --show-error http://127.0.0.1:8000/produtos/PRD-001
```

Resultado observado na preparação: Mouse sem fio, quantidade atual 5, estoque mínimo 10. A consulta funcionou; a análise pelo agente será implementada na próxima etapa. Este registro não substitui os três testes finais do agente.

## Sequência de desenvolvimento

1. Criar repositório e ambiente; executar uma consulta HTTP à API.
2. Montar LangGraph com LLM, estado compartilhado, nós, transição condicional e encerramento.
3. Demonstrar agente funcional, resposta fundamentada e erro tratado.
4. Integrar n8n via Docker e exportar o workflow JSON.
5. Registrar três testes: análise de estoque, produto inexistente e pergunta conceitual sem API.
6. Completar documentação e gravar vídeo de até cinco minutos.
7. Submeter os links no AVA até 30/11/2026 às 22h.

As etapas seguem o cronograma do curso, avançando conforme a conclusão de cada marco.

## Organização Git

- `main`: versões prontas para demonstração.
- `develop`: integração do desenvolvimento.
- `feature/...`: trabalho de cada etapa, integrado primeiro em `develop`.

## API de apoio

Repositório do professor: https://github.com/wangsouza/api-estoque

O código do agente será desenvolvido neste repositório. A API do professor é um componente separado.

## Entregáveis pendentes

- Código Python com LLM, LangGraph, ferramenta HTTP e validações.
- Workflow n8n exportado e evidência da troca de dados.
- Configuração e instruções reproduzíveis de execução.
- Entradas, resultados esperados, observados e evidências dos três testes.
- Arquitetura, limitações e link do vídeo.

Credenciais devem permanecer em `.env`, fora do Git. O projeto utiliza dados fictícios.
