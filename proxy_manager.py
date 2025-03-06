def load_proxies_from_file(file_path):
    proxies = []
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.strip() and not line.startswith("#"):
                proxies.append(line.strip())
    return proxies

async def assign_proxy(email, proxy_str):
    async with aiosqlite.connect("grass_farm.db") as db:
        # Check proxy availability (e.g., account_count < 100)
        # Logic to select and assign proxy here
        await db.execute("INSERT INTO accounts (email, proxy) VALUES (?, ?)", (email, proxy_str))
        await db.commit()
