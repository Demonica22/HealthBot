import aiosqlite
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DB_NAME = getenv("DB_NAME")


async def initialize_database():
    # Подключаемся к базе данных (если база данных не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу users, если она не существует
        users = """
            CREATE TABLE IF NOT EXISTS Users (
        	id	INTEGER PRIMARY KEY,
        	name	TEXT,
        	gender	INTEGER,
        	language TEXT,
        	weight INTEGER,
        	height INTEGER
        	);
            """
        await db.execute(users)
        # Сохраняем изменения
        await db.commit()


async def get_user_by_id(id: int) -> dict | None:
    async with aiosqlite.connect(DB_NAME) as db:
        query = '''
            SELECT name, gender, language, weight, height
            FROM Users
            WHERE id = ?;
            '''
        result = await db.execute(query, (id,))
        user = await result.fetchone()

        if user is None:
            return None
        return {'name': user[0],
                'gender': user[1],
                'language': user[2],
                'weight': user[3],
                'height': user[4],
                }


async def add_user(id: int, data: dict):
    async with aiosqlite.connect(DB_NAME) as db:
        query = """
            INSERT INTO users (id, name, gender, language, weight, height)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO NOTHING
        """
        await db.execute(query, (id, data['name'], data['gender'], data['language'], data['weight'], data['height']))
        await db.commit()
