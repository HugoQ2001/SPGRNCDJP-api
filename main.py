from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.expense import expense
from routes.pronostication import pronostication

tags_metadata = [
    {
        "name": "Expense",
        "description": "Operaciones para listar y guardar los gastos mesuales de cada usuario.",
    },
    {
        "name": "Pronostication",
        "description": "Operaciones para guardar los pronosticos de gastos mesuales.",
    },
]

app = FastAPI(
    title="Predicción de gastos mensuales API",
    version="1.0",
    summary="API para la predicción de gastos mesuales de usuarios que quieran mejorar su control del dinero basada en redes neuronales recurrentes",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expense)
app.include_router(pronostication)
