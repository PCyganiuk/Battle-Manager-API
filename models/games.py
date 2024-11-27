from pydantic import BaseModel
from typing import Optional

class InitiativeItem(BaseModel):
    name:str
    initiative: int
    ai_enabled: bool

class Game(BaseModel):
    game_name: str
    owner_id: str
    dimension_x: int
    dimension_y: int
    current_turn: Optional[str]
    initiative_list: list[InitiativeItem]
    picture_id: Optional[str]
    player_list: list[str]
    is_fog: bool