from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Carro
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API - Garagem S-A", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
carro_tag = Tag(name="Carro", description="Adição, visualização e remoção de carros à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/carro', tags=[carro_tag],
          responses={"200": CarroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_carro(form: CarroSchema):
    """Adiciona um novo carro à base de dados

    Retorna uma representação de carro.
    """
    carro = Carro(
        marca=form.marca,
        modelo=form.modelo,
        placa=form.placa,
        ano=form.ano,
        quilometragem=form.quilometragem)
        
    logger.debug(f"Adicionando carro de placa: '{carro.placa}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(carro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado carro de placa: '{carro.placa}'")
        return apresenta_carro(carro), 200

    except IntegrityError as e:
        # como a duplicidade de placa é a provável razão do IntegrityError
        error_msg = "Carro com a mesma placa já cadastrado, verifique"
        logger.warning(f"Erro ao adicionar carro '{carro.id}','{carro.marca}','{carro.modelo}','{carro.placa}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar carro"
        logger.warning(f"Erro ao adicionar carro '{carro.id}','{carro.marca}','{carro.modelo}','{carro.placa}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.get('/carros', tags=[carro_tag],
         responses={"200": ListagemCarrosSchema, "404": ErrorSchema})
def get_carros():
    """Faz a busca por todos os carros cadastrados
    Retorna uma representação da listagem de carros.
    """
    logger.debug(f"Coletando carros ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carros = session.query(Carro).all()

    if not carros:
        # se não há carro cadastrados
        return {"carros": []}, 200
    else:
        logger.debug(f"%d Carros econtrados" % len(carros))
        # retorna a representação de carro
        print(carros)
        return apresenta_carros(carros), 200

@app.get('/carro', tags=[carro_tag],
         responses={"200": CarroViewSchema, "404": ErrorSchema})
def get_carro(query: CarroBuscaSchema):
    """Faz a busca por um carro a partir do id do produto
       Retorna uma representação do carro.
    """
    carro_id = query.id
    logger.debug(f"Coletando dados sobre carro #{carro_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carro = session.query(Carro).filter(Carro.id == carro_id).first()

    if not carro:
        # se o carro não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao buscar o carro com o ID: '{carro_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Carro econtrado: '{carro.modelo}','{carro.marca}''{carro.placa}'")
        # retorna a representação de carro
        return apresenta_carro(carro), 200
    
@app.get('/carro', tags=[carro_tag],
         responses={"200": CarroViewSchema, "404": ErrorSchema})
def get_carroPlaca(query: CarroBuscaPlacaSchema):
    """Faz a busca por um carro a partir da placa do carro
       Retorna uma representação do carro.
    """
    carro_placa = query.placa
    logger.debug(f"Coletando dados sobre carro #{carro_placa}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carro = session.query(Carro).filter(Carro.placa == carro_placa).first()

    if not carro:
        # se o carro não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao buscar o carro com a placa informada: '{carro_placa}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Carro econtrado: '{carro.modelo}','{carro.marca}''{carro.placa}'")
        # retorna a representação de produto
        return apresenta_carro(carro), 200
    
@app.delete('/carro', tags=[carro_tag],
            responses={"200": CarroDelSchema, "404": ErrorSchema})
def del_carro(query: CarroBuscaSchema):
    """Deleta um Carro a partir do id do carro
    Retorna uma mensagem de confirmação da remoção.
    """
    carro_id = query.id
    print(carro_id)
    logger.debug(f"Deletando dados do carro id: #{carro_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Carro).filter(Carro.id == carro_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado carro #{carro_id}")
        return {"mesage": "Carro removido", "id": carro_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        logger.warning(f"Erro ao deletar carro #'{carro_id}', {error_msg}")
        return {"mesage": error_msg}, 404