"""Ferramenta somente de leitura: GET /produtos/{codigo}."""
import re
import httpx
from pydantic import ValidationError
from .contratos import Produto


class FalhaConsulta(Exception):
    """Erro controlado que pode ser apresentado ao usuário."""


def consultar_produto(codigo: str, base_url: str) -> Produto:
    """Recebe código PRD-XXX e URL configurada; retorna Produto validado."""
    if not re.fullmatch(r'PRD-[0-9]{3}', codigo):
        raise FalhaConsulta('Código inválido. Use o formato PRD-001.')
    try:
        resposta = httpx.get(f'{base_url.rstrip("/")}/produtos/{codigo}', timeout=10)
        if resposta.status_code == 404:
            raise FalhaConsulta('Produto não encontrado na API de estoque.')
        resposta.raise_for_status()
        produto = Produto.model_validate(resposta.json())
        if produto.codigo != codigo:
            raise FalhaConsulta('A API retornou um código diferente do solicitado.')
        return produto
    except httpx.HTTPError as exc:
        raise FalhaConsulta('API indisponível ou com erro. Tente novamente mais tarde.') from exc
    except (ValidationError, ValueError) as exc:
        raise FalhaConsulta('A API retornou dados inválidos; a análise foi interrompida.') from exc
