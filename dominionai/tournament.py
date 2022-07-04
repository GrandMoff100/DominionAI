import copy
import logging
import threading
import typing as t
from collections import defaultdict
from itertools import combinations
from queue import Queue

import numpy as np
from dominion import Card, Game, Player
from dominion.report import Report

LOGGER = logging.getLogger(__name__)


class PlayerRecord:
    def __init__(self) -> None:
        self.wins = 0
        self.total = 0
        self.score_quality = 0.0


class Tournament:
    def __init__(
        self,
        players: t.List[t.Type[Player]],
        kingdom: t.List[t.Type[Card]],
        number: int,
    ) -> None:
        self.players = players
        self.kingdom = kingdom
        self.number = number

    def player_rankings_per_game(self, report: Report) -> t.Dict[t.Type[Player], float]:
        all_scores = np.array(list(report.scores.values()))
        score_quality = (
            all_scores + np.median(all_scores) - np.mean(all_scores)
        ) / np.sum(all_scores)
        normalized_quality = score_quality - np.min(score_quality)
        if (high := np.max(normalized_quality)) > 0:
            normalized_quality /= high
        spread_score_quality = (
            2 * normalized_quality + all_scores / np.sum(all_scores) - 1
        )
        return {
            type(player): score
            for player, score in zip(report.scores.keys(), spread_score_quality)
        }

    def game_thread(
        self,
        score_board: t.Dict[t.Type[Player], PlayerRecord],
    ):
        pass

    def execute(self) -> t.Dict[t.Type[Player], PlayerRecord]:
        score_board: t.Dict[t.Type[Player], PlayerRecord] = defaultdict(PlayerRecord)
        queue: t.List[t.Type[Player]] = copy.copy(self.players)
        active_games: t.List[threading.Thread] = []
