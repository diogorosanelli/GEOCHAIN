# tests/test_blockchain.py
import json
import os
import pytest
from web3 import Web3

# Constantes fornecidas
ETH_NODE_URL = "http://127.0.0.1:7545"
CONTRACT_ABI_PATH = "/mnt/d/PESSOAL/2025/250131-GEOCHAIN/source/GeoChain/blockchain/build/contracts/GeoChainTracker.json"
CONTRACT_ADDRESS = "0x2c41BA0Ec2674626FfBD9611cd1e52D0F99b6c98"
ETH_ACCOUNT = "0xe7394dE96a2F17D79de7D9063Ee9155B5B2162e5"

@pytest.fixture(scope="module")
def w3():
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    assert w3.is_connected(), "Não foi possível conectar ao nó Ethereum"
    print('Nó Ethereum conectado com sucesso')
    w3.eth.defaultAccount = ETH_ACCOUNT  # Define a conta padrão para as transações
    return w3

@pytest.fixture(scope="module")
def contract(w3):
    # Carrega o ABI a partir do arquivo JSON
    with open(CONTRACT_ABI_PATH, "r") as f:
        contract_data = json.load(f)
    # Se o JSON tiver a chave "abi", utiliza-a; caso contrário, usa o próprio conteúdo
    abi = contract_data.get("abi", contract_data)
    return w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def test_register_and_get_events(contract, w3):
    lot_id = 1  # Identificador do lote para o teste

    # Consulta os eventos já registrados para o lote
    initial_events = contract.functions.getEvents(lot_id).call()
    initial_count = len(initial_events)

    # Dados do evento a ser registrado
    event_type = "plantio"
    geo_hash = "geo123"
    details = "detalhes do plantio"

    # Envia a transação utilizando o método transact()
    tx_hash = contract.functions.registerEvent(
        lot_id,
        event_type,
        geo_hash,
        details
    ).transact({
        "from": ETH_ACCOUNT,
        "gas": 3000000
    })

    # Converte o tx_hash para string hexadecimal, se necessário
    if isinstance(tx_hash, bytes):
        tx_hash = tx_hash.hex()

    # Aguarda a confirmação da transação
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Recupera novamente os eventos para o mesmo lote
    updated_events = contract.functions.getEvents(lot_id).call()
    updated_count = len(updated_events)

    # Verifica se o número de eventos aumentou em 1
    assert updated_count == initial_count + 1, "O número de eventos não aumentou após o registro"
    print("Evento registrado com sucesso!")

    # Valida os dados do novo evento
    # Supondo que a estrutura do evento seja: (timestamp, eventType, geoHash, details)
    novo_evento = updated_events[-1]
    assert novo_evento[1] == event_type, f"Esperado '{event_type}', obtido '{novo_evento[1]}'"
    print(f"Tipo de evento '{event_type}' validado com sucesso!")
    
    assert novo_evento[2] == geo_hash, f"Esperado '{geo_hash}', obtido '{novo_evento[2]}'"
    print(f"GeoHash '{geo_hash}' validado com sucesso!")
    
    assert novo_evento[3] == details, f"Esperado '{details}', obtido '{novo_evento[3]}'"
    print(f"Detalhes '{details}' validados com sucesso!")
    
