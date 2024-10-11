from pydantic import BaseModel

class Picture(BaseModel):
    game_id: str
    picture_content: str