#!/usr/bin/env python3

import json
import socket
import time
from urllib.parse import urlparse

from loguru import logger
import paho.mqtt.client as mqtt

from .models import get_settings, Settings


def on_connect(client: mqtt.Client, userdata, flags, reason_code, properties):
    logger.debug(f"Connected with result code {reason_code}")


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    logger.debug(f'{msg.topic}: {msg.payload}')


def on_cmd_received(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    logger.info('Command Received')
    payload = json.loads(msg.payload)
    logger.debug(f'{msg.topic}: {payload}')

    if 'name' not in payload:
        return

    cmd = payload['name'].lower()
    if cmd == 'change_channel':
        channel = payload['channel']
        logger.info(f'Switching channel to {channel}')
        send_cmd(f'goto {10 + channel}')

    elif cmd == 'turn_off':
        logger.info('Turn Off')
        send_cmd('goto 1')

    elif cmd == 'turn_on':
        logger.info('Turn On')
        send_cmd('goto 11')

    else:
        logger.warning(f'Unknown command: {cmd}')


def send_cmd(cmd: str):
    try:
        settings = get_settings()
        with socket.create_connection((settings.vlc_host, settings.vlc_port), timeout=0.5) as sock:
            sock.sendall(f"{cmd}\n".encode())
    except ConnectionRefusedError as ex:
        logger.error(f"Can't connect to VLC on {settings.vlc_host}:{settings.vlc_port}")


def wait_for_vlc(settings: Settings):
    logger.info(f"Waiting for VLC at {settings.vlc_host}:{settings.vlc_port}...")

    while True:
        try:
            with socket.create_connection((settings.vlc_host, settings.vlc_port), timeout=0.5):
                logger.info("VLC is running.")
                return
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(3)


def main():
    settings = get_settings()

    # Connect to VLC
    wait_for_vlc(settings)
    send_cmd('goto 11')

    # init mqtt client
    parsed = urlparse(settings.mqtt_uri)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Set TLS if the scheme is mqtts
    if parsed.scheme == "mqtts":
        client.tls_set()

    # Set username and password if provided
    if parsed.username and parsed.password:
        client.username_pw_set(parsed.username, parsed.password)

    client.will_set(
            f'{settings.base_topic}/status', 
            json.dumps({'status': 'offline'}), 
            retain=True
    )

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(parsed.hostname, parsed.port, 60)
        client.publish(
                f'{settings.base_topic}/status', 
                json.dumps({'status': 'online'}), 
                retain=True
        )
        client.message_callback_add(f'{settings.base_topic}/cmd', on_cmd_received)

        client.subscribe(f'{settings.base_topic}/cmd')

        logger.info('Waiting for messages.')
        client.loop_forever()
    except OSError as ex:
        logger.critical("Can't connect to broker.")
        logger.exception(ex)


if __name__ == '__main__':
    main()

