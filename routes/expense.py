from fastapi import APIRouter
from config.db import conn
from models.expense import expenses
from schemas.expense import Expense

expense = APIRouter()

# Get all expenses
@expense.get("/expenses", tags=["Expense"])
async def get_all_expenses():
    result = conn.execute(expenses.select().order_by(expenses.c.expense_date.desc())).fetchall()
    return result

@expense.get("/expenses/user/{user_id}", tags=["Expense"])
async def get_expenses_by_user_id(user_id: str):
    # Consulta para seleccionar los gastos que coinciden con el user_id y ordenarlos por fecha descendente
    result = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == user_id)
        .order_by(expenses.c.expense_date.desc())  # Ordenar por fecha de gasto de forma descendente
    ).fetchall()
    
    # Si no se encuentran resultados, devuelve un mensaje apropiado
    if not result:
        return {"message": "No expenses found for this user"}
    
    return result

# Get expense by id_expense
@expense.get("/expenses/{id}", tags=["Expense"])
async def get_expense_by_id(id: int):
    result = conn.execute(expenses.select().where(expenses.c.id == id)).first()
    return result


# Get expenses limit 5 users by user_id
@expense.get("/expenses/limit/user/{user_id}", tags=["Expense"])
async def get_expenses_limit_by_user(user_id: str):
    results = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == user_id)
        .order_by(expenses.c.expense_date.desc())
        .limit(5)
    ).fetchall()
    return results


# Get last expenses by user_id
@expense.get("/expense/last/user/{user_id}", tags=["Expense"])
async def get_expense_last_by_user(user_id: str):
    result = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == user_id)
        .order_by(expenses.c.expense_date.desc())  # Ordenar por expenses_date en orden descendente
        .limit(1)
    ).fetchone()
    return result


# register expenses
@expense.post("/expenses", tags=["Expense"])
async def save_expense(register: Expense):
    new_register = {
        "user_id": register.user_id,
        "category": register.category,
        "expense_date": register.expense_date,
        "expense_value": register.expense_value,
    }

    add_register = conn.execute(expenses.insert().values(new_register))
    result = conn.execute(
        expenses.select().where(
            expenses.c.user_id == register.user_id,
            expenses.c.id == add_register.lastrowid,
        )
    ).first()
    return result


# delete expeses
@expense.delete("/expenses/delete/user/{user_id}/{id}", tags=["Expense"])
async def delete_expense(user_id: str, id: int):
    remove = conn.execute(
        expenses.delete().where(expenses.c.user_id == user_id, expenses.c.id == id)
    )
    return f"Se eliminó el registro del usuario con id {user_id}"
