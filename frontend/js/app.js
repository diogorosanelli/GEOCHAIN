// js/app.js

// Configuração do mapa utilizando o ArcGIS SDK for JavaScript
require([
  "esri/request",
  "esri/config",
  "esri/Map",
  "esri/views/MapView",
  "esri/layers/TileLayer",
  "esri/layers/FeatureLayer",
  "esri/widgets/Expand",
  "esri/widgets/Legend",
  "esri/widgets/LayerList"
], function(esriRequest, esriConfig, Map, MapView, TileLayer, FeatureLayer, Expand, Legend, LayerList) {

  // Configuração do CORS para permitir requisições ao backend
  esriConfig.request.corsEnabledServers.push("gisai.local");
  
  let activeGUID = -1; // OID do evento ativo (-1 para nenhum evento ativo)
  let activeGraphic = undefined; // Gráfico do evento ativo
  let activeEvents = []; // Lista de eventos ativos

  const carousel = document.getElementById('carousel');
  const prevButton = document.getElementById('prevButton');
  const nextButton = document.getElementById('nextButton');
  const cardWidth = 200; // Largura do card + margem

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
  view.on("click", async function(event) {
    view.hitTest(event).then(async function(response) {
      const results = response.results;
      if (results.length) {
        const filteredResults = results.filter(result => result.graphic.layer === lyrSJCImoveisCAR);
        if (filteredResults.length > 0) {
          const graphic = filteredResults[0].graphic;
          activeGUID = graphic.attributes.globalid.replace("{", "").replace("}", "");
          activeGraphic = graphic;
          console.log("Imóvel Ativo Selecionado:", activeGUID);
          constructEventDetails(graphic);
        } else {
          console.log("Nenhum imóvel selecionado.");
          document.getElementById("eventDetails").innerHTML = "<p>Nenhum imóvel selecionado.</p>";
        }
      }
    });
  });

  async function constructEventDetails(graphic) {
    // Criar área fixa para os atributos principais
    let eventDetailsHTML = `
      <div id="fixedAttributes">
        <p><strong>GeoHash:</strong> ${graphic.attributes.globalid}</p>
        <p><strong>Código do Imóvel:</strong> ${graphic.attributes.cod_imovel}</p>
        <p><strong>Situação CAR:</strong> 
            ${(graphic.attributes.ind_status === 'AT') ? '<span style="background-color:#0F0;font-weight:bold;">ATIVO</span>' : 
            (graphic.attributes.ind_status === 'PE') ? '<span style="background-color:#f88e02;font-weight:bold;">PENDENTE</span>' : 
            (graphic.attributes.ind_status === 'SU') ? '<span style="background-color:#fc0000;font-weight:bold;">SUSPENSO</span>' : 
            '<span style="background-color:#CCCCCC;font-weight:bold;">CANCELADO</span>'}
        </p>
    `;

    // Atualizar a camada de eventos com base no GUID do imóvel
    activeEvents = await fetchEvents();        
    if (activeEvents && activeEvents.length > 0) {
      eventDetailsHTML += `
          <p><strong>Nro. Eventos Registrados:</strong> ${activeEvents.length}</p>
        </div>
        <hr>
        <div id="carouselContainer">
          <button id="prevButton" class="navigationButtons"> ◀ </button>
          <div id="carousel">
      `;
      activeEvents.forEach(event => {
        eventDetailsHTML += `
            <div class="eventCard">
              <p><strong>Tipo de Evento:</strong> ${event.eventType || '-'}</p>
              <p><strong>Data/Hora:</strong> ${new Date(event.timestamp * 1000).toLocaleString()}</p>
              <p><strong>Detalhes:</strong> ${event.details || '-'}</p>
              <p><strong>GeoHash:</strong> ${event.geoHash || '-'}</p>
            </div>
        `;
        });
      eventDetailsHTML += `
          </div>
          <button id="nextButton" class="navigationButtons"> ▶ </button>
        </div>
      `;
    } else {
      eventDetailsHTML += `
          <p><strong>Nro. Eventos Registrados:</strong> 0</p>
        </div>
        <hr>
        <div id="carouselContainer">
          <div id="carousel">
            <div class="eventCard" style="text-align:center;">
              <p>Nenhum evento encontrado.</p>
            </div>
          </div>
        </div>
      `;
    }
    
    document.getElementById("eventDetails").innerHTML = eventDetailsHTML;

    // Adicionar funcionalidade de rolagem horizontal ao carrossel
    const carousel = document.getElementById("carousel");
    if (activeEvents && activeEvents.length > 0) {
      document.getElementById("prevButton").addEventListener("click", () => {
          carousel.scrollBy({ left: -200, behavior: "smooth" });
      });
      document.getElementById("nextButton").addEventListener("click", () => {
          carousel.scrollBy({ left: 200, behavior: "smooth" });
      });
    }
  }

  // Função para consumir a API REST do backend e atualizar a camada de eventos
  // Exemplo de chamada com fetch (ajuste conforme a necessidade):
  async function fetchEvents() {
    if(activeGUID==-1) return [];
    try {
      const response = await esriRequest(`http://gisai.local/geochain/api/event/list/${activeGUID}`, {
        responseType: "json",
        method: "get",
        mode: "no-cors"
      });
      activeEvents = response.data
      console.log("Eventos do lote:", activeEvents);
      // Aqui você pode atualizar a camada ou criar gráficos dinâmicos com os dados recebidos.
      return activeEvents;
    } catch (error) {
      console.error("Erro ao buscar eventos:", error);
      return [];
      // throw new Error("Erro ao buscar eventos: " + error.message);
    }
  }

  setInterval(() => { if (activeGUID !== -1) constructEventDetails(activeGraphic); }, 1 * 60 * 1000); // Atualiza a cada 1 minuto
});
