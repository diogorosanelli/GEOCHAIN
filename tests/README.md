# Test Suite - GeoChain

Este diretório contém os testes para validar a solução GeoChain. A suite de testes está dividida em três partes:

- **Teste de Integração:** `test_integration.py` – Valida a integração entre os componentes (backend, blockchain e frontend).
- **Teste do Backend:** `test_backend.py` – Executa testes unitários e de endpoints do backend.
- **Teste do Blockchain:** `test_blockchain.py` – Valida a interação com os smart contracts na rede Ethereum.
- **Teste do Frontend:** `test_frontend.py` – Verifica o carregamento e a integridade da aplicação frontend.

## Requisitos

- **Python 3.x**
- **Node.js e NPM** (para dependências do blockchain, se necessário)
- **Web3.py** (para testes do smart contract)
- **Selenium WebDriver** (para testes do frontend)
- **Chrome ou Firefox** (para execução dos testes do frontend em modo headless)

## Execução dos Testes

### Teste de Integração

Para executar o teste de integração, execute:
```bash
pytest tests/test_integration.py
```

### Teste do Backend
Para executar os testes do backend, na raiz do projeto, execute:
```bash
pytest tests/test_backend.py
```

### Teste do Blockchain
Antes de executar:

- Certifique-se de que um nó Ethereum de testes (ex.: Ganache) esteja rodando e acessível.
- Defina a variável de ambiente GEOCHAIN_CONTRACT_ADDRESS com o endereço do contrato implantado.
- Verifique se o arquivo blockchain/contracts/GeoChainTracker.json contém o ABI do contrato.

Para executar:
```bash
pytest tests/test_blockchain.py
```

### Teste do Frontend
Para executar o teste do frontend, certifique-se de que o Selenium WebDriver está instalado e configurado, e execute:
```bash
pytest tests/test_frontend.py
```

### Considerações
Garanta que todas as dependências estejam instaladas.
Configure corretamente as variáveis de ambiente necessárias para os testes do blockchain.
Para os testes do frontend, o caminho para o arquivo index.html foi configurado a partir da raiz do projeto; ajuste-o se a estrutura for alterada.

### Contribuição
Caso deseje adicionar ou modificar testes, siga as convenções existentes e atualize este documento conforme necessário.

---

### Conclusão

Esses testes fornecem uma base para validar cada parte da solução e a integração entre elas. Você poderá expandir os cenários conforme a evolução do projeto, oferecendo:
- Uma verificação unitária e funcional do backend.
- Um teste para garantir que o smart contract esteja acessível e operante.
- Um teste para que o frontend seja carregado corretamente.
- Um teste de integração que cobre os pontos principais da solução.
