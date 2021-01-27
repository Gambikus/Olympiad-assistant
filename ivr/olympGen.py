from selenium import webdriver
from bs4 import BeautifulSoup
import config
import time
import json

data = {}
for i in config.subjects:
    data[i] = {}
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
driver = webdriver.Chrome(executable_path=r'C:\Users\ver45\PycharmProjects\chromedriver.exe', options=options)
driver.get('https://olimpiada.ru/activities?type=ind&class=any&period_date=&period=year')
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
print(driver.execute_script("return document.body.scrollHeight"))
soup = BeautifulSoup(driver.page_source, 'html5lib')
print(len(soup.find_all("div", "olimpiada")))
for tag in soup.find_all("div", "olimpiada"):
    if "subord_item" in tag["class"]:

        continue
    if len(tag.findChildren("span", "classes_dop")) == 0:
        continue
    if len(tag.findChildren("span", "classes_dop")[0].contents) == 0:
        continue
    classes = str(tag.findChildren("span", "classes_dop")[0].contents[0]).split('\xa0')[0]
    classes = classes.split()[0]
    if classes[-1] in "22345678":
        continue
    k = 1
    oly = tag.findChildren("tr")[0]
    oly2 = tag.findChildren("tr")[1]
    for subj in oly.findChildren('span', "subject_tag"):
        if ' '.join(str(subj.contents[1]).split('\xa0')).strip() not in config.subjects:
            continue
        print()
        print(' '.join(str(subj.contents[1]).split('\xa0')).strip())
        data[' '.join(str(subj.contents[1]).split('\xa0')).strip()][len(data[' '.join(str(subj.contents[1]).split('\xa0')).strip()].keys()) + 1] = {}
        data[' '.join(str(subj.contents[1]).split('\xa0')).strip()][
            len(data[' '.join(str(subj.contents[1]).split('\xa0')).strip()].keys())]["Name"] = \
            ' '.join(str(oly2.findChildren("span")[0].contents[0]).split('\xa0')).strip()
        data[' '.join(str(subj.contents[1]).split('\xa0')).strip()][
            len(data[' '.join(str(subj.contents[1]).split('\xa0')).strip()].keys())]["href"] = \
            "https://olimpiada.ru" + oly2.findChildren("a")[0]["href"]
        data[' '.join(str(subj.contents[1]).split('\xa0')).strip()][
            len(data[' '.join(str(subj.contents[1]).split('\xa0')).strip()].keys())]["time"] = {}
        if len(tag.findChildren("div", "timeline")) == 0:
            continue
        time = tag.findChildren("div", "timeline")[0]
        for ev in time.find_all("div", "enow"):
            data[' '.join(str(subj.contents[1]).split('\xa0')).strip()][
                len(data[' '.join(str(subj.contents[1]).split('\xa0')).strip()].keys())]["time"][ev["date"]] = \
                ' '.join(str(ev.findChildren("font")[0].contents[0]).split('\xa0'))
    print(data)
with open("olimps.json", 'w') as file:
    json.dump(data, file)
