# app.py
from flask import Flask, request, jsonify

import config
from services.arcgis import get_geographic_data
from services.blockchain import register_event_on_blockchain, get_events_from_blockchain

app = Flask(__name__)

@app.route('/')
def index():
    return "GeoChain Backend is Running!"

@app.route('/register_event', methods=['POST'])
def register_event():
    """
    Endpoint para registrar um novo evento.
    Espera um JSON com os seguintes parâmetros:
      - lotId: Identificador do lote
      - eventType: Tipo de evento (ex.: plantio, colheita, transporte)
      - details: Informações adicionais sobre o evento
    O backend consulta o ArcGIS Online para complementar com os dados geográficos.
    """
    data = request.get_json()
    lot_id = data.get('lotId')
    event_type = data.get('eventType')
    details = data.get('details')

    # Obter dados geográficos a partir do ArcGIS Online
    geo_data = get_geographic_data(lot_id)
    # Supondo que geo_data contenha um identificador único "geoHash"
    geo_hash = geo_data.get("geoHash", "NA")

    # Registrar evento na blockchain
    tx_receipt = register_event_on_blockchain(lot_id, event_type, geo_hash, details)
    response = {
        "message": "Evento registrado com sucesso!",
        "transaction": tx_receipt
    }
    return jsonify(response), 201

@app.route('/get_events/<int:lot_id>', methods=['GET'])
def get_events(lot_id):
    """
    Endpoint para obter os eventos registrados para um determinado lote.
    """
    events = get_events_from_blockchain(lot_id)
    return jsonify(events), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT, debug=True)
