
from aiofile import async_open


async def readlogs():
    return ''
    async with async_open('assets/last.txt', 'r') as file:
        text = await file.read()
    return text


async def writelog(user_id: int, log: str):
    return
    async with async_open('assets/last.txt', 'a') as file:
        await file.write(f'{user_id}:{log}\n')
