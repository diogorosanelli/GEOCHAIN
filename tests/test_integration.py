# tests/test_integration.py
import sys
sys.path.insert(0, "/mnt/d/PESSOAL/2025/250131-GEOCHAIN/source/GeoChain")

import os
import pytest
import requests

# Supondo que o backend seja uma aplicação Flask e possua um endpoint /health
from backend.app import app

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_backend_health(client):
    """
    Valida que o endpoint de saúde (health) do backend retorne status 200.
    Ajuste a rota conforme a implementação do seu backend.
    """
    response = client.get('/health')
    assert response.status_code == 200, "O backend não retornou status 200 na rota /health"

def test_frontend_index_exists():
    """
    Verifica que o arquivo index.html do frontend existe e contém a palavra-chave 'GeoChain'.
    """
    frontend_index = os.path.join("frontend", "index.html")
    assert os.path.exists(frontend_index), "Arquivo index.html do frontend não encontrado"
    with open(frontend_index, "r", encoding="utf-8") as f:
        content = f.read()
        assert "GeoChain" in content, "Conteúdo esperado não foi encontrado no index.html"
