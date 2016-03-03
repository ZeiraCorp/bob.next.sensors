var config = require('./app.config');
var mqtt = require('mqtt');

var mqttClientId = "CyclOps"
  , mqttBrokerConnectionString = "mqtt://"+config().mqttBroker+":"+config().mqttPort+"?clientId=" + mqttClientId;

var client = mqtt.connect(mqttBrokerConnectionString);

client.on("connect", function(){
  client.publish('news', JSON.stringify({
    message: "Yo! It's CyclOps, I'm ready"
  }));

});