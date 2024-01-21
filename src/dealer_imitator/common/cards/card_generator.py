import subprocess

from abc import ABC, abstractmethod
from typing import Optional


class ICardGenerator(ABC):
    @abstractmethod
    def generate_card(self) -> Optional[int]:
        """ INTERFACE FOR GENERATING CARD INDEX FROM REMAINING CARDS """
    
    @abstractmethod
    def _is_valid_operation(self) -> bool:
        """ INTERFACE FOR CHECKING WHETHER OPERATION IS VALID OR NOT """


class CardGenerator(ICardGenerator):
    def __init__(self, remaining_cards: int) -> None:
        """
        remaining_cards: int -> it is a number of remaining cards in the deck(s)
        """
        self.remaining_cards = remaining_cards
        self.file_name = "rand.sh"
    
    def generate_card(self) -> Optional[int]:
        if not self._is_valid_operation():
            return None
        script_arguments = ["1", str(self.remaining_cards), "1"]
        result = subprocess.run(["bash", self.file_name] + script_arguments, capture_output=True, text=True, check=True)
        error_output = result.stderr

        if not error_output:
            output = result.stdout
            card = int(output.strip())
            self.remaining_cards -= 1
            return card
        return None
    
    def _is_valid_operation(self):
        if self.remaining_cards <= 0:
            return False
        return True
