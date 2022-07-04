import copy
import logging
import random
import typing as t

from dominion import Player
from dominion.cards import Card

from dominionai.strategies import Strategy
from dominionai.tournament import PlayerRecord, Tournament

LOGGER = logging.getLogger(__name__)


class DominionAI:
    def __init__(self, kingdom: t.List[t.Type[Card]]) -> None:
        self.kingdom = kingdom
        self.generations: t.List[Generation] = []

    def compile_strategy(self, buy_list: t.List[t.Type[Card]]) -> t.Type[Player]:
        return type(
            "AIPlayer",
            (Strategy,),
            {"buy_list": copy.copy(buy_list), "original_buy_list": buy_list},
        )

    def seed_buy_lists(
        self,
        *,
        length: int = 1000,
        count: int = 1,
    ) -> t.List[t.List[t.Type[Card]]]:
        return [
            [random.choice(self.kingdom) for _ in range(length)] for _ in range(count)
        ]

    def initial_generation(
        self,
        *,
        length: int = 1000,
        size: int = 1,
        **kwargs,
    ) -> "Generation":
        LOGGER.debug("Seeding Buy Lists")
        players = [
            self.compile_strategy(buy_list)
            for buy_list in self.seed_buy_lists(length=length, count=size)
        ]
        return Generation(players, self, **kwargs)


class Generation:
    def __init__(
        self,
        players: t.List[Player],
        host: DominionAI,
        number: int = 1,
    ) -> None:
        self.players = players
        self.host = host
        self.number = number

    def execute(self, *args, **kwargs) -> t.Dict[t.Type[Player], PlayerRecord]:
        LOGGER.debug("Simulating generation #%i", self.number)
        return Tournament(self.players, self.host.kingdom, self.number).execute(
            *args, **kwargs
        )

    def next_generation(self, *args, **kwargs):
        records = self.execute(*args, **kwargs)
        breakpoint
