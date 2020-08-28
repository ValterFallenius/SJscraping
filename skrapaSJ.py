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

dates=[] #List to store exact date
prices=[] #List to store price of the tickets
my_url_to_sthlm="https://www.sj.se/#/tidtabell/K%25C3%25B6benhavn%2520H/Stockholm%2520Central/enkel/avgang/20200101-0001/avgang/20200101-0001/BO-22--false///0//"
my_url_to_cph="https://www.sj.se/#/tidtabell/Stockholm%2520Central/K%25C3%25B6benhavn%2520H/enkel/avgang/20200101-0001/avgang/20200101-0001/BO-22--false///0//"
driver = webdriver.Chrome(executable_path=path_to_chromedriver)

waiting = 3
def main(my_url):

    for i in range(daysahead):
        prices_today = []


        dates.append(str(today))
        my_url = my_url.replace(my_url[90:98],str(today).replace("-", ""),2)

        driver.get(my_url)
        sleep(waiting)
        for i in range(2):
            try:
                button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[2]/div/div/div[5]/div[4]/div/button")
            except:
                pass
            try:
                button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div/div[5]/div[4]/div/button")
            except:
                pass
            if button.get_attribute("class")!="timetable__navigation-container timetable__link-hover-state timetable__navigation-button outline ng-scope":
                continue
            button.click()
            sleep(waiting)

        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")





        for a in soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ["timetable-unexpanded-price"]):
            not_available = a.find("span", attrs={"class":"timetable-unexpanded-price--unavailable"})
            if not_available:
                continue
            else:
                try:
                    price=a.find(lambda tag: tag.name == 'span' and tag.get('class') == ['ng-binding']).get_text()
                    price = price.replace(" ", "")
                    price = int(price)
                    prices_today.append(price)

                except AttributeError:
                    pass
        if prices_today: prices.append(prices_today)
        today += datetime.timedelta(days=1)
    driver.quit()

    #Time to sort these prices and print the cheapest days to travel.
    cheapest=1338
    all_time_cheapest=1337
    dates_with_all_time_cheapest=[]
    for prices_today,date in enumerate(dates):
        try:
            cheapest=min(prices[prices_today])
        except:
            continue
        if cheapest<all_time_cheapest:
            dates_with_all_time_cheapest=[date]
            all_time_cheapest=cheapest
        elif cheapest == all_time_cheapest:
            dates_with_all_time_cheapest.append(date)
        else:
            continue
    return(dates_with_all_time_cheapest, all_time_cheapest)

print("for STHLM to CPH:", str(main(my_url_to_cph)))
print("for CPH to STHLM:", str(main(my_url_to_sthlm)))
