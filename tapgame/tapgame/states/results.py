import json
import math
from time import sleep

from loguru import logger
from sqlmodel import Session, select
from sqlalchemy.sql.functions import rank
from sqlalchemy.sql import desc
import paho.mqtt.client as mqtt

from ..helpers import datetime_serializer, get_db_engine, get_top_players
from ..models.settings import get_settings
from ..models.player import Player
from .state import State


class Results(State):
    name = "RESULTS"

    def _on_tap(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        """
        Change the rule pages on tap.
        """
        logger.debug("TAP")
        from .start import Start
        self.context.state = Start(self.context)

    def on_enter(self):
        player = dict(self.context.player)
        player["rank"] = self._get_rank_of_player(player["id"])

        payload = {
            "name": self.name, 
            "player": player, 
            "table": get_top_players(), 
            "chart": self._get_chart_data()
        }

        self.context.mqtt_client.publish(
            get_settings().screen_topic, 
            json.dumps(payload, ensure_ascii=False, default=datetime_serializer)
        )

        self.context.mqtt_client.message_callback_add(f"{get_settings().keyboard_topic}/event", self._on_tap)

    def exec(self):
        """
        Shows the results for RESULTS_VIEW_DURATION period.
        """
        
        duration = 0.3
        idle = 0
        while self.context.state == self:
            sleep(duration)
            idle += duration
            if idle >= get_settings().results_view_duration:
                from .start import Start
                self.context.state = Start(self.context)

    def _get_rank_of_player(self, id):
        with Session(get_db_engine()) as session:
            stmt = select(Player.id, rank().over(order_by=desc(Player.score)).label("rank")).subquery()
            query = select(stmt.c.rank).where(stmt.c.id == id)
            return session.exec(query).one()

    def _get_chart_data(self):
        # get scores of players
        with Session(get_db_engine()) as session:
            scores = session.exec(select(Player.score)).all()

        # are there any data?
        if not scores:
            return None

        # create bins
        num_bins = get_settings().gauss_bins
        min_score, max_score = min(scores), max(scores)
        bin_width = (max_score - min_score) / num_bins
        bins = [min_score + i * bin_width for i in range(num_bins + 1)]

        # create histogram based on player score
        histogram = [0 for i in range(num_bins)]
        for score in scores:
            for i in range(num_bins):
                if bins[i] <= score < bins[i + 1]:  # Posledný interval zahŕňa max_score
                    histogram[i] += 1
                    break

        # find index of the bin for player
        player_score_bin = None
        labels = []
        for i in range(len(bins) - 1):
            labels.append(f"{math.ceil(bins[i])} - {math.floor(bins[i + 1])}")
            if bins[i] <= self.context.player.score <= bins[i + 1]:
                player_score_bin = i

        return {
            "labels": [f"{math.ceil(bins[i])} - {math.floor(bins[i + 1])}" for i in range(len(bins) - 1)],
            "data": histogram,
            "playerScoreBin": player_score_bin,
        }
