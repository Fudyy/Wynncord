import aiohttp


async def fetch_json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                json = await r.json()
                return json
