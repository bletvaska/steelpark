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
            # "player": dict(self.context.player),
            'player': {
                'name': self.player,
                'score': self.score,
                'dt': self.start.isoformat(),
            }
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
        self.score += 1
        self.idle = 0
        logger.debug(f"Score: {self.score}")
        self._publish()

    def on_enter(self, *args, **kwargs):
        super().on_enter(*args, **kwargs)
        
        self.countdown = get_settings().gameplay_duration
        self.idle = 0
        self.top_players = get_top_players()
        
        # create player 
        self.player = get_player_name()
        self.score = 0
        self.start = datetime.datetime.now(datetime.UTC)
        # self.context.player = Player(name=get_player_name(), score=0, dt=datetime.datetime.now(datetime.UTC))

        self._publish()
        self.context.mqtt_client.message_callback_add(f"{get_settings().keyboard_topic}/event", self._on_tap)

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
            player = Player(name=self.player, score=self.score, dt=self.start)
            # save player to db
            with Session(get_db_engine()) as session:
                session.add(player)
                session.commit()
                session.refresh(player)
                self.context.player = player

        self.context.mqtt_client.message_callback_remove(f"{get_settings().keyboard_topic}/event")
