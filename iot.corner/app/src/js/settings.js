function generateHash(length = 5) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let hash = '';
    for (let i = 0; i < length; i++) {
        hash += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return hash;
}

// mqtt properties
const mqtt = {
    user: "maker",
    password: "Kulturpark13",
    broker: "78a616db237848caafd6d609ef8f627a.s1.eu.hivemq.cloud",
    // broker: window.location.host,
    // port: 8000,
    port: 8884,
    topicPrefix: "kulturpark/iotcorner",
    // clientId: "control_panel",
    clientId: `control_panel_${generateHash()}`,
};
