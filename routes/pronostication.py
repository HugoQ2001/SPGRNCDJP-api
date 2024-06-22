from fastapi import APIRouter
from config.db import conn
from models.pronostication import pronostications
from models.expense import expenses
from schemas.pronostication import Pronostication
from routes.prediction import predecir, model, scaler
from datetime import datetime

pronostication = APIRouter()


@pronostication.post("/pronostications", tags=["Pronostication"])
async def save_pronostication(register: Pronostication):

    datos = conn.execute(
        expenses.select()
        .where(expenses.c.user_id == register.user_id)
        .order_by(expenses.c.id.asc())
        .limit(5)
    ).fetchall()
    valores = [dato.value for dato in datos]
    print(valores)

    # x = [100, 120, 210, 300, 200]
    predecir_var = predecir(valores, model, scaler)
    new_register = {
        "user_id": register.user_id,
        "pronostication_date": datetime.now(),
        "value": predecir_var[0],
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
