import os

from telethon import events


async def init(bot):
    @bot.on(events.NewMessage(pattern="/ping"))
    async def ping(event):
        hostname = event.raw_text.split(sep=" ")[1]
        response = os.system("ping -c 1 " + hostname)

        if response == 0:
            await event.respond(f"{hostname} is up!")
        else:
            await event.respond(f"{hostname} is down!")
