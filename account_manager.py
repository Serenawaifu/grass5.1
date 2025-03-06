import aiohttp
from loguru import logger
from proxy_manager import ProxyPool

async def register_account(email, password, referral_code, proxy_pool, account_id):
    try:
        # Fetch a valid proxy for this account
        proxy = await proxy_pool.get_proxy(account_id)
        if not proxy:
            raise ValueError("No valid proxy available")

        # Prepare request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://app.getgrass.io/register",
        }
        data = {
            "email": email,
            "password": password,
            "referral_code": referral_code,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://app.getgrass.io/register",
                headers=headers,
                data=data,
                proxy=proxy,
                timeout=30
            ) as response:
                if response.status == 200:
                    content = await response.text()
                    if "Registration successful" in content:
                        logger.info(f"✅ Account {email} registered via proxy {proxy}")
                        return "🟢"
                    else:
                        logger.error(f"Registration failed for {email}: {content}")
                        return "🔴"
                else:
                    logger.warning(f"HTTP Error {response.status} for {email}")
                    return "🔴"

    except (aiohttp.ClientError, TimeoutError) as e:
        logger.warning(f"Connection error for {email}: {str(e)}. Switching proxy...")
        proxy_pool.reset_proxy(account_id)  # Reset proxy pool for retries
        return await register_account(email, password, referral_code, proxy_pool, account_id)  # Retry

    except Exception as e:
        logger.error(f"Critical error for {email}: {str(e)}")
        return "⚠️"
