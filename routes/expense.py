from fastapi import APIRouter
from config.db import conn
from models.expense import expenses
from schemas.expense import Expense

expense = APIRouter()


@expense.get("/expenses/{id}", tags=["Expense"])
async def get_expense_by_id(id: int):
    result = conn.execute(expenses.select().where(expenses.c.id == id)).first()
    return result


@expense.get("/expenses/user/{user_id}", tags=["Expense"])
async def get_expenses_by_user(user_id: str):
    results = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == user_id)
        .order_by(expenses.c.id.desc())
        .limit(5)
    ).fetchall()
    return results


@expense.get("/expense/user/{user_id}", tags=["Expense"])
async def get_expense_last_by_user(user_id: str):
    result = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == user_id)
        .order_by(expenses.c.id.desc())
        .limit(1)
    ).fetchone()
    return result


@expense.post("/expenses", tags=["Expense"])
async def save_expense(register: Expense):
    new_register = {
        "user_id": register.user_id,
        "expense_date": register.expense_date,
        "value": register.value,
    }

    add_register = conn.execute(expenses.insert().values(new_register))
    result = conn.execute(
        expenses.select().where(
            expenses.c.user_id == register.user_id,
            expenses.c.id == add_register.lastrowid,
        )
    ).first()
    return result


@expense.delete("/expenses/user/{user_id}/{id}", tags=["Expense"])
async def delete_expense(user_id: str, id: int):
    remove = conn.execute(
        expenses.delete().where(expenses.c.user_id == user_id, expenses.c.id == id)
    )
    return f"Se eliminó el registro del usuario con id {user_id}"
