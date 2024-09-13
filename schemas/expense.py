from typing import Optional
from pydantic import BaseModel
from datetime import date


class Expense(BaseModel):
    id: Optional[int] = None
    user_id: str
    category: str
    expense_date: date
    expense_value: float
