from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://udtiprhg06szg6lm:HATF7CaOXzPPNKH4W8wK@bmrrggwuyfqveoqr0sab-mysql.services.clever-cloud.com:3306/bmrrggwuyfqveoqr0sab",
    pool_timeout=40,
    pool_recycle=60 * 5,
    pool_pre_ping=True,
)

meta = MetaData()

conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
