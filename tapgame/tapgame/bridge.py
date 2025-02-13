#!/usr/bin/env python3

from gpiozero import Button
import json
from signal import pause
from time import sleep
import paho.mqtt.client as mqtt
from loguru import logger

from .models.settings import get_settings


INPUT_PIN = 4
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
settings = get_settings()


def on_press():
    logger.info("TAP")
    client.publish(f"{settings.keyboard_topic}/event", json.dumps({"name": "tap"}))


def init_mqtt_client():
    logger.info(f"Connecting to MQTT Broker {settings.broker}...")

    client.username_pw_set(settings.user, settings.password)
    client.will_set(
        f"{settings.bridge_topic}/status",
        json.dumps({"status": "offline"}),
        retain=True,
    )
    return client


def main():
    logger.info('Initializing')
    init_mqtt_client()

    button = Button(INPUT_PIN)
    button.when_pressed = on_press

    client.connect(settings.broker, settings.port, 60)
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