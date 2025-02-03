# Testes de Integração - GeoChain

## Objetivo
Validar o fluxo completo da solução GeoChain, garantindo que as integrações entre o backend, o serviço ArcGIS Online, a rede Ethereum e o frontend estejam funcionando corretamente.

## Cenário 1: Registro de Evento Completo

**Descrição:**  
Testar o endpoint `/register_event` para verificar se um evento é processado, complementado com dados geográficos e registrado na blockchain.

**Dados de Entrada:**  
- `lotId`: 1  
- `eventType`: "plantio"  
- `details`: "Plantio realizado com sucesso."

**Passos:**  
1. Enviar uma requisição POST para `/register_event` com os dados acima.
2. O backend consulta o ArcGIS Online para recuperar informações geográficas (geoHash).
3. O backend processa os dados e chama o smart contract para registrar o evento.
4. Uma resposta com o status da transação é retornada.

**Resultado Esperado:**  
- Código de status 201.  
- Resposta JSON contendo "Evento registrado com sucesso!" e dados da transação (txHash, status, blockNumber).

## Cenário 2: Consulta de Eventos

**Descrição:**  
Testar o endpoint `/get_events/<lot_id>` para verificar se os eventos registrados para um lote específico são retornados corretamente.

**Dados de Entrada:**  
- `lotId`: 1

**Passos:**  
1. Enviar uma requisição GET para `/get_events/1`.
2. O backend consulta o smart contract e retorna os eventos registrados.

**Resultado Esperado:**  
- Código de status 200.  
- Resposta JSON contendo uma lista de eventos com campos: timestamp, eventType, geoHash e details.

## Cenário 3: Fluxo Completo com Atualização em Tempo Real

**Descrição:**  
Validar o fluxo de integração entre o backend e o frontend, simulando uma atualização de eventos em tempo real.

**Passos:**  
1. Iniciar a aplicação backend e o frontend.
2. Realizar um registro de evento via API.
3. A página do frontend consome periodicamente a API `/get_events` e atualiza o mapa.
4. Verificar que o novo evento aparece no mapa e nos detalhes exibidos.

**Resultado Esperado:**  
- O evento registrado é visível no mapa interativo do frontend.  
- A sidebar atualiza com os detalhes do novo evento quando o usuário interage com o marcador.

## Conclusão

Estes testes de integração garantem que cada módulo do sistema GeoChain esteja corretamente integrado e que o fluxo de dados seja consistente e confiável. Caso ocorram discrepâncias, os logs do backend e as respostas dos endpoints deverão ser analisados para identificar e corrigir o problema.
