from collections import defaultdict
from bson import ObjectId
from typing import Optional, List, Literal, DefaultDict

from pydantic import (
    BaseModel,
    AnyHttpUrl,
    Field,
    StrictStr,
    StrictBool,
    StrictInt,
    StrictFloat,
    validator,
)

from dealer_imitator.common.utils import generate_api_key, get_timestamp
from dealer_imitator.common.enums import BetTypes


class MongoModel(BaseModel):
    id: StrictStr = Field(default_factory=lambda: str(ObjectId()))

    @validator("id")
    @classmethod
    def check_id(cls, value):
        if len(value) != 24:
            raise ValueError("id should be a proper ObejctId (24 chars long)")
        return value


class GameModel(MongoModel):
    name: StrictStr
    front_stream: StrictStr
    top_stream: StrictStr
    audio_stream: StrictStr

    is_break: StrictBool = False
    is_open: StrictBool = False

    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)


class MerchantGameModel(BaseModel):
    game_id: str
    game_name: str
    min_bet: float
    max_bet: float
    bet_range: List[float]
    is_active: bool
    shoe_size: int


class MerchantModel(MongoModel):
    name: StrictStr
    api_key: Optional[str] = generate_api_key()

    games: List[MerchantGameModel] = []

    validate_token_url: AnyHttpUrl
    bet_url: AnyHttpUrl
    win_url: AnyHttpUrl
    rollback_url: AnyHttpUrl
    get_balance_url: AnyHttpUrl

    schema_type: Literal["decamelize", "camelize", "pascalize", "kebabize"]


class RoundModel(MongoModel):
    created_at: str = Field(default_factory=get_timestamp)
    updated_at: str = Field(default_factory=get_timestamp)

    game_id: StrictStr
    round_id_short: StrictStr

    player_cards: List[StrictStr] = []
    banker_cards: List[StrictStr] = []
    winner: Optional[str] = None

    starts_at: Optional[int] = None
    was_reset: StrictBool = False
    finished: StrictBool = False
    dealer_name: StrictStr = ""
    card_count: StrictInt = 0

    previous_round_id: Optional[StrictStr] = None

    cutting_card: StrictBool = False
    shuffling_ends_at: Optional[int] = None


class BetModel(BaseModel):
    bet_amount: float = 0
    bet_list: List[StrictFloat] = []


class PlayerModel(MongoModel):
    joined_game_at: str = Field(default_factory=get_timestamp)

    sid: StrictStr
    user_token: StrictStr
    user_id: str
    user_name: StrictStr
    player_id: StrictStr

    game_id: StrictStr
    round_id: StrictStr
    merchant_id: StrictStr
    bets: DefaultDict[str, BetModel] = defaultdict(BetModel)

    total_balance: float = 0
    winning_amount: float = 0
    total_bet: float = 0
    archived: bool = False
    is_reset: bool = False
    is_active: bool = True

    external_ids: dict = {}

    def max_main_bet(self):
        return max(
            [
                self.bets[BetTypes.PLAYER.value].bet_amount,
                self.bets[BetTypes.BANKER.value].bet_amount,
                self.bets[BetTypes.TIE.value].bet_amount,
            ]
        )

    def main_bets_are_placed(self):
        if any(main_bet_type in self.bets for main_bet_type in BetTypes.main_bets()):
            return True

    def highest_placed_sidebet(self):
        maximum_side_bet = 0
        for bet_type, bet in self.bets.items():
            if bet_type in BetTypes.side_bets() and bet.bet_amount > maximum_side_bet:
                maximum_side_bet = bet.bet_amount
        return maximum_side_bet

    def bet_exceeds_limit(self, bet_type, limit, placing_amount):
        if bet_type in BetTypes.lower_limit_bets():
            limit = limit / 10
        if self.bets[bet_type].bet_amount + placing_amount > limit:
            return True

    def less_than_lower_limit(self, bet_type, limit, placing_amount):
        if self.bets[bet_type].bet_amount + placing_amount < limit:
            return True

    def side_bet_exeeds_main_bet(self, bet_type, placing_amount):
        if bet_type in BetTypes.side_bets():
            if self.max_main_bet() < self.bets[bet_type].bet_amount + placing_amount:
                return True

    def main_bet_falls_behind_side_bet(self, bet_type, placing_amount):
        if bet_type in BetTypes.main_bets():
            decremented_amount = self.bets[bet_type].bet_amount - placing_amount
            remaining_two_bets = [
                bet for bet in BetTypes.main_bets() if bet != bet_type
            ]
            max_from_remaining_two = max(
                [self.bets[bet].bet_amount for bet in remaining_two_bets]
            )
            if (
                decremented_amount < self.highest_placed_sidebet()
                and max_from_remaining_two < self.highest_placed_sidebet()
            ):
                return True


class AuthResponseModel(BaseModel):
    token: StrictStr
    total_balance: StrictFloat
    currency: StrictStr
    user_name: StrictStr
    user_id: str
    status: StrictStr
