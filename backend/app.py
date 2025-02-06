# app.py
import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from services.arcgis import get_geographic_data
from services.blockchain import register_event_on_blockchain, get_events_from_blockchain

load_dotenv()
PORT = os.getenv("PORT", "5000")

app = Flask(__name__)

@app.route('/')
def index():
    return "GeoChain Backend is Running!"

@app.route('/api/event/register', methods=['POST'])
def register_event():
    """
    Endpoint para registrar um novo evento.
    Espera um JSON com os seguintes parâmetros:
      - globalid: Identificador do lote
      - eventType: Tipo de evento (ex.: plantio, colheita, transporte)
      - details: Informações adicionais sobre o evento
    O backend consulta o ArcGIS Online para complementar com os dados geográficos.
    """
    data = request.get_json()
    globalid = data.get('globalid')
    event_type = data.get('eventType')
    details = data.get('details')

    # Obter dados geográficos a partir do ArcGIS Online
    geo_data = get_geographic_data(globalid)
    # Supondo que geo_data contenha um identificador único "geoHash"
    geo_hash = geo_data.get("geohash", "NA")

    # Registrar evento na blockchain
    tx_receipt = register_event_on_blockchain(globalid, event_type, geo_hash, details)
    response = {
        "message": "Evento registrado com sucesso!",
        "transaction": tx_receipt
    }
    return jsonify(response), 201

@app.route('/api/event/list/<int:globalid>', methods=['GET'])
def get_events(globalid):
    """
    Endpoint para obter os eventos registrados para um determinado lote.
    """
    events = get_events_from_blockchain(globalid)
    return jsonify(events), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
