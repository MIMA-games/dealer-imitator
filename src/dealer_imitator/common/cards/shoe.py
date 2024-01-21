from typing import NamedTuple, Dict, Final, ClassVar


class Card(NamedTuple):
    card: str
    score: int
    suit: str

    def __lt__(self, other: "Card"):
        return self.score <= other.score


class Shoe:
    """
    Class for generating shoe depending on shoe_size parameter.
    """

    SUITS: Final = ["H", "D", "S", "C"]
    CARDS: Final = [
        "A",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "T",
        "J",
        "Q",
        "K",
    ]
    SCORES: Final = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 0,
        "J": 0,
        "Q": 0,
        "K": 0,
    }

    def __init__(self, shoe_size: int):
        self.shoe_size = shoe_size
        self._shoe: Dict[str, Card] = {}

    @staticmethod
    def setup(shoe_size: int) -> "Shoe":
        """
        This function is factory method which contracts Shoe class.
        """
        shoe = Shoe(shoe_size)
        shoe.generate_deck()
        return shoe

    @property
    def shoe(self):
        """
        returns dictionary with all the shoe cards.
        """
        return self._shoe

    def generate_deck(self) -> None:
        """
        function for generating shoe.
        """
        for deck_number in range(1, self.shoe_size + 1):
            for suit in self.SUITS:
                for card in self.CARDS:
                    self._shoe[str(deck_number) + card + suit] = Card(
                        card, self.SCORES[card], suit
                    )

    def __contains__(self, card: str) -> bool:
        return card in self._shoe

    def __getitem__(self, card: str) -> Card:
        return self._shoe[card]
