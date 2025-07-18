import json
import sys
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from loguru import logger
from pydantic import ValidationError


from .models.player import Player
from .models.settings import Settings
from .states.start import Start


class Context:
    def __init__(self):
        # prepare context variables
        self.state = Start(self)
        self.player: Player = None
        self.table = []
        try:
            self.settings = Settings()
        except ValidationError as ex:
            logger.critical("Invalid Settings")
            logger.error(ex)
            sys.exit(1)

        # prepare mqtt client
        self.mqtt_client = self._init_mqtt_client()

    def _on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        logger.warning(f'Ignoring message: {msg.topic}: {msg.payload}')


    def _init_mqtt_client(self):
        # init mqtt client
        parsed = urlparse(self.settings.mqtt_uri)
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="core")

        # Set TLS if the scheme is mqtts
        if parsed.scheme == "mqtts":
            client.tls_set()

        # Set username and password if provided
        if parsed.username and parsed.password:
            client.username_pw_set(parsed.username, parsed.password)

        client.will_set(
            f"{self.settings.backend_topic}/status",
            json.dumps({"status": "offline"}),
            retain=True,
        )
        client.on_message = self._on_message
        return client


    def run(self):
        logger.debug('Current Settings')
        logger.debug(dict(self.settings))
    
        parsed = urlparse(self.settings.mqtt_uri)
        logger.debug(parsed)

        try:
            logger.info(f"Connecting to MQTT broker {parsed.hostname}")
            self.mqtt_client.connect(parsed.hostname, parsed.port, 60)
            self.mqtt_client.publish(
                f"{self.settings.backend_topic}/status",
                json.dumps({"status": "online"}),
                retain=True,
            )
            self.mqtt_client.subscribe(f'{self.settings.keyboard_topic}/event')
            self.mqtt_client.loop_start()

            logger.info("Running main loop")

            while True:
                state = self.state
                
                # enter state
                logger.info(f"Entering State {state.name}.")
                state.on_enter()

                # run state
                state.exec()
                
                # leave state
                # logger.info(f"Leaving State {state.name}.")
                state.on_exit()

        except OSError as ex:
            logger.critical(f"Can't connect to the broker '{parsed.hostname}'")

        except Exception as ex:
            logger.error("Something went wrong")
            print(type(ex))
            print(ex)

        logger.info("Disconnecting from MQTT")
        self.mqtt_client.publish(
            f"{self.settings.backend_topic}/status",
            json.dumps({"status": "offline"}),
            retain=True,
        )
        self.mqtt_client.loop_stop()

        logger.info("Bye")
