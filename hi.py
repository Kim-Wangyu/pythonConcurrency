import asyncio
import aiohttp
import requests


# def io_bound_func():
#     result = requests.get("https://google.com")
#     return result  #이 함수는 한번 응답을 보내면 끝, 그래서 with 를 사용할거임 or 세션을 사용해 서버와클라사이를 유지시켜줌


async def fetcher(session, url):  # 인자로 현재 열려있는 세션을 받음
    async with session.get(url) as response:  # 이 세션에 대해서 with구문을 사용
        return await response.text()


async def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]

    # session = requests.Session()
    # session.get(url)  #세션 오픈 한것임
    # session.close()   이 3줄이 아래 2줄로 요약이됨, 여기서 열어주고 닫아주느냐 or 아래에서 자동으로 열고 닫게 해주거나

    async with aiohttp.ClientSession() as session:
        # session.get(url)
        # result = [fetcher(session, url) for url in urls]
        # fetcher의 의미는 해당하는 세션에 url을 보내가지고 해당하는 url의 데이터를 다 가지고 오는것 리턴을 해주는것
        # print(result)
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        print(result)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
# if __name__ == "__main__":
#     result = io_bound_func()
#     print(result)
