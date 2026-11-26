"""Executa os três cenários com Gemini e API reais, salvando evidências."""
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from agente.state_graph import executar

load_dotenv(RAIZ / '.env')
casos = [
    ('Como está o estoque do PRD-001?', 'API consultada; 5 unidades, mínimo 10; estoque baixo.'),
    ('Como está o estoque do PRD-999?', 'API consultada; produto não encontrado.'),
    ('O que é estoque mínimo?', 'Explicação conceitual sem consultar a API.'),
]
registros = []
for pergunta, esperado in casos:
    resultado = executar(pergunta)
    registros.append({'entrada': pergunta, 'esperado': esperado, 'observado': resultado})
    print(json.dumps(registros[-1], ensure_ascii=False), flush=True)
    (RAIZ / 'evidencias' / 'cenarios_agente.json').write_text(
        json.dumps(registros, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if resultado.get('tipo_erro'):
        print('Teste interrompido: resolver a falha do modelo antes de repetir os cenários.')
        raise SystemExit(1)
