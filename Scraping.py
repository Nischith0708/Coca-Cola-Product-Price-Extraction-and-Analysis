from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import pickle
import re
from collections import defaultdict
import pandas as pd
import csv
import datetime
import time
import subprocess


today = datetime.date.today()
formatted_date = today.strftime("%B %d, %Y")




def create_dictionary():
    
    file = open('links.txt', 'r')

    dictionary = {}

    for line in file:
        # Match the text in the format '(a,b)'
        match = re.match(r'\((.*?),\s*(.*?)\)', line)

        # If the match is successful, add the key-value pair to the dictionary
        if match:
            key = match.group(1)
            value = match.group(2)
            dictionary[key] = value

    
    file.close()

    return dictionary



dictionary = create_dictionary()


print(dictionary)



def lst(web):
    parsed_web = urlparse(web)
    website_name = parsed_web.netloc
    l = website_name.split('.')
    return l[1]

 
def price_value(web,pname):
    driver_path = r'C:\Users\Engro\Downloads\chromedriver.exe'  

    options = Options()
    #options.add_argument('--headless')

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(web)
    
    
       
    if lst(web) == 'qoo10':
        try:   
            element = driver.find_element(By.XPATH, "//strong[@data-price]")
            price = element.get_attribute("data-price") if element else 'Price not found'
            price_symbol = ' 円'
            whole_price=price + price_symbol
            return([formatted_date,'Qoo10',pname,whole_price])
        except:
            return([formatted_date,'Qoo10',pname,"0"])
    
    if lst(web) == 'shopping':
        try:
            whole_price = driver.find_element(By.CLASS_NAME, 'elPriceNumber').text
            price_symbol = ' 円'
            price = whole_price + price_symbol
            total=price.replace(',','')
            return([formatted_date,'Yahoo! Shopping',pname,total])
        except:
            return([formatted_date,'Yahoo! Shopping',pname,"0"])
        
    if lst(web) == 'rakuten':
        try:
            time.sleep(4)
            whole_price_element = driver.find_element(By.XPATH, '//*[@id="rakutenLimitedId_cart"]/tbody/tr[2]/td/span[1]/span/div[1]/div')
            whole_price = whole_price_element.text
            new_string = whole_price.replace(',', "")
            price_symbol = ' 円'
            price = new_string + price_symbol
            return([formatted_date,'Rakuten',pname,price])
        except:
            return([formatted_date,'Rakuten',pname,"0"])
    if lst(web) == 'amazon':
        try:
            
            time.sleep(5)
            # Try to find the element by its class
            box= driver.find_element(By.XPATH, '//*[@id="unqualifiedBuyBox"]')
            box1 = driver.find_element(By.XPATH, '//*[@id="unqualifiedBuyBox"]/div')
            box2 = driver.find_element(By.XPATH, '//*[@id="exports_desktop_unqualifiedBuybox_all_buying_options_cta_feature_div"]')

            box2.click()
            time.sleep(7)

            box7 = driver.find_element(By.XPATH, '//*[@id="aod-price-1"]/div[1]/span/span[2]/span[2]')
            price=box7.text + ' 円'
            total=price.replace(',','')
            return([formatted_date,'Amazon Japan',pname,total])

    # Do something with the element, if needed
        except :
            try:
                time.sleep(5)
                element = driver.find_element(By.XPATH,'//*[@id="outOfStock"]')
                return([formatted_date,'Amazon Japan',pname,"0"])
            except:
                time.sleep(12)
                element = driver.find_element(By.XPATH,'//*[@id="exports_desktop_outOfStock_buybox_message_feature_div"]/div')
                return([formatted_date,'Amazon Japan',pname,"0"])
            else:
                element = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]')
                price=element.text + ' 円'
                return([formatted_date,'Amazon Japan',pname,price])

    if lst(web) == 'jp':
        try:
            whole_price_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/section/section/div[3]/div[2]/div[1]/div/div[2]/div/div/span')
            whole_price = whole_price_element.text
            price=whole_price[:-6]
            price_mod=price.replace(',', "")
            total=price_mod+' 円'
            return([formatted_date,'Wowma!',pname,total])
        except:
            try:
                time.sleep(10)
                whole_price_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/section/section/div[3]/div[2]/div[1]/div/div[3]/div[2]/div/span')
                whole_price = whole_price_element.text
                price=whole_price[:-6]
                total=price+' 円'
                total_mod=total.replace(',', "")
                return([formatted_date,'Wowma!',pname,total_mod])
            except:
                return([formatted_date,'Wowma!',pname,"0"])
            
    


 
count=0
import csv

with open("output.csv", "a", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    
    # Check if the file is empty
    is_empty = csvfile.tell() == 0
    
    if is_empty:
        # Write header if the file is empty
        writer.writerow(["Date", "Links", "Brands", "Price"])
    
    for key, value in dictionary.items():
        count = count + 1
        a = price_value(key, value)
        writer.writerow(a)

         
    print(count)


df = pd.read_csv('output.csv')
df_sorted = df.sort_values(by=['Date', 'Links'])
df_sorted.to_csv('output.csv', index=False)
       
csvfile.close()


