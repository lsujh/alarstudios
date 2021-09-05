import databases

from app.core.config import settings


async def check_db_connected():
    try:
        database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
        if not database.is_connected:
            await database.connect()
            await database.execute("SELECT 1")
        print("Database is connected")
    except Exception as e:
        print(
            "Looks like db is missing or is there is some problem in connection,see below traceback"
        )
        raise e


async def check_db_disconnected():
    try:

        database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
        if database.is_connected:
            await database.disconnect()
        print("Database is Disconnected")
    except Exception as e:
        raise e
