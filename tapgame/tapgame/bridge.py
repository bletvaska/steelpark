#!/usr/bin/env python3

# from gpiozero import Button
import json
from signal import pause
import paho.mqtt.client as mqtt
from loguru import logger
from .models.settings import get_settings

INPUT_PIN = 4
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_press():
    print('signal')


def init_mqtt_client():
    global client
    settings = get_settings()

    client.username_pw_set(settings.user, settings.password)
    client.will_set(
        f"{settings.bridge_topic}/status",
        json.dumps({"status": "offline"}),
        retain=True,
    )
    # client.on_message = on_message
    return client


def main():
    global client

    init_mqtt_client()



    # button = Button(INPUT_PIN)
    # button.when_pressed = on_press

    pause()



if __name__ == '__main__':
    main()
