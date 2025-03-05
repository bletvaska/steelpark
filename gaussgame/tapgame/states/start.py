import json
from time import sleep

from loguru import logger
import paho.mqtt.client as mqtt

from ..models.settings import Settings
from .gauss import Gauss
from .state import State


class Start(State):
    name = "START"

    def _on_tap(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        logger.debug("TAP")
        self.context.state = Gauss(self.context)
        self.player = None

    def on_enter(self, *args, **kwargs):
        super().on_enter(*args, **kwargs)
        
        self.context.mqtt_client.message_callback_add(
            f'{Settings().keyboard_topic}/event', self._on_tap
        )

    def exec(self):
        # wait for tap to change the state
        while self.context.state == self:
            sleep(0.3)

    def on_exit(self):
        self.context.mqtt_client.message_callback_remove(f'{Settings().keyboard_topic}/event')
