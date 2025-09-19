import aiosqlite
from pathlib import Path
from .config import cfg

Path(cfg.db_path).parent.mkdir(parents=True, exist_ok=True)

async def init_db():
    async with aiosqlite.connect(cfg.db_path) as db:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY,
              username TEXT,
              first_name TEXT,
              last_name TEXT,
              created_at INTEGER
            );
            CREATE TABLE IF NOT EXISTS reflections (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL,
              mood INTEGER CHECK(mood BETWEEN 1 AND 5),
              text TEXT NOT NULL,
              tags TEXT,
              created_at INTEGER
            );
            """
        )
        await db.commit()

async def upsert_user(u):
    import time
    async with aiosqlite.connect(cfg.db_path) as db:
        await db.execute(
            """
            INSERT INTO users(id, username, first_name, last_name, created_at)
            VALUES(?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET username=excluded.username,
                first_name=excluded.first_name,
                last_name=excluded.last_name
            """,
            (u.id, u.username, u.first_name, u.last_name, int(time.time()*1000)),
        )
        await db.commit()

async def insert_reflection(user_id: int, mood: int, text: str, tags: str):
    import time
    async with aiosqlite.connect(cfg.db_path) as db:
        await db.execute(
            "INSERT INTO reflections(user_id, mood, text, tags, created_at) VALUES (?,?,?,?,?)",
            (user_id, mood, text, tags, int(time.time()*1000)),
        )
        await db.commit()

async def stats_by_user(user_id: int):
    async with aiosqlite.connect(cfg.db_path) as db:
        async with db.execute(
            "SELECT COUNT(*) as cnt, AVG(mood) as avg_mood FROM reflections WHERE user_id=?",
            (user_id,),
        ) as cur:
            row = await cur.fetchone()
            return {"cnt": row[0] or 0, "avg_mood": float(row[1]) if row[1] is not None else None}

async def list_reflections(user_id: int, limit: int = 1000, offset: int = 0):
    async with aiosqlite.connect(cfg.db_path) as db:
        async with db.execute(
            "SELECT created_at, mood, text, tags FROM reflections WHERE user_id=? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (user_id, limit, offset),
        ) as cur:
            rows = await cur.fetchall()
            return [
                {"created_at": r[0], "mood": r[1], "text": r[2], "tags": r[3] or ""}
                for r in rows
            ]
