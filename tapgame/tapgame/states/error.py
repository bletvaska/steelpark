from ..helpers import countdown_timer
from ..models.settings import Settings
from .state import State


class Error(State):
    name = "ERROR"

    def exec(self):
        """
        Shows the error screen for ERROR_VIEW_DURATION period.
        """

        countdown_timer(Settings().error_view_duration)
        from .start import Start
        self.context.state = Start(self.context)
