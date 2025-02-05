# tests/test_backend.py
import pytest
from backend.app import app # Importa a instância do Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
         yield client

def test_home(client):
    """
    Testa se a rota principal retorna status 200.
    (Ajuste a rota se necessário.)
    """
    response = client.get('/')
    assert response.status_code == 200, "A rota '/' não retornou status 200"

# Adicione outros testes específicos para funções do backend,
# como por exemplo, a integração com o ArcGIS ou a interação com o blockchain.
