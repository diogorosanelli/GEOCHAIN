// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title GeoChainTracker
 * @dev Contrato para registrar eventos de rastreabilidade de commodities agrícolas.
 * Cada evento é associado a um lote (lotId) e contém informações como timestamp,
 * tipo do evento, identificador geográfico (geoHash) e detalhes adicionais.
 */
contract GeoChainTracker {
    // Estrutura que define um evento
    struct Event {
        uint256 timestamp;   // Data/hora do evento (em Unix timestamp)
        string eventType;    // Tipo de evento (ex.: "plantio", "colheita", "transporte")
        string geoHash;      // Identificador ou hash da localização geoespacial
        string details;      // Detalhes adicionais do evento
    }

    // Mapeamento para associar um lote (lotId) a um array de eventos
    mapping(uint256 => Event[]) private lotEvents;

    // Evento emitido quando um novo evento é registrado
    event EventRegistered(
        uint256 indexed lotId,
        uint256 timestamp,
        string eventType,
        string geoHash,
        string details
    );

    /**
     * @notice Registra um novo evento para um lote específico.
     * @param lotId Identificador do lote.
     * @param eventType Tipo do evento.
     * @param geoHash Identificador da localização geográfica.
     * @param details Informações adicionais sobre o evento.
     */
    function registerEvent(
        uint256 lotId, 
        string memory eventType, 
        string memory geoHash, 
        string memory details
    ) public {
        // Cria o novo evento com o timestamp atual
        Event memory newEvent = Event({
            timestamp: block.timestamp,
            eventType: eventType,
            geoHash: geoHash,
            details: details
        });

        // Adiciona o evento ao array correspondente ao lote
        lotEvents[lotId].push(newEvent);

        // Emite o evento para registro na blockchain
        emit EventRegistered(lotId, block.timestamp, eventType, geoHash, details);
    }

    /**
     * @notice Recupera os eventos registrados para um lote.
     * @param lotId Identificador do lote.
     * @return Um array de eventos associados ao lote.
     */
    function getEvents(uint256 lotId) public view returns (Event[] memory) {
        return lotEvents[lotId];
    }
}
