# config.py

# Configurações do servidor Flask
PORT = 5000

# Configurações do ArcGIS Enterprise
ARCGIS_BASE_URL = "https://saopaulo.img.com.br/innovaserver/rest/services/Hosted/SJC/FeatureServer/24"
# ARCGIS_TOKEN = "SEU_TOKEN_DO_ARCGIS_ONLINE"

# Configurações da rede Ethereum
ETH_NODE_URL = "http://127.0.0.1:7545"
CONTRACT_ABI_PATH = "/mnt/d/PESSOAL/2025/250131-GEOCHAIN/source/GeoChain/blockchain/build/contracts/GeoChainTracker.json"  # Certifique-se de gerar e salvar o ABI
CONTRACT_ADDRESS = "0xc31d60439D1E188a29E1511928740fEbB5a983fb"
ETH_ACCOUNT = "0x065488A62018c0eeb961A5A50a45CF26Cdb57d4F"
ETH_PRIVATE_KEY = "0xd10e6c56ae96a4265e99d7cf9931e23e08ba2e6a63c15d5fd2ec95feea6a4ebd"

# Parâmetros de transação
GAS_LIMIT = 3000000
GAS_PRICE = 20  # em Gwei
