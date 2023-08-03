from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time


driver_path = r'C:\Users\Engro\Downloads\chromedriver.exe'  # Update with the path to your chromedriver executable

options = Options()
# options.add_argument('--headless')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)




# Set up the WebDriver  # Replace with the appropriate WebDriver for your browser

# Navigate to the web page
driver.get("https://wowma.jp/item/431042679?spe_id=sspromo431042679")  

# Define the class of the element you want to check
time.sleep(10)
whole_price_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/section/section/div[3]/div[2]/div[1]/div/div[3]/div[2]/div/span')
whole_price = whole_price_element.text
price=whole_price[:-6]
total=price+' 円'
total_mod=total.replace(',', "")
print(total_mod)






# Close the WebDriver
driver.quit()



