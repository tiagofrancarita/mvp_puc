from pydantic import BaseModel
from typing import Optional, List
from model.carro import Carro



class CarroSchema(BaseModel):
    """ Define como um novo carro a ser cadastrado deve ser representado
    """
    marca:str = "Honda"
    modelo:str = "City"
    placa:str = "LQJ-9685"
    ano:str = "2019"
    quilometragem:str = "100690"
class CarroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do carro.
    """
    id: int = 1
class CarroBuscaPlacaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na placa do carro
    """
    placa: str = "LQJ-1010"
class ListagemCarrosSchema(BaseModel):
    """ Define como uma listagem de carros será retornada.
    """
    carros:List[CarroSchema]

def apresenta_carros(carros: List[Carro]):
    """ Retorna uma representação de carros seguindo o schema definido em
        CarroViewSchema.
    """
    result = []
    for carro in carros:
        result.append({
            "id": carro.id,
            "marca":carro.marca,
            "modelo":carro.modelo,
            "placa": carro.placa,
            "ano": carro.ano,
            "quilometragem": carro.quilometragem,
        })

    return {"carros": result}
class CarroViewSchema(BaseModel):
    """ Define como um carro será retornado.
    """
    id: int = 1
    marca:str = "Honda"
    modelo:str = "City"
    placa:str = "LQJ-9685"
    ano:str = "2019"
    quilometragem:str = "100690"
class CarroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int

def apresenta_carro(carro: Carro):
    """ Retorna uma representação do carro seguindo o schema definido em
        CarroViewSchema.
    """
    return {
        "id": carro.id,
        "marca": carro.marca,
        "modelo": carro.modelo,
        "placa": carro.placa,
        "ano": carro.ano,
        "quilometragem": carro.quilometragem,
        "Data Cadastro": carro.data_insercao
    }