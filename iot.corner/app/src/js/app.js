// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.error(`onConnectionLost: ${responseObject.errorMessage}`);
    }

    // refresh browser
    location.reload();
}

function publishMessage(client, topic, payload, retain=false, qos=0) {
    const msg = JSON.stringify(payload);
    console.log(`sending payload ${msg} to ${topic}.`);

    const message = new Paho.MQTT.Message(msg);
    message.destinationName = `${mqtt.topicPrefix}/${topic}`;
    message.retained = retain;
    message.qos = qos;
    client.send(message);
}

function toggleSocket(client, socketId){
    publishMessage(client, `z2m/${socketId}/set`, {"state": "TOGGLE"} );
}

window.addEventListener("load", function (event) {
    // add onclick handlers
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

    // prepare last will topic message
    var lwt = new Paho.MQTT.Message('{"state": "offline"}');
    lwt.destinationName = `${mqtt.topicPrefix}/${mqtt.clientId}/state`;
    lwt.qos = 0;
    lwt.retained = false;

    // connect client
    client.connect({
        userName : mqtt.user,
        password : mqtt.password,
        useSSL: true,
        willMessage: lwt, 
        onSuccess: function () {
            console.log('Connected to MQTT');
            publishMessage(client, `${mqtt.clientId}/state`, {"state": "online"}, retain=false);
        },
    });
});
