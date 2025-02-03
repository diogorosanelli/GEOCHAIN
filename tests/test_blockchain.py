# tests/test_blockchain.py
import os
import json
import pytest
from web3 import Web3

@pytest.fixture(scope="module")
def w3():
    # Conecta a um nó local; ajuste a URL se necessário.
    provider_url = os.getenv("WEB3_PROVIDER_URL", "http://127.0.0.1:8545")
    w3 = Web3(Web3.HTTPProvider(provider_url))
    assert w3.isConnected(), "Web3 não conseguiu conectar com o provedor"
    return w3

@pytest.fixture(scope="module")
def contract(w3):
    # Carrega o ABI do contrato a partir do JSON gerado pela compilação (por exemplo, via Truffle)
    contract_address = os.getenv("GEOCHAIN_CONTRACT_ADDRESS")
    assert contract_address, "A variável de ambiente GEOCHAIN_CONTRACT_ADDRESS não está definida"
    abi_path = os.path.join("blockchain", "contracts", "GeoChainTracker.json")
    with open(abi_path, "r") as f:
         contract_data = json.load(f)
    abi = contract_data.get("abi")
    assert abi, "ABI não encontrado no arquivo GeoChainTracker.json"
    return w3.eth.contract(address=contract_address, abi=abi)

def test_contract_call(contract):
    """
    Exemplo de teste que chama uma função do contrato.
    Supondo que exista uma função 'getEventCount' que retorne um número.
    Ajuste o nome da função conforme a implementação.
    """
    event_count = contract.functions.getEventCount().call()
    assert isinstance(event_count, int), "A função getEventCount não retornou um inteiro"
