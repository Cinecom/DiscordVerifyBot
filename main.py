#!/usr/bin/env python3

import asyncio
import logging
import os
import threading
from dotenv import load_dotenv
from flask import Flask
from bot import VerificationBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'),
              logging.StreamHandler()])

logger = logging.getLogger(__name__)

# Create Flask app for UptimeRobot
app = Flask(__name__)


@app.route('/')
def home():
    return "Discord bot is running!"


@app.route('/health')
def health():
    return {"status": "online", "message": "Bot is healthy"}


def run_flask():
    """Run Flask server in a separate thread."""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)


async def main():
    """Main entry point for the Discord bot."""
    # Get Discord token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables")
        return

    # Start Flask server in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask server started for UptimeRobot monitoring")

    # Create and run the bot
    bot = VerificationBot()

    try:
        logger.info("Starting Discord verification bot...")
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
