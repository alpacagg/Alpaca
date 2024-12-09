from tortoise import Tortoise


async def init_db():
    """Initialize the database and create tables."""
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['src.database.models']}
    )
    await Tortoise.generate_schemas(safe=True)
    

async def close_db():
    """Close the database connections."""
    await Tortoise.close_connections()
