from ..models.settings import Settings
from ..helpers import countdown_timer
from .results import Results
from .state import State


class GameOver(State):
    """
    When Game is Over, wait few seconds.
    """

    name = "GAME OVER"

    def exec(self):
        countdown_timer(Settings().game_over_view_duration)
        self.context.state = Results(self.context)
