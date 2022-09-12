import asyncio
import importlib
import json
import logging
from importlib import resources
from types import SimpleNamespace

from telethon import TelegramClient, events

configFile = "./config.json"
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)


async def global_handler(event):
    await event.respond("handler hi!")


async def import_plugins(package, bot):
    files = resources.contents(package)
    plugin_names = [f[:-3] for f in files if f.endswith(".py") and f[0] != "_"]

    plugins = [
        importlib.import_module(f"{package}.{plugin}")
        for plugin in plugin_names
    ]
    for p in plugins:
        try:
            await p.init(bot)
            logging.info(f"plugin {p.__name__} loaded")
        except Exception:
            logging.error(f"failed to load {p.__name__}")


async def main():

    # https://stackoverflow.com/a/15882054
    with open(configFile, "r") as f:
        cfg = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

    bot = TelegramClient("bot", cfg.api_id, cfg.api_hash)
    await bot.start(bot_token=cfg.bot_token)

    # init global handlers
    bot.add_event_handler(
        global_handler,
        events.NewMessage(from_users=cfg.user_id, pattern="/hello"),
    )

    try:
        await import_plugins("plugins", bot)
        await bot.run_until_disconnected()
    except ImportError:
        logging.error(
            "Could not load plugins module, ensure the directory exists."
        )
    # finally:
    #     await bot.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
