import aiosqlite

async def init_db():
    async with aiosqlite.connect("grass_farm.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                referral_code TEXT,
                proxy TEXT,
                status TEXT CHECK(status IN ('🟢', '🔴', '⚠️')),
                points INTEGER DEFAULT 0,
                balance REAL DEFAULT 0.0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS proxies (
                id INTEGER PRIMARY KEY,
                protocol TEXT,
                user TEXT,
                password TEXT,
                ip TEXT,
                port INTEGER,
                account_count INTEGER DEFAULT 0
            )
        """)
        await db.commit()
