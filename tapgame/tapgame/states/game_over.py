import json
from ..models.settings import Settings
from ..helpers import countdown_timer, to_iso8601
from .results import Results
from .state import State


class GameOver(State):
    """
    When Game is Over, wait few seconds.
    """

    name = "GAME OVER"

    def on_enter(self):
        player = dict(self.context.player)
        player['dt'] = to_iso8601(player['dt'])

        payload = {
            "name": self.name,
            "player": player,
        }
        
        self.context.mqtt_client.publish(
            Settings().screen_topic, json.dumps(payload, ensure_ascii=False)
        )

    def exec(self):
        countdown_timer(Settings().game_over_view_duration)
        self.context.state = Results(self.context)
