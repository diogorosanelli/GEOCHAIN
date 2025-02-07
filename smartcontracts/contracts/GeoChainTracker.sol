// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title GeoChainTracker
 * @dev Contrato para registrar eventos de rastreabilidade de commodities agrícolas.
 * Cada evento é associado a um lote (globalid) e contém informações como timestamp,
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

    // Mapeamento para associar um lote (globalid) a um array de eventos
    mapping(uint256 => Event[]) private geoEvents;

    // Evento emitido quando um novo evento é registrado
    event EventRegistered(
        uint256 indexed globalid,
        uint256 timestamp,
        string eventType,
        string geoHash,
        string details
    );

    /**
     * @notice Registra um novo evento para um lote específico.
     * @param globalid Identificador do lote.
     * @param eventType Tipo do evento.
     * @param geoHash Identificador da localização geográfica.
     * @param details Informações adicionais sobre o evento.
     */
    function registerEvent(
        string memory globalid, 
        string memory eventType, 
        string memory geoHash, 
        string memory details
    ) public {
        // Convert lotId from GUID to uint256
        uint128 globalidUint = uint128(uint256(keccak256(abi.encodePacked(globalid))));

        // Cria o novo evento com o timestamp atual
        Event memory newEvent = Event({
            timestamp: block.timestamp,
            eventType: eventType,
            geoHash: geoHash,
            details: details
        });

        // Adiciona o evento ao array correspondente ao lote
        geoEvents[globalidUint].push(newEvent);

        // Emite o evento para registro na blockchain
        emit EventRegistered(globalidUint, block.timestamp, eventType, geoHash, details);
    }

    /**
     * @notice Recupera os eventos registrados para um lote.
     * @param globalid Identificador do lote.
     * @return Um array de eventos associados ao lote.
     */
    function getEvents(string memory globalid) public view returns (Event[] memory) {
        // Convert lotId from GUID to uint256
        uint128 globalidUint = uint128(uint256(keccak256(abi.encodePacked(globalid))));
        return geoEvents[globalidUint];
    }
}
