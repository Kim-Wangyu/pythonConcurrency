from bs4 import BeautifulSoup
import requests


url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=1"

soup = BeautifulSoup(requests.get(url, headers={"User-agent": "Mozilla/5.0"}).text, "lxml")

# print(soup)

table = soup.find_all("table", {"class": "type_2"})[0]
# print(table)
STOCK_NAME_LIST = []

for tr in table.findAll("tr"):
    stockName = tr.findAll("a", attrs={"class": "tltle"})
    if stockName is None or stockName == []:
        pass
    else:
        print(stockName[0].contents[-1])
        STOCK_NAME_LIST.append(stockName[0].contents[-1])

print(type(STOCK_NAME_LIST))
for i in range(len(STOCK_NAME_LIST)):
    if STOCK_NAME_LIST[i] == "하이브":
        print(STOCK_NAME_LIST[i])
