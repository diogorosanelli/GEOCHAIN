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
    visible: true
  });

  const lyrSJCImoveisCAR = new FeatureLayer({
    title: "Perímetro do Imóvel Rural",
    url: "https://saopaulo.img.com.br/innovaserver/rest/services/Hosted/SJC/FeatureServer/24",
    outFields: ["*"],
    opacity: 0.5,
    visible: true
  });

  map.addMany([lyrSJCImoveisCAR, lyrSJCLimiteMunicipal]);

  // Exemplo: Adicionando uma camada de eventos (pode ser uma FeatureLayer que consome dados do backend)
  // const eventsLayer = new FeatureLayer({
  //   url: "https://<seu-backend-url>/arcgis/rest/services/EventLayer/FeatureServer/0",
  //   outFields: ["*"],
  //   popupTemplate: {  // Configuração do pop-up para exibir detalhes do evento
  //     title: "Evento: {eventType}",
  //     content: [
  //       {
  //         type: "fields",
  //         fieldInfos: [
  //           { fieldName: "timestamp", label: "Data/Hora" },
  //           { fieldName: "geoHash", label: "Localização" },
  //           { fieldName: "details", label: "Detalhes" }
  //         ]
  //       }
  //     ]
  //   }
  // });

  // Adiciona a camada ao mapa
  // map.add(eventsLayer);

  // Adiciona um widget de legenda
  // const legend = new Legend({
  //   view: view
  // });
  // const legendExpand = new Expand({
  //   view: view,
  //   content: legend
  // });
  // view.ui.add(legendExpand, "bottom-left");

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
      console.log(results)
      if (results.length) {
        const graphic = results.filter(result => result.graphic.layer === lyrSJCImoveisCAR)[0].graphic;
        // Exibir os detalhes do evento na sidebar
        document.getElementById("eventDetails").innerHTML = `
          <p><strong>Código Imóvel:</strong> ${graphic.attributes.cod_imovel}</p>
          <p><strong>Status:</strong> ${(graphic.attributes.ind_status === 'AT') ? '<span style="background-color:#0F0;font-weight:bold;">ATIVO</span>' : (graphic.attributes.ind_status === 'PE') ? '<span style="background-color:#f88e02;font-weight:bold;">PENDENTE</span>' : (graphic.attributes.ind_status === 'SU') ? '<span style="background-color:#fc0000;font-weight:bold;">SUSPENSO</span>' : '<span style="background-color:#CCCCCC;font-weight:bold;">CANCELADO</span>'}</p>
          <p><strong>Tipo:</strong> ${(graphic.attributes.eventType === undefined ? '-' : graphic.attributes.eventType)}</p>
          <p><strong>Data/Hora:</strong> ${new Date(graphic.attributes.timestamp * 1000).toLocaleString()}</p>
          <p><strong>Localização (GeoHash):</strong> ${(graphic.attributes.geoHash === undefined) ? '-' : graphic.attributes.geoHash}</p>
          <p><strong>Detalhes:</strong> ${(graphic.attributes.details === undefined) ? '-' : graphic.attributes.details}</p>
        `;
      }
    });
  });

  // Função para consumir a API REST do backend e atualizar a camada de eventos
  // Exemplo de chamada com fetch (ajuste conforme a necessidade):
  async function fetchEvents() {
    try {
      const response = await fetch("https://<seu-backend-url>/get_events/1");
      const data = await response.json();
      // Aqui você pode atualizar a camada ou criar gráficos dinâmicos com os dados recebidos.
      console.log("Eventos do lote:", data);
    } catch (error) {
      console.error("Erro ao buscar eventos:", error);
    }
  }

  // Chamada periódica para atualizar os eventos
  setInterval(fetchEvents, 60000); // Atualiza a cada 60 segundos

});
