# blockchain.py
from web3 import Web3
import json
import config

try:
    # Inicialização da conexão com a rede Ethereum
    print("Conectando ao nó Ethereum:", config.ETH_NODE_URL)
    w3 = Web3(Web3.HTTPProvider(config.ETH_NODE_URL))
    if not w3.is_connected():
        raise Exception("Falha ao conectar ao nó Ethereum. Verifique ETH_NODE_URL.")

    # Carregar o arquivo do ABI
    print("Lendo o arquivo ABI de:", config.CONTRACT_ABI_PATH)
    with open(config.CONTRACT_ABI_PATH, 'r') as abi_file:
        contract_json = json.load(abi_file)
    contract_abi = contract_json["abi"]
    print("Tipo de contract_abi:", type(contract_abi))
    print("Número de entradas na ABI:", len(contract_abi))
    print("Arquivo ABI carregado com sucesso.")

    # Recuperar o endereço do contrato
    contract_address = config.CONTRACT_ADDRESS
    checksumAddress = Web3.to_checksum_address(config.CONTRACT_ADDRESS)
    if not contract_address or contract_address == "":
        raise Exception("CONTRACT_ADDRESS não está definido ou está vazio.")

    print("Instanciando o contrato no endereço:", contract_address)
    # Instanciar o contrato
    contract = w3.eth.contract(address=checksumAddress, abi=contract_abi)
    print("Contrato instanciado com sucesso.")
except Exception as e:
    print("Erro ao inicializar o contrato:", str(e))
    raise

def register_event_on_blockchain(lot_id, event_type, geo_hash, details):
    """
    Registra um evento na blockchain chamando a função do smart contract.
    """
    account = config.ETH_ACCOUNT
    private_key = config.ETH_PRIVATE_KEY

    # Preparar a transação
    nonce = w3.eth.getTransactionCount(account)
    txn = contract.functions.registerEvent(lot_id, event_type, geo_hash, details).buildTransaction({
        'from': account,
        'nonce': nonce,
        'gas': config.GAS_LIMIT,
        'gasPrice': w3.toWei(config.GAS_PRICE, 'gwei')
    })

    # Assinar e enviar a transação
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return {
        "txHash": tx_hash.hex(),
        "status": tx_receipt.status,
        "blockNumber": tx_receipt.blockNumber
    }

def get_events_from_blockchain(lot_id):
    """
    Consulta o smart contract para recuperar os eventos registrados para o lote informado.
    """
    events = contract.functions.getEvents(lot_id).call()
    # Converter a estrutura de eventos (se necessário) para um formato amigável
    formatted_events = []
    for event in events:
        formatted_events.append({
            "timestamp": event[0],
            "eventType": event[1],
            "geoHash": event[2],
            "details": event[3]
        })
    return formatted_events
