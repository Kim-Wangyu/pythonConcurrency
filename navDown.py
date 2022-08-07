import os
import aiohttp
import asyncio
from config import get_secret
import aiofiles


# https://docs.aiohttp.org/en/stable/ aiohttp공식설명  -> pip install aiohttp~=3.7.3   설치
# pip install aiofiles==0.7.0


async def img_downloader(session, img):
    img_name = img.split("/")[-1].split("?")[
        0
    ]  # img =https://i.pinimg.com/originals/2c/8c/6e/2c8c6ede99c6ac8600b813bfe530df65.jpg 여기서 2c8c6ede99c6ac8600b813bfe530df65.jpg 추출

    try:
        os.mkdir("./images")
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(
                f"./images/{img_name}", mode="wb"
            ) as file:  # 쓰는것! w 근데 byte니까 b
                # img_data = await response.read()
                # await file.write(img_data)   #아래 한줄이랑 같음
                await file.write(await response.read())


async def fetcher(session, url):
    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]

        await asyncio.gather(*[img_downloader(session, img) for img in images])


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
