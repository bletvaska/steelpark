import datetime
import json
from time import sleep

from loguru import logger
import paho.mqtt.client as mqtt
from sqlmodel import Session

from ..helpers import datetime_serializer, get_db_engine, get_player_name, get_top_players
from ..models.settings import get_settings
from ..models.player import Player
from .state import State
from .inactive import Inactive
from .game_over import GameOver


class Play(State):
    name = "PLAY"

    def _publish(self):
        payload = {
            "name": self.name,
            "player": dict(self.context.player),
        }

        self.context.mqtt_client.publish(
            get_settings().screen_topic, 
            json.dumps(payload, ensure_ascii=False, default=datetime_serializer)
        )

    def _on_tap(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        # on tap only
        # no need to check - no other type of message
        # message = json.loads(msg.payload.decode("utf-8"))
        #   if message["name"] == "tap":
        self.context.player.score += 1
        self.idle = 0
        logger.debug(f"Score: {self.context.player.score}")
        self._publish()

    def on_enter(self, *args, **kwargs):
        super().on_enter(*args, **kwargs)
        
        self.countdown = get_settings().gameplay_duration
        self.idle = 0
        self.context.player = Player(name=get_player_name(), score=0, dt=datetime.datetime.now(datetime.UTC))
        self.top_players = get_top_players()

        self.context.mqtt_client.message_callback_add(f"{get_settings().keyboard_topic}/event", self._on_tap)
        self._publish()

    def exec(self):
        # game loop
        while self.countdown > 0 and self.idle < get_settings().idle_duration:
            self.countdown -= 1
            self.idle += 1
            logger.debug(f"{self.countdown} / {self.idle}")
            sleep(1)

        # change state
        if self.countdown == 0:
            self.context.state = GameOver(self.context)
        else:
            self.context.state = Inactive(self.context)

    def on_exit(self):
        if isinstance(self.context.state, GameOver):
            # save player to db
            with Session(get_db_engine()) as session:
                session.add(self.context.player)
                session.commit()
                session.refresh(self.context.player)

        self.context.mqtt_client.message_callback_remove(f"{get_settings().keyboard_topic}/event")
