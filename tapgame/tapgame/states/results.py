import json
import math

import numpy as np
from sqlmodel import Session, select
from sqlalchemy.sql.functions import rank
from sqlalchemy.sql import desc

from ..helpers import countdown_timer, get_db_engine, get_top_players, to_iso8601
from ..models.settings import Settings
from ..models.player import Player
from .state import State


class Results(State):
    name = "RESULTS"

    def on_enter(self):
        player = dict(self.context.player)
        player['dt'] = to_iso8601(player['dt'])
        player['rank'] = self._get_rank_of_player(player['id'])

        payload = {
            "name": self.name,
            "player": player,
            "table": get_top_players(),
            "chart": self._get_chart_data()
        }
        
        self.context.mqtt_client.publish(
            Settings().screen_topic, json.dumps(payload, ensure_ascii=False)
        )


    def exec(self):
        """
        Shows the results for RESULTS_VIEW_DURATION period.
        """
        countdown_timer(Settings().results_view_duration)
        from .start import Start
        self.context.state = Start(self.context)


    def _get_rank_of_player(self, id):
        with Session(get_db_engine()) as session:
            stmt = select(Player.id, rank().over(order_by=desc(Player.score)).label('rank')).subquery()
            query = select(stmt.c.rank).where(stmt.c.id == id)
            return  session.exec(query).one()


    def _get_chart_data(self):
        # get scores of players
        with Session(get_db_engine()) as session:
            scores = session.exec(select(Player.score)).all()

        # are there any data?
        if not scores:
            return None
        
        # create 9 bins
        bins = np.linspace(min(scores), max(scores), 9)

        # create histogram
        hist_values, bin_edges = np.histogram(scores, bins=bins)

        # find index of the bin for player
        player_score_bin = None
        labels = []
        for i in range(len(bin_edges) - 1):
            labels.append(f"{math.ceil(bin_edges[i])} - {math.floor(bin_edges[i+1])}")
            if bin_edges[i] <= self.context.player.score <= bin_edges[i+1]:
                player_score_bin = i

        return {
            'labels': [f"{math.ceil(bin_edges[i])} - {math.floor(bin_edges[i+1])}" for i in range(len(bin_edges) - 1)],
            'data': list(map(int, hist_values)),
            'playerScoreBin': player_score_bin
        }
