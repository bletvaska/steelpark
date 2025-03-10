from abc import ABC, abstractmethod
import json
from typing import TYPE_CHECKING

from ..models.settings import Settings

if TYPE_CHECKING:
    from ..context import Context


class State(ABC):
    name: str
    
    def __init__(self, context, *args, **kwargs):
        self.context: "Context" = context

    def on_enter(self) -> None:
        payload = json.dumps({"name": self.name})
        self.context.mqtt_client.publish(Settings().screen_topic, payload)

    @abstractmethod
    def exec(self) -> None:
        pass

    def on_exit(self) -> None:
        pass
