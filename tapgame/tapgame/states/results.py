import json
import math

# import numpy as np
from sqlmodel import Session, select
from sqlalchemy.sql.functions import rank
from sqlalchemy.sql import desc

from ..helpers import countdown_timer, get_db_engine, get_top_players, to_iso8601
from ..models.settings import Settings
from ..models.player import Player
from .state import State


# def mean(values):
#     return sum(values) / len(values)

# def std_dev(values, mean_value):
#     variance = sum((x - mean_value) ** 2 for x in values) / len(values)
#     return math.sqrt(variance)

class Results(State):
    name = "RESULTS"

    def on_enter(self):
        player = dict(self.context.player)
        player["dt"] = to_iso8601(player["dt"])
        player["rank"] = self._get_rank_of_player(player["id"])

        payload = {"name": self.name, "player": player, "table": get_top_players(), "chart": self._get_chart_data()}

        self.context.mqtt_client.publish(Settings().screen_topic, json.dumps(payload, ensure_ascii=False))

    def exec(self):
        """
        Shows the results for RESULTS_VIEW_DURATION period.
        """
        countdown_timer(Settings().results_view_duration)
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

        # Vypočítať štatistiky
        # mean_score = mean(scores)
        # std_dev_score = std_dev(scores, mean_score)

        # create bins
        # bins = np.linspace(min(scores), max(scores), Settings().gauss_bins)
        num_bins = Settings().gauss_bins
        min_score, max_score = min(scores), max(scores)
        bin_width = (max_score - min_score) / num_bins
        bins = [min_score + i * bin_width for i in range(num_bins + 1)]

        # create histogram
        # hist_values, bin_edges = np.histogram(scores, bins=bins)
        histogram = {i: 0 for i in range(num_bins)}

        # Priradenie skóre hráčov do binov
        for score in scores:
            for i in range(num_bins):
                if bins[i] <= score < bins[i + 1]:  # Posledný interval zahŕňa max_score
                    histogram[i] += 1
                    break
        

        # x_values = [min_score + i * (max_score - min_score) / 100 for i in range(101)]
        # y_values = [len(scores) * bin_width * gaussian(x, mean_score, std_dev_score) for x in x_values]

        # find index of the bin for player
        player_score_bin = None
        labels = []
        for i in range(len(bins) - 1):
            labels.append(f"{math.ceil(bins[i])} - {math.floor(bins[i + 1])}")
            if bins[i] <= self.context.player.score <= bins[i + 1]:
                player_score_bin = i

        return {
            "labels": [
                f"{math.ceil(bins[i])} - {math.floor(bins[i + 1])}" for i in range(len(bins) - 1)
            ],
            "data": list(map(int, histogram)),
            "playerScoreBin": player_score_bin,
        }
