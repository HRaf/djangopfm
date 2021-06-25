import pymongo
from mongoengine import connect
from pymongo import MongoClient
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from indexing_data import add_data_to_elastic


#Scrapping news
class scrapping():
    #Scrapping real data
    def scrapFromAlyaoum24(url):
        #'https://alyaoum24.com/news/coronavirus/page'
        mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
        db = mongo.NEWS_DB
        titles = []
        texts = []
        dates = []
        for i in range(20):
            page = requests.get(url + str(i))
            soup = BeautifulSoup(page.content, 'html.parser')
            articles = soup.find('ul', class_='listing-archive')
            li_articles = articles.find_all('li')
            for li in li_articles:

                link = li.find('a', href=True)
                nextpage = requests.get(link.get('href'))
                soupnext = BeautifulSoup(nextpage.content, 'html.parser')
                title = soupnext.find('h1').text
                #titles.append(title)
                date = soupnext.find('span', class_='timePost').text
                #dates.append(date)
                textclass = soupnext.find('div', class_='post_content')
                contentList = []
                for par in textclass.find_all('p'):
                    content = par.text
                    contentList.append(content)
                    content = ' '.join(contentList)

                    #texts.append(content)
                news= {"url":url,"title": title, "content": content,"date":date,"language":"arabic","classe":0}
                #news = pd.DataFrame(list(zip(titles,texts, dates)), columns=['Title', 'Content', 'Date'])
                add_data_to_elastic(title, content, date)
                dbResponse = db.quickstart_news.insert_one(news)
                print(dbResponse.inserted_id)

    #scrapping fake news
    def scrapFromFatabayyano(url):
        #https://fatabyyano.net/?s=+%D9%83%D9%88%D8%B1%D9%88%D9%86%D8%A7
        mongo = pymongo.MongoClient(
            host="localhost",
            port=27017,
            serverSelectionTimeoutMS=1000,
        )
        db = mongo.NEWS_DB
        options = Options()
        b = webdriver.Chrome(options=options)
        url = 'https://fatabyyano.net/?s=+%D9%83%D9%88%D8%B1%D9%88%D9%86%D8%A7'
        b.get(url)
        for i in range(45):
            try:
                btn = b.find_element_by_class_name('w-btn.us-btn-style_5')
                btn.click()
            except ElementClickInterceptedException:
                print("error")

        soup=BeautifulSoup(b.page_source,'html.parser')
        articles = soup.find_all('article')
        for art in articles:
            head = art.find('h2',
                            class_='w-post-elm post_title usg_post_title_1 entry-title color_link_inherit')
            link = head.find('a', href=True)
            nextpage = requests.get(link.get('href'))
            soupnext = BeautifulSoup(nextpage.content, 'html.parser')
            title = soupnext.find('h1',
                                  class_='w-post-elm post_title us_custom_d6b5cf89 entry-title color_link_inherit')
            title=title.text
            date = soupnext.find('time',
                                 class_='w-post-elm post_date us_custom_0fd75781 entry-date published').text
            date = date.split(':')
            date=date[1]
            con = soupnext.find('div', class_='w-post-elm post_content')
            contentList=[]
            for par in con.find_all('p'):
                paragraph=par.text
                contentList.append(paragraph)
                content=' '.join(contentList)



            news = {"url": url, "title": title, "content": content, "date": date, "language": "arabic", "classe": 1}
            # news = pd.DataFrame(list(zip(titles,texts, dates)), columns=['Title', 'Content', 'Date'])
            add_data_to_elastic(title,content,date)
            dbResponse = db.quickstart_news.insert_one(news)
            print(dbResponse.inserted_id)






if __name__ == '__main__':
    print('PyCharm')
    connect('NEWS_DB', host='mongodb://localhost', alias='default')
    scrapping.scrapFromAlyaoum24('https://alyaoum24.com/news/coronavirus/page')
    scrapping.scrapFromFatabayyano('https://fatabyyano.net/?s=+%D9%83%D9%88%D8%B1%D9%88%D9%86%D8%A7')



