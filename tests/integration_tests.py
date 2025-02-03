import sys
import os
import pytest
import json
import importlib

# Define o diretório raiz e o diretório backend para que o Python encontre os pacotes
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Importa os módulos de serviços para aplicar as substituições
import backend.services.arcgis as arcgis_module
import backend.services.blockchain as blockchain_module

# Define as funções fake para simulação
def fake_get_geographic_data(lot_id):
    return {"geoHash": "fakeGeoHash123", "feature": {"attributes": {"objectid": 1}}}

def fake_register_event_on_blockchain(lot_id, event_type, geo_hash, details):
    print("Fake register_event_on_blockchain chamada")
    return {"txHash": "0xfake", "status": 1, "blockNumber": 12345}

def fake_get_events_from_blockchain(lot_id):
    return [{
        "timestamp": 1630000000,
        "eventType": "plantio",
        "geoHash": "fakeGeoHash123",
        "details": "Plantio realizado com sucesso."
    }]

# Aplica as substituições diretamente nos módulos dos serviços
arcgis_module.get_geographic_data = fake_get_geographic_data
blockchain_module.register_event_on_blockchain = fake_register_event_on_blockchain
blockchain_module.get_events_from_blockchain = fake_get_events_from_blockchain

# Agora, recarregue o módulo da aplicação para garantir que ele use as funções fake
import backend.app as app_module
importlib.reload(app_module)
app = app_module.app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """
    Testa se a rota raiz retorna a mensagem esperada.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"GeoChain Backend is Running!" in response.data

def test_register_and_get_event(client):
    """
    Testa o fluxo de registro e recuperação de um evento.
    Como as funções de serviço já foram monkeypatched antes da importação do app,
    o endpoint /register_event deve retornar os valores simulados.
    """
    # Testa o endpoint de registro de evento
    payload = {
        "lotId": 1,
        "eventType": "plantio",
        "details": "Plantio realizado com sucesso."
    }
    response = client.post("/register_event", data=json.dumps(payload), content_type="application/json")
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data["message"] == "Evento registrado com sucesso!"
    # Agora, como a função fake foi aplicada, o hash retornado deve ser "0xfake"
    assert data["transaction"]["txHash"] == "0xfake"

    # Testa o endpoint para recuperar eventos
    response = client.get("/get_events/1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["eventType"] == "plantio"
    assert data[0]["geoHash"] == "fakeGeoHash123"
    assert data[0]["details"] == "Plantio realizado com sucesso."
