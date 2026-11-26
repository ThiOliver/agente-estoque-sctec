"""Contratos: validam o que entra e o que vem do modelo e da API."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Entrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    pergunta: str = Field(min_length=3, max_length=1000)


class Decisao(BaseModel):
    model_config = ConfigDict(extra='forbid')
    acao: Literal['consultar', 'conceito', 'esclarecer', 'fora_escopo']
    codigo: str | None = None
    resposta: str = Field(max_length=2000)


class Produto(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    codigo: str = Field(pattern=r'^PRD-\d{3}$')
    nome: str = Field(min_length=1, max_length=200)
    categoria: str = Field(min_length=1, max_length=200)
    quantidade_atual: int = Field(ge=0)
    estoque_minimo: int = Field(ge=0)
    unidade: str = Field(min_length=1, max_length=30)
