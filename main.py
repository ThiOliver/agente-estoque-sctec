"""Comece a leitura do projeto por este arquivo."""
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError
from agente.state_graph import executar

# 1. Ler a configuração local, incluindo a chave que não vai para o GitHub.
load_dotenv(Path(__file__).resolve().parent / '.env')

# 2. Receber a pergunta escrita no terminal.
if len(sys.argv) < 2:
    print('Uso: python main.py "Como está o estoque do PRD-001?"')
    raise SystemExit(1)

pergunta = ' '.join(sys.argv[1:])

# 3. Passar a pergunta ao grafo e mostrar o resultado.
try:
    resultado = executar(pergunta)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
except ValidationError:
    print('Pergunta inválida: informe de 3 a 1000 caracteres.')
    raise SystemExit(1)
