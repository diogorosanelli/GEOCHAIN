const GeoChainTracker = artifacts.require("GeoChainTracker");

contract("GeoChainTracker", accounts => {
  const lotId = 1;
  const eventType = "plantio";
  const geoHash = "fakeGeoHash123";
  const details = "Plantio realizado com sucesso.";

  let instance;

  before(async () => {
    instance = await GeoChainTracker.deployed();
  });

  it("deve registrar um evento e emitir o evento EventRegistered", async () => {
    // Registra um evento utilizando a conta 0
    let tx = await instance.registerEvent(lotId, eventType, geoHash, details, { from: accounts[0] });

    // Verifica se o log do evento foi emitido corretamente
    assert.equal(tx.logs.length, 1, "Deve haver um log emitido");
    let log = tx.logs[0];
    assert.equal(log.event, "EventRegistered", "O nome do evento deve ser 'EventRegistered'");
    assert.equal(log.args.lotId.toNumber(), lotId, "lotId deve ser igual ao enviado");
    assert.equal(log.args.eventType, eventType, "eventType deve ser igual ao enviado");
    assert.equal(log.args.geoHash, geoHash, "geoHash deve ser igual ao enviado");
    assert.equal(log.args.details, details, "details devem ser iguais ao enviados");
  });

  it("deve retornar os eventos registrados para um lote específico", async () => {
    // Recupera os eventos do lote
    let events = await instance.getEvents(lotId);
    assert.isAtLeast(events.length, 1, "Deve haver pelo menos um evento registrado para o lote");

    // Valida os detalhes do primeiro evento registrado
    let event = events[0];
    assert.equal(event.eventType, eventType, "O tipo do evento deve ser igual ao esperado");
    assert.equal(event.geoHash, geoHash, "O geoHash deve ser igual ao esperado");
    assert.equal(event.details, details, "Os detalhes do evento devem ser iguais ao esperado");

    // Converte o timestamp para número (se não for um BigNumber)
    const timestampNumber = Number(event.timestamp);
    assert.isTrue(timestampNumber > 0, "O timestamp deve ser um valor válido");
  });
});
