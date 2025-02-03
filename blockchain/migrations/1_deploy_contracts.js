const GeoChainTracker = artifacts.require("GeoChainTracker");

module.exports = function (deployer) {
  deployer.deploy(GeoChainTracker);
};
