from pydantic import BaseModel
from typing import Optional, List
from model.pessoa import Pessoa
from schemas import ComentarioSchema


class PessoaSchema(BaseModel):
    """ Define como uma nova pessoa a ser inserido deve ser representado
    """
    nome: str = "Tiago"
  


class PessoaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da pessoa.
    """
    nome: str = "Tiago"
  


class ListagemPessoaSchema(BaseModel):
    """ Define como uma listagem de pessoas será retornada.
    """
    pessoas:List[PessoaSchema]


def apresenta_pessoas(pessoas: List[Pessoa]):
    """ Retorna uma representação de pessoas seguindo o schema definido em
        PessoaViewSchema.
    """
    result = []
    for pessoa in pessoas:
        result.append({
            "nome": pessoa.nome,
        })

    return {"pessoas": result}


class PessoaViewSchema(BaseModel):
    """ Define como uma pessoa será retornado: pessoa + comentários.
    """
    id: int = 1
    nome: str = "Banana Prata"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class PessoaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_pessoa(pessoa: Pessoa):
    """ Retorna uma representação do pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        "id": pessoa.id,
        "nome": pessoa.nome,
        "total_cometarios": len(pessoa.comentarios),
        "comentarios": [{"texto": c.texto} for c in pessoa.comentarios]
    }