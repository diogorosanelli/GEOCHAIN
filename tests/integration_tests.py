# tests/integration_tests.py
import sys
import os
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_DIR = os.path.join(ROOT_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from app import app  # Importa a instância Flask do app.py
from services.arcgis import get_geographic_data
from services.blockchain import register_event_on_blockchain, get_events_from_blockchain

# Configurar o cliente de teste do Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Teste para verificar se a rota raiz está funcionando."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"GeoChain Backend is Running!" in response.data

def test_register_event(client, monkeypatch):
    """
    Teste para o endpoint /register_event.
    Este teste utiliza monkeypatch para simular as funções de consulta do ArcGIS e registro na blockchain.
    """
    # Simular a função get_geographic_data para retornar um geoHash fixo
    def fake_get_geographic_data(lot_id):
        return {"geoHash": "fakeGeoHash123", "feature": {"attributes": {"objectid": 1}}}
    monkeypatch.setattr("backend.arcgis_service.get_geographic_data", fake_get_geographic_data)
    
    # Simular a função register_event_on_blockchain para retornar uma transação simulada
    def fake_register_event_on_blockchain(lot_id, event_type, geo_hash, details):
        return {"txHash": "0xfake", "status": 1, "blockNumber": 12345}
    monkeypatch.setattr("backend.blockchain.register_event_on_blockchain", fake_register_event_on_blockchain)
    
    # Dados para o teste
    payload = {
        "lotId": 1,
        "eventType": "plantio",
        "details": "Plantio realizado com sucesso."
    }
    
    response = client.post("/register_event", data=json.dumps(payload), content_type="application/json")
    data = json.loads(response.data)
    
    # Verificar se o status code e os dados da resposta estão corretos
    assert response.status_code == 201
    assert data["message"] == "Evento registrado com sucesso!"
    assert data["transaction"]["txHash"] == "0xfake"

def test_get_events(client, monkeypatch):
    """
    Teste para o endpoint /get_events/<lot_id>.
    Simula a função get_events_from_blockchain para retornar um conjunto fixo de eventos.
    """
    fake_events = [
        {
            "timestamp": 1630000000,
            "eventType": "colheita",
            "geoHash": "fakeGeoHash456",
            "details": "Colheita realizada com sucesso."
        }
    ]
    monkeypatch.setattr("backend.blockchain.get_events_from_blockchain", lambda lot_id: fake_events)
    
    response = client.get("/get_events/1")
    data = json.loads(response.data)
    
    # Verificar se a resposta contém os eventos simulados
    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["eventType"] == "colheita"
    assert data[0]["geoHash"] == "fakeGeoHash456"
