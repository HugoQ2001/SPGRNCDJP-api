from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float, Date
from config.db import meta, engine

pronostications = Table(
    "pronostications",
    meta,
    Column("id", Integer, primary_key=True),
    Column("user_id", String(200), nullable=False),
    Column("pronostication_date", Date, nullable=False),
    Column("value", Float, nullable=False),
)


meta.create_all(bind=engine, tables=[pronostications])
