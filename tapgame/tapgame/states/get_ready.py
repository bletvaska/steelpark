from ..helpers import countdown_timer
from .play import Play
from .state import State


class GetReady(State):
    name = "GET READY"

    def exec(self):
        countdown_timer(5)
        self.context.state = Play(self.context)
