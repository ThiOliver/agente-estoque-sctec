"""Testes locais com decisão simulada: não comprovam funcionamento do LLM real."""
import unittest
from agente.contratos import Decisao, Produto
from agente.ferramentas import FalhaConsulta
from agente.state_graph import criar_grafo


class TestGrafo(unittest.TestCase):
    def rodar(self, decisao, ferramenta, pergunta='Consultar PRD-001'):
        return criar_grafo(lambda _: decisao, ferramenta).invoke(
            {'pergunta': pergunta, 'consultou_api': False})

    def test_estoque_e_limites(self):
        for quantidade, esperado in [(0, 'esgotado'), (5, 'baixo'), (10, 'no limite'), (11, 'normal')]:
            with self.subTest(quantidade=quantidade):
                produto = Produto(codigo='PRD-001', nome='Mouse', categoria='Periféricos',
                                  quantidade_atual=quantidade, estoque_minimo=10, unidade='un')
                resultado = self.rodar(Decisao(acao='consultar', codigo='PRD-001', resposta=''), lambda *_: produto)
                self.assertIn(esperado, resultado['resposta'])
                self.assertTrue(resultado['consultou_api'])

    def test_produto_inexistente(self):
        def ausente(*_):
            raise FalhaConsulta('Produto não encontrado na API de estoque.')
        resultado = self.rodar(Decisao(acao='consultar', codigo='PRD-001', resposta=''), ausente)
        self.assertIn('não encontrado', resultado['resposta'])

    def test_conceito_nao_consulta(self):
        def proibido(*_):
            self.fail('A pergunta conceitual não deveria acessar a API.')
        resultado = self.rodar(Decisao(acao='conceito', resposta='Estoque mínimo é um limite de referência.'), proibido,
                              'O que é estoque mínimo?')
        self.assertFalse(resultado['consultou_api'])
        self.assertIn('limite', resultado['resposta'])

    def test_codigo_inventado_bloqueado(self):
        def proibido(*_):
            self.fail('Código inventado não pode chegar à API.')
        resultado = self.rodar(Decisao(acao='consultar', codigo='PRD-999', resposta=''), proibido)
        self.assertFalse(resultado['consultou_api'])
        self.assertIn('Informe um único código', resultado['resposta'])

    def test_falha_modelo(self):
        def falha(_):
            raise RuntimeError('detalhe privado')
        resultado = criar_grafo(falha).invoke({'pergunta': 'Consultar PRD-001', 'consultou_api': False})
        self.assertNotIn('detalhe privado', resultado['resposta'])
        self.assertFalse(resultado['consultou_api'])


if __name__ == '__main__':
    unittest.main()
