# config.py

# Configurações do servidor Flask
PORT = 5000

# Configurações do ArcGIS Enterprise
ARCGIS_BASE_URL = "https://saopaulo.img.com.br/innovaserver/rest/services/Hosted/SJC/FeatureServer/24"
# ARCGIS_TOKEN = "SEU_TOKEN_DO_ARCGIS_ONLINE"

# Configurações da rede Ethereum
ETH_NODE_URL = "http://127.0.0.1:7545"
CONTRACT_ABI_PATH = "/mnt/d/PESSOAL/2025/250131-GEOCHAIN/source/GeoChain/blockchain/build/contracts/GeoChainTracker.json"  # Certifique-se de gerar e salvar o ABI
CONTRACT_ADDRESS = "0x2c41BA0Ec2674626FfBD9611cd1e52D0F99b6c98"
ETH_ACCOUNT = "0xe7394dE96a2F17D79de7D9063Ee9155B5B2162e5"
ETH_PRIVATE_KEY = "0xf9f9981bae86d59f20eb512d7c1b2a90317d9d105f5f5e8861674cd85d8baf23"

# Parâmetros de transação
GAS_LIMIT = 3000000
GAS_PRICE = 20  # em Gwei
