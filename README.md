# GeoChain - Rastreabilidade de Commodities Agrícolas

GeoChain é uma solução inovadora que integra dados geoespaciais obtidos via ArcGIS Online com a segurança e imutabilidade dos registros blockchain na rede Ethereum. Essa plataforma permite rastrear e auditar toda a cadeia de suprimentos de commodities agrícolas, promovendo transparência e confiabilidade para produtores, distribuidores e consumidores.

## Visão Geral

A solução GeoChain foi desenvolvida com os seguintes componentes:

- **Backend**: Desenvolvido em Python, integra dados geográficos do ArcGIS Online e interage com a rede Ethereum via smart contracts escritos em Solidity.
- **Blockchain (Smart Contracts)**: Implementados em Solidity, registram de forma imutável os eventos operacionais (ex.: plantio, colheita, transporte) na blockchain.
- **Frontend**: Aplicação web interativa desenvolvida com o ArcGIS SDK for JavaScript, que exibe mapas e informações dos eventos em tempo real.
- **Testes**: Scripts e documentação para testes unitários e de integração, garantindo a robustez da solução.

## Estrutura do Projeto

`GEOCHAIN/ 
├── README.md 
├── backend/ 
│ ├── app.py 
│ ├── arcgis_service.py 
│ ├── blockchain.py 
│ ├── config.py 
│ └── requirements.txt 
├── blockchain/ 
│ ├── contracts/ 
│ │ └── GeoChainTracker.sol 
│ ├── migrations/ 
│ │ └── deploy_contract.js 
│ └── tests/ 
│ └── test_GeoChainTracker.sol 
├── frontend/ 
│ ├── index.html 
│ ├── js/ 
│ │ └── app.js 
│ ├── css/ 
│ │ └── style.css 
│ └── assets/ 
│ ├── logo.png 
│ └── (outros arquivos gráficos) 
├── docs/ 
│ ├── architecture.md 
│ └── user_manual.md
└── tests/ 
    ├── test_backend.py 
    └── integration_tests.md`


## Requisitos

- **Node.js e NPM**: Para gerenciar dependências e executar scripts relacionados aos smart contracts e ao frontend.
- **Python 3.x**: Para o backend.
- **Truffle** (ou Hardhat): Para compilar, testar e fazer deploy dos smart contracts.
- **ArcGIS Online Account**: Para acessar os dados geoespaciais.
- **Conexão com a rede Ethereum**: Pode ser uma rede de testes (ex.: Rinkeby, Ropsten ou Ganache).

## Instalação

### Backend

1. Navegue até a pasta `backend/`:
    ```bash
    cd backend
    ```
2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure o arquivo `config.py` com suas variáveis (URLs, tokens, chaves, etc.).

### Blockchain (Smart Contracts)

1. Navegue até a pasta `blockchain/`:
    ```bash
    cd blockchain
    ```
2. Instale as dependências do Node.js:
    ```bash
    npm install
    ```
3. Compile os smart contracts utilizando o Truffle:
    ```bash
    truffle compile
    ```
4. Execute os testes dos smart contracts (opcional):
    ```bash
    truffle test
    ```
5. Faça o deploy na rede de testes:
    ```bash
    truffle migrate --network <nome_da_rede>
    ```

### Frontend

1. Navegue até a pasta `frontend/`:
    ```bash
    cd frontend
    ```
2. Abra o arquivo `index.html` em um navegador ou utilize um servidor web simples, por exemplo:
    ```bash
    http-server .
    ```
    *Você pode utilizar qualquer servidor de sua preferência.*

## Execução da Solução

1. **Inicie o Backend**:  
   Na pasta `backend/`, execute:
    ```bash
    python app.py
    ```
2. **Verifique o Deploy do Smart Contract**:  
   Certifique-se de que o contrato foi implantado e que o endereço está configurado corretamente no `config.py`.
3. **Acesse a Aplicação Web**:  
   Abra o `index.html` via navegador. O frontend exibirá o mapa interativo com os eventos registrados e a comunicação com o backend ocorrerá via APIs REST.

## Testes

- **Testes Unitários do Backend**:  
  Navegue até a pasta raiz e execute os testes:
    ```bash
    pytest tests/test_backend.py
    ```
- **Testes de Integração**:  
  Consulte o documento `tests/integration_tests.md` para cenários detalhados e instruções de execução dos testes de integração.

## Contribuição

Contribuições são bem-vindas! Se você deseja ajudar a melhorar a solução GeoChain, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch com sua feature ou correção:
    ```bash
    git checkout -b feature/nome-da-sua-feature
    ```
3. Commit suas alterações:
    ```bash
    git commit -am 'Adiciona nova feature'
    ```
4. Faça push para a branch:
    ```bash
    git push origin feature/nome-da-sua-feature
    ```
5. Abra um Pull Request.

## Documentação

Para mais detalhes sobre a arquitetura e o uso da solução, consulte os arquivos na pasta `docs/`:

- **architecture.md**: Detalhamento técnico da arquitetura do sistema.
- **user_manual.md**: Guia do usuário para utilização da aplicação web.

## Contato

Em caso de dúvidas, sugestões ou problemas, entre em contato através de:

- **Email**: diogo.rosanelli@gmail.com
- **GitHub**: [https://github.com/diogorosanelli/GEOCHAIN](https://github.com/diogorosanelli/GEOCHAIN)

---

Sinta-se à vontade para ajustar qualquer seção de acordo com atualizações futuras no projeto. Bom trabalho com o GeoChain!
