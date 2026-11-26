# Assistente de estoque — SCTEC

Projeto avaliativo de agentes de IA: Python, LLM, LangGraph, API de estoque do professor e automação complementar no n8n.

## Objetivo

Responder à pergunta: “Como está o estoque do produto PRD-001?”, consultando os dados reais da API simulada e comparando quantidade disponível e estoque mínimo. Também tratar produtos inexistentes e responder perguntas conceituais sem consulta desnecessária.

## Estado atual

Repositório criado e primeira consulta HTTP à API do professor realizada com sucesso. O agente e a integração n8n ainda não foram implementados. Docker instalado e n8n aberto no navegador, conforme verificação do usuário. Configuração do LLM pendente.

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

## Preparar Docker e abrir n8n

No Linux Mint 22.3, execute no terminal, dentro da pasta `agente-estoque`:

```bash
bash scripts/instalar_docker.sh
sudo docker compose up -d
```

O script configura o repositório oficial do Docker para a base Ubuntu Noble, instala Docker Engine e Compose e executa `hello-world`. Exige senha de administrador, digitada somente no terminal. O Docker informa que derivados como Mint não são oficialmente suportados; esta configuração usa a base Ubuntu do sistema.

Abra http://localhost:5678 e crie a conta local de acesso ao n8n. O volume `n8n_data` conserva os workflows quando o contêiner é parado. O serviço fica acessível apenas neste computador.

```bash
sudo docker compose ps       # verificar o serviço
sudo docker compose logs --tail=50 n8n  # consultar logs
sudo docker compose stop    # parar
sudo docker compose start   # iniciar novamente
```

Esta configuração prepara apenas o editor n8n. O workflow integrado ao agente será construído na etapa de integração. Instalação concluída; o usuário demonstrou a tela de configuração inicial do n8n no navegador.

## Organização Git

A preparação do agente está na branch `feature/agente-langgraph`. As dependências e o arquivo de exemplo abaixo preparam o ambiente; o grafo ainda não foi implementado.

## Ambiente Python do agente

Dentro de `agente-estoque`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copie `.env.example` para `.env` se este ainda não existir. Crie sua chave em https://aistudio.google.com/apikey e preencha `GEMINI_API_KEY` somente no `.env`. O modelo será escolhido após verificar a disponibilidade da conta. Não envie chaves por chat nem faça commit do `.env`.

Esta venv pertence ao agente e é independente da venv da API do professor. O n8n usa Docker e não depende de nenhuma delas.

## Branches

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
