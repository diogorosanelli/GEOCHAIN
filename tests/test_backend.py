import sys
sys.path.insert(0, "/mnt/d/PESSOAL/2025/250131-GEOCHAIN/source/GeoChain")

import pytest
import json
from backend.app import app  # Certifique-se de que sua aplicação Flask está exposta como "app"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_endpoint(client):
    """Verifica se o endpoint raiz está funcionando."""
    response = client.get('/')
    assert response.status_code == 200
    # Supondo que a página inicial mencione 'GeoChain'
    assert b"GeoChain" in response.data

def test_register_event(client):
    """
    Testa o endpoint responsável por registrar um evento.
    Esse teste simula a chamada para registrar, por exemplo, um evento de plantio.
    """
    # Exemplo de payload; adapte conforme a implementação real
    payload = {
        "evento": "Plantio",
        "detalhes": "Início do plantio de soja",
        "localizacao": {"lat": -23.5505, "lng": -46.6333}
    }
    response = client.post('/api/eventos', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data.get("status") == "sucesso"
    # Opcional: verifique se o backend repassa o comando para o smart contract conforme esperado.
