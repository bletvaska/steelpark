import json
from ..models.settings import Settings
from ..helpers import countdown_timer, datetime_serializer
from .results import Results
from .state import State


class GameOver(State):
    """
    When Game is Over, wait few seconds.
    """

    name = "GAME OVER"

    def on_enter(self):
        payload = {
            "name": self.name,
            "player": dict(self.context.player),
        }
        
        self.context.mqtt_client.publish(
            Settings().screen_topic, 
            json.dumps(payload, ensure_ascii=False, default=datetime_serializer)
        )

    def exec(self):
        countdown_timer(Settings().game_over_view_duration)
        self.context.state = Results(self.context)
