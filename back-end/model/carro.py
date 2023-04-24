from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from  model import Base
from typing import Union


class Carro(Base):
    __tablename__ = 'carro'

    id = Column("id", Integer, primary_key=True)
    marca = Column(String(140))
    modelo = Column(String(140))
    placa = Column(String(140), unique=True)
    ano = Column(String(140))
    quilometragem = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())
   


    def __init__(self, marca:str,modelo:str,placa:str,ano:str,quilometragem:str, data_insercao:Union[DateTime, None] = None):
        """
        Cadastra um carro

        Arguments:
            Marca: Marca do carro
            Modelo: Modelo do carro
            Ano: Ano de fabricação do carro
            Placa: Placa do carro
            Quilometragem: Quilometragem atual de entrada na loja
            
        """
        self.marca = marca
        self.modelo = modelo
        self.placa = placa
        self.ano = ano
        self.quilometragem = quilometragem

        # se não for informada a data, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao