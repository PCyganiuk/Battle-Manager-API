from pydantic import BaseModel
from typing import Optional

class Picture(BaseModel):
    picture_id: str
    picture_content: str