from fastapi import APIRouter
from config.db import conn
from models.pronostication import pronostications
from models.expense import expenses
from schemas.pronostication import Pronostication
from datetime import datetime
from modelornn.modelredneuronal import predecirgasto
import numpy as np
import httpx

pronostication = APIRouter()


@pronostication.get("/pronostications", tags=["Pronostication"])
async def get_all_pronostications():
    result = conn.execute(pronostications.select()).fetchall()
    return result


@pronostication.post("/pronostications", tags=["Pronostication"])
async def save_pronostication(register: Pronostication):

    datos = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == register.user_id)
        .order_by(expenses.c.id.desc())
        .limit(5)
    ).fetchall()

    valores = [dato.expense_value for dato in datos]
    print(valores)

    valores_2d = np.array(valores).reshape(1, -1)

    prediccion = predecirgasto(valores_2d)
    print(prediccion)

    new_register = {
        "user_id": register.user_id,
        "pronostication_date": datetime.now(),
        "pronostication_value": prediccion,
    }

    add_register = conn.execute(pronostications.insert().values(new_register))
    result = conn.execute(
        pronostications.select().where(
            pronostications.c.user_id == register.user_id,
            pronostications.c.id == add_register.lastrowid,
        )
    ).first()
    return result


@pronostication.get("/pronostications/user/{user_id}", tags=["Pronostication"])
async def get_pronostication_by_user(user_id: str):

    result = conn.execute(
        pronostications.select()
        .where(pronostications.c.user_id == user_id)
        .order_by(pronostications.c.id.desc())
        .limit(1)
    ).fetchone()
    return result
