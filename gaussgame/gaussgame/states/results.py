import json
import math
from time import sleep

from loguru import logger
from sqlmodel import Session, select
from sqlalchemy.sql.functions import rank
from sqlalchemy.sql import desc
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from scipy.stats import norm

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
            "chart": self._get_chart_data(),
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
        settings = self.context.settings

        # get scores of players, if there are some
        with Session(get_db_engine()) as session:
            df = pd.read_sql_query("SELECT score FROM player", session.get_bind().connect())
            scores = df['score'].dropna()

            if len(scores) == 0:
                return None
        
        # create bins for histogram
        counts, bin_edges = np.histogram(scores, bins=settings.gauss_bins)

        # Príprava Gaussovej krivky škálovanej na početnosť (50 points)
        x = np.linspace(min(scores), max(scores), 50)
        gauss_curve = norm.pdf(x, scores.mean(), scores.std())

        # Škálovanie krivky na početnosť (nie hustotu)
        bin_width = bin_edges[1] - bin_edges[0]
        gauss_curve_scaled = gauss_curve * len(scores) * bin_width

        # find index of the bin for player
        player_score_bin = None
        for i in range(len(bin_edges) - 1):
            if bin_edges[i] <= self.context.player.score <= bin_edges[i + 1]:
                player_score_bin = i
                break

        return {
            "labels": [f"{math.ceil(bin_edges[i])} - {math.floor(bin_edges[i + 1])}" for i in range(len(bin_edges) - 1)],
            "data": counts.tolist(),
            "playerScoreBin": player_score_bin,
            "gauss": {
                "x": [ int(value) for value in x ],
                "y": [ int(value) for value in gauss_curve_scaled ],
            }
        }
