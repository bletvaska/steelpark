from time import sleep
from loguru import logger
import paho.mqtt.client as mqtt

from ..models.settings import Settings
from .rules import Rules
from .state import State


class Gauss(State):
    name = "GAUSS"

    def _on_tap(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        logger.debug("TAP")
        self.context.state = Rules(self.context)

    def on_enter(self, *args, **kwargs):
        super().on_enter(*args, **kwargs)
        
        self.context.mqtt_client.message_callback_add(f'{Settings().keyboard_topic}/event', self._on_tap)
        self.idle = 0

    def exec(self):
        # wait for tap to change the state
        duration = 0.3
        while self.context.state == self:
            sleep(duration)
            self.idle += duration
            if self.idle >= Settings().idle_duration:
                from .start import Start
                self.context.state = Start(self.context)

    def on_exit(self):
        self.context.mqtt_client.message_callback_remove(f'{Settings().keyboard_topic}/event')
