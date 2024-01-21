from abc import ABC, abstractmethod

from dealer_imitator.common.cards.card_generator import CardGenerator
from dealer_imitator.connections.async_redis_conn import r


class IDealerManager(ABC):
    @abstractmethod
    async def generate_new_card(game_id) -> str:
        """INTERFACE FOR GENERATING NEW CARD FOR THE PLAYERS"""


class DealerManager(IDealerManager):
    def __init__(self, game_id: str) -> None:
        self.game_id = game_id
        self.remaining_cards: list[str]
        self.new_card: str

    async def generate_new_card(self) -> str:
        self.remaining_cards = await r.get_remaining_cards_list(self.game_id)
        card_generator = CardGenerator(len(self.remaining_cards))
        new_card_index = card_generator.generate_card()
        self.new_card = self.remaining_cards[new_card_index]
        await r.remove_card_from_list(self.game_id, self.new_card)
        return self.new_card
