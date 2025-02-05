import json
from time import sleep
from loguru import logger
import paho.mqtt.client as mqtt

from .get_ready import GetReady
from ..models.settings import Settings
from .state import State


class Rules(State):
    name = "RULES-1"

    def _on_tap(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        """
        Change the rule pages on tap.
        """
        logger.debug("TAP")

        self.idle = 0
        self.part += 1
        if self.part > 3:
            self.context.state = GetReady(self.context)
            return

        payload = json.dumps({"name": f"RULES-{self.part}"})
        self.context.mqtt_client.publish(Settings().screen_topic, payload)

    def on_enter(self, *args, **kwargs):
        super().on_enter(*args, **kwargs)
        
        self.context.mqtt_client.message_callback_add(f"{Settings().keyboard_topic}/event", self._on_tap)
        self.part = 1
        self.idle = 0

    def exec(self):
        """
        Waits until the state change.

        If player will not tap within IDLE_DURATION time interval, screen will change to INACTIVE.
        """

        duration = 0.3
        while self.context.state == self:
            sleep(duration)
            self.idle += duration
            if self.idle >= Settings().idle_duration:
                from .start import Start
                self.context.state = Start(self.context)

    def on_exit(self):
        self.context.mqtt_client.message_callback_remove(f"{Settings().keyboard_topic}/event")
