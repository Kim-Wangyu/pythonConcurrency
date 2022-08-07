import aiohttp
from bs4 import BeautifulSoup
import asyncio


# https://docs.aiohttp.org/en/stable/ aiohttp공식설명  -> pip install aiohttp~=3.7.3   설치


async def fetcher(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        cont_thumb = soup.find_all("div", "cont_thumb")
        print(cont_thumb)

        for cont in cont_thumb:
            title = cont.find("p", "txt_thumb")
            if title is not None:
                print(title.text)


async def main():  # 동시성을 이용해서 요청을 계속 보내고 기다리지 않고 하나 더 보내고 다시 보내고
    Base_URL = "https://bjpublic.tistory.com/category/%EC%A0%84%EC%B2%B4%20%EC%B6%9C%EA%B0%84%20%EB%8F%84%EC%84%9C"
    urls = [f"{Base_URL}?page={i}" for i in range(1, 10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetcher(session, url) for url in urls])
        # result = await fetcher(
        #     session, urls[0]
        # )  # fetcher는 코르틴 함수이기 때문에 어웨이터블awaitable 객체임 그래서 이렇게 받아야함


if __name__ == "__main__":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
