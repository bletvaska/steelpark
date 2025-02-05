from ..helpers import countdown_timer
from ..models.settings import Settings
from .state import State


class Inactive(State):
    name = "INACTIVE"

    def exec(self):
        """
        Shows the inactive screen for INACTIVE_VIEW_DURATION period.
        """

        countdown_timer(Settings().inactive_view_duration)
        from .start import Start
        self.context.state = Start(self.context)
