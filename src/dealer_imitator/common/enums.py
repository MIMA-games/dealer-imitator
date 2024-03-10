from enum import Enum, StrEnum


class Games(StrEnum):
    BLACKJACK = "blackjack"
    CASINO_POKER = "casino_poker"
    BACCARAT = "baccarat"


class GameStates(Enum):

    CLOSED = "closed"
    PRECOUNTDOWN = "precountdown"
    BETTING = "betting"
    CLOSING_BETS = "closing_bets"
    DEALING = "dealing"
    ANNOUNCING = "announcing"
    SHUFFLING = "SHUFFLING"
    WAITING_DEALER_SCAN_DEALER_CARD = "waiting_dealer_scan_dealer_card"
    WAITING_DEALER_SCAN_PLAER_CARD = "waiting_dealer_scan_player_card"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class SendEvents(StrEnum):

    SCAN_CARD = "scan_card"
    DEALER_CARDS = "dealer_cards"
    ACTION_CARDS = "action_cards"


class ActionTypes(StrEnum):
    HIT = "hit"
    DOUBLE = "double"
    SPLIT = "split"
