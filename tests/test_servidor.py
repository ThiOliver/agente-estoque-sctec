"""Verifica o contrato HTTP sem consumir a API Gemini."""
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from servidor import app


class TestServidor(unittest.TestCase):
    def setUp(self):
        self.cliente = TestClient(app)

    def test_recebe_pergunta_e_entrega_ao_agente(self):
        with patch('servidor.executar', return_value={'resposta': 'Estoque baixo.'}) as executar:
            resposta = self.cliente.post('/perguntar', json={'pergunta': 'Consultar PRD-001'})
        executar.assert_called_once_with('Consultar PRD-001')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), {'resposta': 'Estoque baixo.'})

    def test_entrada_invalida_nao_chama_agente(self):
        with patch('servidor.executar') as executar:
            for entrada in ({}, {'pergunta': ' '}, {'pergunta': 'Consultar PRD-001', 'comando': 'extra'}):
                with self.subTest(entrada=entrada):
                    resposta = self.cliente.post('/perguntar', json=entrada)
                    self.assertEqual(resposta.status_code, 422)
        executar.assert_not_called()
