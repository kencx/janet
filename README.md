# J.A.N.E.T
>**Just A Nifty Electronic Tool**

Janet is a selfhosted, personal all-in-one Telegram bot.

Janet is easily extendable with custom plugins.

## Plugin Template
Create a plugin in `/plugins` with the following template:

```python
async def init(bot):
    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):
        await event.respond('Hi!')
```
