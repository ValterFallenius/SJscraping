from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import datetime
today = datetime.date.today()


#Aks the user for how many days to scout ahead
daysahead = int(input("How many days ahead from today ("+ str(today)+ ") do you wanna scout?"))

#Here goes the path to your chromedriver.exe file:
path_to_chromedriver = 'C:\Program Files\chromedriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path_to_chromedriver)

dates=[] #List to store exact date
prices=[] #List to store price of the tickets
my_url="https://www.sj.se/#/tidtabell/K%25C3%25B6benhavn%2520H/Stockholm%2520Central/enkel/avgang/20200101-0500/avgang/20200101-1500/BO-22--false///0//"

for i in range(daysahead):
    prices_today = []
    dates.append(str(today))
    today += datetime.timedelta(days=1)
    my_url = my_url.replace(my_url[90:98],str(today).replace("-", ""),2)

    driver.get(my_url)
    sleep(5)
    button = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div/div[5]/div[4]/div/button")
    sleep(5)
    button.click()
    sleep(5)

    button = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div/div[5]/div[4]/div/button")
    sleep(5)
    button.click()
    sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")





    for a in soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ["timetable-unexpanded-price"]):
        not_available = a.find("span", attrs={"class":"timetable-unexpanded-price--unavailable"})
        if not_available: continue
        else:
            try:

                price=a.find(lambda tag: tag.name == 'span' and tag.get('class') == ['ng-binding']).get_text()
                price = price.replace(" ", "")
                price = int(price)
                prices_today.append(price)
            except AttributeError:
                pass
    prices.append(prices_today)
driver.quit()
print(prices)

#Time to sort these prices and print the cheapest days to travel.

all_time_cheapest=1337
dates_with_all_time_cheapest=[]
for prices_today,date in enumerate(dates):
    cheapest=min(prices[prices_today])
    if cheapest<all_time_cheapest:
        dates_with_all_time_cheapest=[date]
        all_time_cheapest=cheapest
    elif cheapest == all_time_cheapest:
        dates_with_all_time_cheapest.append(date)
    else:
        continue
print(dates_with_all_time_cheapest, all_time_cheapest)
