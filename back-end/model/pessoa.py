from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base, Comentario


class Pessoa(Base):
    __tablename__ = 'pessoa'

    id = Column("id", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
   

    # Definição do relacionamento entre a pessoa e o comentário.
    # Essa relação é implicita, não está salva na tabela 'pessoa',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str):
        """
        Cria uma Pessoa

        Arguments:
            nome: Nome completo
        """
        self.nome = nome


    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Produto
        """
        self.comentarios.append(comentario)