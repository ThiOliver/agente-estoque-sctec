"""Executa os três cenários com Gemini e API reais, salvando evidências."""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import os
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
for numero, (pergunta, esperado) in enumerate(casos, start=1):
    resultado = executar(pergunta)
    if numero == 1:
        produto = resultado.get('produto', {})
        passou = (resultado.get('consultou_api') is True
                  and produto.get('codigo') == 'PRD-001'
                  and produto.get('quantidade_atual') == 5
                  and produto.get('estoque_minimo') == 10
                  and 'Estoque baixo' in resultado['resposta'])
    elif numero == 2:
        passou = (resultado.get('consultou_api') is True
                  and resultado.get('erro') == 'Produto não encontrado na API de estoque.')
    else:
        passou = (resultado.get('consultou_api') is False
                  and resultado.get('decisao', {}).get('acao') == 'conceito'
                  and bool(resultado.get('resposta')) and not resultado.get('erro'))
    registros.append({'entrada': pergunta, 'esperado': esperado, 'observado': resultado,
                      'verificacao_automatica': 'PASSOU' if passou else 'FALHOU',
                      'modelo': os.getenv('GEMINI_MODEL'),
                      'executado_em_utc': datetime.now(timezone.utc).isoformat()})
    print(json.dumps(registros[-1], ensure_ascii=False), flush=True)
    (RAIZ / 'evidencias' / 'cenarios_agente.json').write_text(
        json.dumps(registros, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if resultado.get('tipo_erro'):
        print('Teste interrompido: resolver a falha do modelo antes de repetir os cenários.')
        raise SystemExit(1)

if any(registro['verificacao_automatica'] == 'FALHOU' for registro in registros):
    raise SystemExit(1)
print('Os três cenários passaram. Revise também a explicação conceitual registrada.')
