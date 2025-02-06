// js/app.js

// Configuração do mapa utilizando o ArcGIS SDK for JavaScript
require([
  "esri/Map",
  "esri/views/MapView",
  "esri/layers/TileLayer",
  "esri/layers/FeatureLayer",
  "esri/widgets/Expand",
  "esri/widgets/Legend",
  "esri/widgets/LayerList"
], function(Map, MapView, TileLayer, FeatureLayer, Expand, Legend, LayerList) {

  const activeGUID = -1; // OID do evento ativo (-1 para nenhum evento ativo)
  const activeEvents = []; // Lista de eventos ativos

  // Criação do mapa base
  const map = new Map({
    basemap: "dark-gray-vector" // ou "streets", "satellite" conforme a necessidade
  });

  // Inicialização da visualização do mapa
  const view = new MapView({
    container: "mapContainer",
    map: map,
    center: [-45.9000, -23.2000], // Coordenadas centrais (exemplo: São Paulo)
    zoom: 11
  });

  // Camadas de feição: Dados de Referência
  const lyrSJCLimiteMunicipal = new FeatureLayer({
    title: "Limite Municipal",
    url: "https://saopaulo.img.com.br/innovaserver/rest/services/Hosted/SJC/FeatureServer/7",
    outFields: ["*"],
    opacity: 0.75,
    visible: true,
    popupEnabled: false
  });

  const lyrSJCImoveisCAR = new FeatureLayer({
    title: "Perímetro do Imóvel Rural",
    url: "https://saopaulo.img.com.br/innovaserver/rest/services/Hosted/SJC/FeatureServer/24",
    outFields: ["*"],
    opacity: 0.5,
    visible: true
  });

  map.addMany([lyrSJCImoveisCAR, lyrSJCLimiteMunicipal]);

  // Adiciona o widget LayerList (Tabela de Conteúdo)
  const layerList = new LayerList({
    view: view,
    listItemCreatedFunction: function(event) {
      // Aqui você pode personalizar os itens da lista se necessário
      const item = event.item;
      // Exemplo: se a camada tiver o título "Eventos Operacionais", adicionar uma ação
      if (item.layer.title === "Perímetro do Imóvel Rural") {
        item.panel = {
          content: "legend",
          open: true
        };
      }
    }
  });
  const tocExpand = new Expand({
    view: view,
    content: layerList,
    expandIconClass: "esri-icon-menu"
  });
  view.ui.add(tocExpand, "bottom-left");

  // Função para carregar detalhes do evento ao clicar em um marcador
  view.on("click", function(event) {
    view.hitTest(event).then(function(response) {
      const results = response.results;
      if (results.length) {
        const graphic = results.filter(result => result.graphic.layer === lyrSJCImoveisCAR)[0].graphic;
        activeGUID = graphic.attributes.globalid;
        // Exibir os detalhes do evento na sidebar
        document.getElementById("eventDetails").innerHTML = `
          <p><strong>Código do Imóvel:</strong> ${graphic.attributes.cod_imovel}</p>
          <p><strong>Situação CAR:</strong> ${(graphic.attributes.ind_status === 'AT') ? '<span style="background-color:#0F0;font-weight:bold;">ATIVO</span>' : (graphic.attributes.ind_status === 'PE') ? '<span style="background-color:#f88e02;font-weight:bold;">PENDENTE</span>' : (graphic.attributes.ind_status === 'SU') ? '<span style="background-color:#fc0000;font-weight:bold;">SUSPENSO</span>' : '<span style="background-color:#CCCCCC;font-weight:bold;">CANCELADO</span>'}</p>
          <hr>
          <p><strong>Tipo de Evento:</strong> ${(graphic.attributes.eventtype === undefined ? '-' : graphic.attributes.eventtype)}</p>
          <p><strong>Data/Hora:</strong> ${new Date(graphic.attributes.timestamp * 1000).toLocaleString()}</p>
          <p><strong>Detalhes:</strong> ${(graphic.attributes.details === undefined) ? '-' : graphic.attributes.details}</p>
          <p><strong>GeoHash:</strong> ${(graphic.attributes.geohash === undefined) ? '-' : graphic.attributes.geohash}</p>
        `;
      }
    });
  });

  // Função para consumir a API REST do backend e atualizar a camada de eventos
  // Exemplo de chamada com fetch (ajuste conforme a necessidade):
  async function fetchEvents() {
    try {
      const response = await fetch(`http://localhost:5000/api/event/list/${activeGUID}`);
      activeEvents = await response.json();
      // Aqui você pode atualizar a camada ou criar gráficos dinâmicos com os dados recebidos.
      console.log("Eventos do lote:", activeEvents);
    } catch (error) {
      console.error("Erro ao buscar eventos:", error);
    }
  }

  // Chamada periódica para atualizar os eventos
  setInterval(fetchEvents, 5 * 60 * 1000); // Atualiza a cada 60 segundos

});
