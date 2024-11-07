from pydantic import BaseModel

class Obstacle(BaseModel):
    pos_x: float
    pos_y: float
    width: int
    height: int
    game_id: str
    color: int

class ObstacleCords(BaseModel):
    pos_x: float
    pos_y: float