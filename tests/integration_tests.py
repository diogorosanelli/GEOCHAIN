import sys
import os
import pytest
import json

# Adiciona o diretório "backend" (localizado na raiz) ao sys.path.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Importa a instância do Flask do módulo app (que está em backend/)
from app import app

# Se você precisar testar também os módulos de services, poderá importar assim:
# from services.arcgis import get_geographic_data
# from services.blockchain import register_event_on_blockchain, get_events_from_blockchain

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

def test_register_and_get_event(client, monkeypatch):
    """
    Testa o fluxo de registro e recuperação de um evento.
    Utiliza monkeypatch para simular as funções dos serviços.
    """
    # Simula a função get_geographic_data definida em backend/services/arcgis.py
    def fake_get_geographic_data(lot_id):
        return {"geoHash": "fakeGeoHash123", "feature": {"attributes": {"objectid": 1}}}
    monkeypatch.setattr("backend.services.arcgis.get_geographic_data", fake_get_geographic_data)

    # Simula as funções do módulo blockchain
    fake_tx_receipt = {"txHash": "0xfake", "status": 1, "blockNumber": 12345}
    def fake_register_event_on_blockchain(lot_id, event_type, geo_hash, details):
        return fake_tx_receipt
    def fake_get_events_from_blockchain(lot_id):
        return [{
            "timestamp": 1630000000,
            "eventType": "plantio",
            "geoHash": "fakeGeoHash123",
            "details": "Plantio realizado com sucesso."
        }]
    monkeypatch.setattr("backend.services.blockchain.register_event_on_blockchain", fake_register_event_on_blockchain)
    monkeypatch.setattr("backend.services.blockchain.get_events_from_blockchain", fake_get_events_from_blockchain)

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
    assert data["transaction"]["txHash"] == "0xfake"

    # Testa o endpoint /get_events/1
    response = client.get("/get_events/1")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["eventType"] == "plantio"
    assert data[0]["geoHash"] == "fakeGeoHash123"
    assert data[0]["details"] == "Plantio realizado com sucesso."
