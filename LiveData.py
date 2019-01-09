import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import csv
import pandas as pd
# https://finance.yahoo.com/quote/{}/history?p={}    This is the one that works
# https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC
def getStockInfo(ticker):
    #driver = webdriver.Chrome("/Users/austindiaz/Downloads/chromedriver")
    url = 'https://finance.yahoo.com/quote/%5EGSPC?p={}'.format(ticker)
    #driver.get(url)
    
    response = urllib.request.urlopen(url)
    html = response.read()

    #driver.page_source this goes back into beautiful soup
    soup = BeautifulSoup(html,"lxml")
    price = soup.find(id="quote-market-notice").find_parent().find_parent().find("span").text
    print(price)
    volume = soup.find("td", {"data-test":"TD_VOLUME-value"}).find("span").text
    # volume = soup2.find("span", {"data-reactid":"51"})
    print(volume)
    #driver.quit()

    price = float(price.replace(',' , ''))
    volume = int(volume.replace(',' , ''))

    time = datetime.datetime.now().time()
    time = str(time)
    data = [{'time': time, 'Price':price, 'Volume':volume}]
    dataList = [time, price, volume]
    newData = pd.DataFrame(data)

    my_file = Path("/Users/austindiaz/Documents/pythonPractice/gspc4.csv")
    if my_file.is_file():
        # df = pd.read_csv('gspc.csv')
        with open('gspc4.csv', 'a') as f:
            newFileWriter = csv.writer(f)
            newFileWriter.writerow(dataList)
            # frames = [df, newData]
            # result = pd.concat(frames)
            # newData.to_csv(f, header=False)
    
    else:
        data = [{'time': time, 'Price':price, 'Volume':volume}]
        newData = pd.DataFrame(data)
        newData = newData[['time', 'Price','Volume']]
        newData.to_csv('gspc4.csv', index = False)

ticker = "^GSPC"
for i in range(1,4):
    getStockInfo(ticker)
