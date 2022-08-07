import imp
import aiohttp
import asyncio
from config import get_secret


# https://docs.aiohttp.org/en/stable/ aiohttp공식설명  -> pip install aiohttp~=3.7.3   설치


async def fetcher(session, url):
    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)


async def main():  # 동시성을 이용해서 요청을 계속 보내고 기다리지 않고 하나 더 보내고 다시 보내고
    Base_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [f"{Base_URL}?query={keyword}&display=20&start={1+ i*20}" for i in range(10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetcher(session, url) for url in urls])
        # result = await fetcher(
        #     session, urls[0]
        # )  # fetcher는 코르틴 함수이기 때문에 어웨이터블awaitable 객체임 그래서 이렇게 받아야함


if __name__ == "__main__":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
