from pydantic import BaseModel


class ScanCardModel(BaseModel):
    card: str
    round_id: str
