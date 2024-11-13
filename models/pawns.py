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
    picture: Optional[str]
    ai_enabled: bool
    player_character: Optional[str]

class PawnCords(BaseModel):
    pos_x: int
    pos_y: int

class PawnInfo(BaseModel):
    dimension_x: Optional[int] = None
    dimension_y: Optional[int] = None
    hit_points: Optional[int] = None
    initiative: Optional[int] = None
    attack_bonus: Optional[int] = None
    damage_bonus: Optional[int] = None
    armor_class: Optional[int] = None
    strength: Optional[int] = None
    dexterity: Optional[int] = None
    constitution: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    charisma: Optional[int] = None
    speed: Optional[int] = None
    picture: Optional[str] = None
    player_character: Optional[str] = None

class PawnPicture(BaseModel):
    picture: str