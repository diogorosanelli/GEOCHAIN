import json
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
CONTRACT_ABI_PATH = os.getenv("CONTRACT_ABI_PATH")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ETH_ACCOUNT = os.getenv("ETH_ACCOUNT")
ETH_PRIVATE_KEY = os.getenv("ETH_PRIVATE_KEY")
GAS_LIMIT = int(os.getenv("GAS_LIMIT"))
GAS_PRICE = int(os.getenv("GAS_PRICE"))

def initialize_web3():
    print("Conectando ao nó Ethereum:", ETH_NODE_URL)
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    if not w3.is_connected():
        raise Exception("Falha ao conectar ao nó Ethereum. Verifique ETH_NODE_URL.")
    return w3

def load_contract(w3):
    print("Lendo o arquivo ABI de:", CONTRACT_ABI_PATH)
    with open(CONTRACT_ABI_PATH, 'r') as abi_file:
        contract_json = json.load(abi_file)
    # Certifique-se de usar somente o array de ABI
    contract_abi = contract_json["abi"]
    print("Arquivo ABI carregado com sucesso. Número de entradas:", len(contract_abi))
    
    # Converter o endereço do contrato para o formato checksum
    contract_address = w3.to_checksum_address(CONTRACT_ADDRESS)
    print("Instanciando o contrato no endereço:", contract_address)
    
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    print("Contrato instanciado com sucesso!")
    return contract

def register_event_on_blockchain(globalid, event_type, geo_hash, details):
    try:
        w3 = initialize_web3()
        contract = load_contract(w3)
        account = ETH_ACCOUNT
        private_key = ETH_PRIVATE_KEY

        # Obter nonce
        nonce = w3.eth.get_transaction_count(account, 'latest')
        # Preparar os parâmetros da transação
        tx_params = {
            'from': account,
            'nonce': nonce,
            'gas': GAS_LIMIT,
            'gasPrice': w3.to_wei(GAS_PRICE, 'gwei')
        }

        # Tente construir a transação usando o método buildTransaction
        try:
            tx = contract.functions.registerEvent(globalid, event_type, geo_hash, details).buildTransaction(tx_params)
        except AttributeError as e:
            # Se buildTransaction não estiver disponível, tente build_transaction
            print("buildTransaction não encontrado, tentando build_transaction...")
            tx = contract.functions.registerEvent(globalid, event_type, geo_hash, details).build_transaction(tx_params)

        print("Transação construída com sucesso:", tx)
        
        # Assinar a transação
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        print("Transação assinada. Enviando...")
        
        # Enviar a transação assinada
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transação confirmada. Receipt:", receipt)
        
        return {
            "txHash": tx_hash.hex(),
            "status": receipt.status,
            "blockNumber": receipt.blockNumber
        }
    except Exception as e:
        print("Erro ao registrar o evento na blockchain:", str(e))
        raise

def get_events_from_blockchain(globalid):
    try:
        w3 = initialize_web3()
        contract = load_contract(w3)
        events = contract.functions.getEvents(globalid).call()
        # Converter os eventos para um formato Python (lista de dicionários)
        formatted_events = []
        for event in events:
            formatted_events.append({
                "timestamp": event[0],
                "eventType": event[1],
                "geoHash": event[2],
                "details": event[3]
            })
        return formatted_events
    except Exception as e:
        print("Erro ao obter eventos:", str(e))
        raise

# Exemplo de uso:
if __name__ == "__main__":
    # Apenas para teste manual
    result = register_event_on_blockchain(1, "plantio", "fakeGeoHash123", "Plantio realizado com sucesso.")
    print(result)
