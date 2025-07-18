#!/usr/bin/env python3

import json
from time import sleep
from signal import pause
from urllib.parse import urlparse

from gpiozero import Button
import paho.mqtt.client as mqtt
from loguru import logger

from .models.settings import get_settings


# INPUT_PIN = 4
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="bridge")
settings = get_settings()


def on_press():
    logger.info("TAP")
    client.publish(f"{settings.keyboard_topic}/event", json.dumps({"name": "tap"}))


def init_mqtt_client():
    parsed = urlparse(settings.mqtt_uri)
    logger.info(f"Connecting to MQTT Broker {parsed.hostname}...")

    # Set TLS if the scheme is mqtts
    if parsed.scheme == "mqtts":
        client.tls_set()

    # Set username and password if provided
    if parsed.username and parsed.password:
        client.username_pw_set(parsed.username, parsed.password)

    client.will_set(
        f"{settings.bridge_topic}/status",
        json.dumps({"status": "offline"}),
        retain=True,
    )
    return client


def main():
    parsed = urlparse(settings.mqtt_uri)
    logger.info('Initializing')
    init_mqtt_client()

    button = Button(settings.input_pin)
    button.when_pressed = on_press

    client.connect(parsed.hostname, parsed.port, 60)
    client.publish(
        f"{settings.bridge_topic}/status",
        json.dumps({"status": "online"}),
        retain=True,
    )
    client.loop_start()


    logger.info('Waiting for events...')
    pause()

    logger.info("Going down...")

    client.publish(
        f"{settings.bridge_topic}/status",
        json.dumps({"status": "offline"}),
        retain=True,
    )

    client.loop_stop()
    sleep(0.1)
    client.disconnect()

    logger.info("Bye")


if __name__ == "__main__":
    main()
    