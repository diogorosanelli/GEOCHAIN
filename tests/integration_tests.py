import sys
import os
import pytest
import json
import importlib

# Adiciona o diretório "backend" ao sys.path para que o Python encontre o pacote.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Importa os módulos de serviços para referência (se necessário para o monkeypatch)
from backend.services import arcgis, blockchain

# Define as funções fake
def fake_get_geographic_data(lot_id):
    return {"geoHash": "fakeGeoHash123", "feature": {"attributes": {"objectid": 1}}}

fake_tx_receipt = {"txHash": "0xfake", "status": 1, "blockNumber": 12345}
def fake_register_event_on_blockchain(lot_id, event_type, geo_hash, details):
    print("Fake register_event_on_blockchain chamada")
    return fake_tx_receipt

def fake_get_events_from_blockchain(lot_id):
    return [{
        "timestamp": 1630000000,
        "eventType": "plantio",
        "geoHash": "fakeGeoHash123",
        "details": "Plantio realizado com sucesso."
    }]

# Importa o módulo app e sobrescreve as funções já importadas (no escopo global)
import backend.app as app_module
# Força a substituição das funções que o app usa diretamente.
setattr(app_module, 'get_geographic_data', fake_get_geographic_data)
setattr(app_module, 'register_event_on_blockchain', fake_register_event_on_blockchain)
setattr(app_module, 'get_events_from_blockchain', fake_get_events_from_blockchain)

# Se app.py já importou essas funções de services, precisamos sobrescrevê-las também no seu namespace.
# Por exemplo, se em app.py houver:
#   from services.arcgis import get_geographic_data
# então podemos fazer:
app_module.__dict__['get_geographic_data'] = fake_get_geographic_data
app_module.__dict__['register_event_on_blockchain'] = fake_register_event_on_blockchain
app_module.__dict__['get_events_from_blockchain'] = fake_get_events_from_blockchain

# Se necessário, recarregue o módulo para garantir que as alterações sejam aplicadas.
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
    Como as funções de serviço foram substituídas no escopo global do módulo app,
    o endpoint /register_event deverá retornar os valores simulados.
    """
    # Testa o endpoint /register_event
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

    # Testa o endpoint /get_events/1
    response = client.get("/get_events/1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["eventType"] == "plantio"
    assert data[0]["geoHash"] == "fakeGeoHash123"
    assert data[0]["details"] == "Plantio realizado com sucesso."
