import asyncio
from loguru import logger
from telegram_bot import start_telegram_bot
from database import init_db

async def main():
    # Initialize the database
    await init_db()
    
    # Start the Telegram bot
    await start_telegram_bot()

if __name__ == "__main__":
    logger.info("Starting Grass Farm Bot...")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot failed to start: {str(e)}")
