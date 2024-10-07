from pydantic import BaseModel
from typing import Optional

class Pawn(BaseModel):
    pawn_name: str
    pos_x: int
    pos_y: int
    dimension_x: int
    dimension_y: int
    hit_points: int
    initiative: Optional[int]
    attack_bonus: Optional[int]
    damage_bonus: Optional[int]
    armor_class: Optional[int]
    strength: Optional[int]
    dexterity: Optional[int]
    constitution: Optional[int]
    intelligence: Optional[int]
    wisdom: Optional[int]
    charisma: Optional[int]
    speed: Optional[int]
    game_id: str
    picture_id: Optional[str]
    ai_enabled: bool
    player_character: Optional[str]

class PawnCords(BaseModel):
    pos_x: int
    pos_y: int