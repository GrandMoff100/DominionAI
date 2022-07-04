import logging

from dominion.cards.expansions import first_edition as fe

from dominionai.base import DominionAI

logging.basicConfig(level=logging.DEBUG, filename="out.log", filemode="w")


kingdom = [
    fe.Cellar,
    fe.ThroneRoom,
    fe.Village,
    fe.Smithy,
    fe.Workshop,
    fe.Remodel,
    fe.Chapel,
    fe.Festival,
    fe.Market,
    fe.Feast,
]


ai = DominionAI(kingdom)


first = ai.initial_generation(size=10)


first.execute(workers=1)
