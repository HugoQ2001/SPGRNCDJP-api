from typing import Optional
from pydantic import BaseModel
from datetime import date


class Pronostication(BaseModel):
    id: Optional[int] = None
    user_id: str
