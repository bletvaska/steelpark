// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log(`onConnectionLost: ${responseObject.errorMessage}`);
    }
}

function publishMessage(client, topic, payload, retain=false, qos=0) {
    const msg = JSON.stringify(payload);
    console.log(`sending payload ${msg} to ${topic}.`);

    const message = new Paho.MQTT.Message(msg);
    message.destinationName = topic;
    message.retained = retain;
    message.qos = qos;
    client.send(message);
}

function toggleSocket(client, socketId){
    publishMessage(client, `zigbee2mqtt/${socketId}/set`, {"state": "TOGGLE"} );
}

window.addEventListener("load", function (event) {
    document.querySelectorAll(".socket").forEach(button => {
        button.addEventListener("click", function(event) {
            toggleSocket(client, event.target.id);
        });
    });



    // the main program

    // Create a MQTT client instance
    const client = new Paho.MQTT.Client(
        mqtt.broker,
        mqtt.port,
        "/mqtt",
        mqtt.clientId
    );

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    // client.onMessageArrived = onMessageArrived;

    // connect client
    client.connect({
        userName : mqtt.user,
        password : mqtt.password,
        useSSL: true,
        onSuccess: function () {
            console.log('Connected to MQTT');
            publishMessage(client, `${mqtt.topicPrefix}/${mqtt.clientId}/status`, 'online', retain=true);
        },
    });
});
