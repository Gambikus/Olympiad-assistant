# импорт библиотек
from selenium import webdriver
from bs4 import BeautifulSoup
import config
import telebot
import datetime
from SQLighter import SQLighter
import schedule
import time
import json


bot = telebot.TeleBot(config.token)


def job():
    print()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # для открытия headless-браузера
    driver = webdriver.Chrome(executable_path=r'C:\Users\ver45\PycharmProjects\chromedriver.exe', options=options)
    driver.get('https://olimpiada.ru/news')
    requiredHtml = driver.page_source
    soup = BeautifulSoup(requiredHtml, 'html5lib')
    table = soup.findChildren('h2')
    for tag in soup.find("h2", text="Вчера").find_all_previous("div", "news_item_in_full_list"):
        chdriver = webdriver.Chrome(executable_path=r'C:\Users\ver45\PycharmProjects\chromedriver.exe', options=options)
        chdriver.get('https://olimpiada.ru' + tag.findChildren('a')[0]["href"])
        chsoup = BeautifulSoup(chdriver.page_source, 'html5lib')
        users = set()
        with open("subjects.json", 'r') as file:
            data = json.load(file)

            for subj in chsoup.find_all("div", "subject_tags")[0].findChildren("span", "subject_tag"):
                if ' '.join(str(subj.contents[1]).split('\xa0')).strip() not in config.subjects:
                    continue
                for user in data[' '.join(str(subj.contents[1]).split('\xa0')).strip()]:
                    users.add(user)
        for user in users:
            bot.send_message(user, "❗❗Новость❗❗\n\n" + tag.findChildren('a')[0].contents[0] + '\n\n' +
                             'Источник: https://olimpiada.ru' + tag.findChildren('a')[0]["href"])
        print(tag.findChildren('a')[0]["href"])
        print(tag.findChildren('span')[1]["class"])


def remind():
    today = datetime.datetime.now()
    with open("dates.json", 'r') as file:
        with open("dateOfOli.json", 'r') as rfile:
            olimps = json.load(rfile)
            data = json.load(file)
            for date, event in data.items():
                s = date.split('-')
                newdate = datetime.datetime(int(s[0]), int(s[1]), int(s[2]))
                print(newdate, (newdate - today).days, event)
                if (newdate - today).days == 5:
                    for text, id in event:
                        db = SQLighter(config.database_name)
                        oli = db.get_oly(str(id))
                        for user in olimps[str(id)]:
                            bot.send_message(user, "❗Внимание❗\n\n" + oli[1] + '\n' + text + ' ' +
                                             "начнется через 5 дней!" + '\n\n' + 'Источник: ' + oli[4])
                elif (newdate - today).days == 1:
                    for text, id in event:
                        db = SQLighter(config.database_name)
                        oli = db.get_oly(str(id))
                        for user in olimps[str(id)]:
                            bot.send_message(user, "❗Внимание❗\n\n" + oli[1] + '\n' + text + ' ' +
                                             "начнется завтра!" + '\n\n' + 'Источник: ' + oli[4])


schedule.every().day.at("17:47").do(remind)
schedule.every().day.at("20:12").do(job)


while True:
    schedule.run_pending()
    job()
    time.sleep(60)
