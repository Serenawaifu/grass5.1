import asyncio
from loguru import logger
from account_manager import register_account
from proxy_manager import ProxyPool
from telegram_bot import notify_telegram

async def run_registration(account, proxy_pool):
    email, password, referral = account
    account_id = hash(email)  # Unique identifier for the account
    status = await register_account(email, password, referral, proxy_pool, account_id)
    if status == "🟢":
        notify_telegram(f"✅ {email} registered successfully!")
    else:
        notify_telegram(f"❌ Failed to register {email}")

async def main():
    # Load proxies from file
    proxies = load_proxies_from_file("proxies.txt")
    proxy_pool = ProxyPool(proxies)

    # Sample accounts (replace with your data)
    accounts = [
        ("user1@example.com", "pass123", "ref123"),
        ("user2@example.com", "pass456", "ref456"),
    ]

    # Run registrations in parallel with error handling
    tasks = []
    for account in accounts:
        tasks.append(run_registration(account, proxy_pool))
    
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    logger.info("Starting registration process...")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
