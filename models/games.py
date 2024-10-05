from pydantic import BaseModel

class Game(BaseModel):
    owner_id: str