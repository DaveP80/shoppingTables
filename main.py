from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import requests
import re
import xlsxwriter
import time

urlarr = []
exarr = []
excelarr = []
book = xlsxwriter.Workbook('GoogleShooping4.0.xlsx')     
sheet = book.add_worksheet()
bold = book.add_format({'bold': True}) 
sheet.write('A1', 'shopping query', bold)
sheet.write('B1', 'price', bold)
sheet.write('C1', 'img url', bold)
 
with open("relist.txt") as file_in:
    for url in file_in:
        url.strip()
        urlarr.append(url)

for u in urlarr:

    if exarr:
        excelarr.append(exarr)

    exarr = []

    def searchShop(args):

        try:

            page = requests.get(args)

            soup = BeautifulSoup(page.content, "html.parser")
                        
                
            topic = soup.find('title')

            query = re.sub(r'(?i)Google Shopping','', topic.text)
            fquery = re.sub(r'[^\w\s]', '', query)

            exarr.append(fquery.strip())
       

            return fquery.strip()
        except:
            exarr.append('bad url')
            return "bad url"

    def google_shopSearch(squery):

        if squery=="bad url":
            print("bad url")
            exarr.append("nil")
            exarr.append("nil")
        
        elif squery!="bad url":
            print(squery)
            params = {
            "q": squery,
            "tbm": "shop",
            "hl": "en",
            "gl": "us",
            "api_key": "your_key"
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            
            try:
                shopping_results = results["shopping_results"]
                exarr.append(shopping_results[0]['price'])
                exarr.append(shopping_results[0]['thumbnail'])
            except:
                exarr.append('nil')
                exarr.append('nil')
                print("bad query string")

    google_shopSearch(searchShop(u))
    time.sleep(1)
row = 1
col = 0

for n in excelarr:
     sheet.write(row, col,     n[0])
     sheet.write(row, col + 1, n[1])
     sheet.write(row, col + 2, n[2])
     row += 1

book.close()

