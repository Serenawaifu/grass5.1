import random
from loguru import logger
from aiohttp import ClientSession, ClientError, TCPConnector
from tenacity import retry, wait_fixed, stop_after_attempt

class ProxyPool:
    def __init__(self, proxies):
        self.primary_proxies = proxies[:100]  # First 100 as primary
        self.backup_proxies = proxies[100:]   # Remaining as backups
        self.used_proxies = {}  # Track usage per account

    async def get_proxy(self, account_id):
        """Return a working proxy for the account, switching if needed."""
        if account_id not in self.used_proxies:
            self.used_proxies[account_id] = {
                "current": 0,
                "primary": list(self.primary_proxies),
                "backup": list(self.backup_proxies)
            }
        pool = self.used_proxies[account_id]

        # Try primary proxies first
        while pool["current"] < len(pool["primary"]):
            proxy = pool["primary"][pool["current"]]
            if await self.validate_proxy(proxy):
                return proxy
            else:
                pool["current"] += 1

        # Switch to backups if all primaries failed
        if pool["backup"]:
            proxy = random.choice(pool["backup"])
            if await self.validate_proxy(proxy):
                return proxy
            else:
                pool["backup"].remove(proxy)
                return await self.get_proxy(account_id)

        logger.error("No valid proxies available for account: {}".format(account_id))
        return None

    @staticmethod
    @retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
    async def validate_proxy(proxy):
        """Check if a proxy is alive."""
        try:
            async with ClientSession(
                connector=TCPConnector(ssl=False)
            ) as session:
                async with session.get(
                    "http://httpbin.org/ip",
                    proxy=proxy,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        return True
        except ClientError as e:
            logger.warning(f"Proxy {proxy} failed: {str(e)}")
            return False
        return False

    def reset_proxy(self, account_id):
        """Reset proxy pool for an account."""
        self.used_proxies[account_id]["current"] = 0
        self.used_proxies[account_id]["backup"] = list(self.backup_proxies)
