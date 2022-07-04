import random
import typing as t

from dominion import Card, Player


class Strategy(Player):
    buy_list: t.List[t.Type[Card]]
    original_buy_list: t.List[t.Type[Card]]

    def buy_phase(self) -> None:
        for i, card in enumerate(self.buy_list):
            if self.deck.buys >= 1:
                if (
                    card.cost <= self.deck.coins
                    and card in self.deck.game.available_cards
                ):
                    self.buy_list.pop(i).buy(self.deck)
            else:
                break

    def action_phase(self) -> None:
        pass

    def choice(
        self, card: t.Optional[t.Type[Card]], prompt: str, choices: t.List[t.Any]
    ) -> t.Any:
        return random.choice(choices)
