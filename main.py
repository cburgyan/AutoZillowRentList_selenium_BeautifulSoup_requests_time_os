import bs4
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os


GOOGLE_DOC = 'https://docs.google.com/forms/d/e/1FAIpQLSdhgoK2008P6_hl2m0EHfhEZzYPQ7zGoeF7haRYhAbl8Rd1ww/viewform?usp=sf_link'
URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

parameters = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
}

response = requests.get(url=URL, headers=parameters)
website_html = response.text

soup = bs4.BeautifulSoup(website_html, 'html.parser')

print(soup.prettify())

price_of_property_tags = soup.select(selector='.list-card-price')
print(type(price_of_property_tags))
print(price_of_property_tags)
print(f'\nget Text:')
count = 0
for tag in price_of_property_tags:
    count += 1
    print(f'{count}. {tag.get_text()}')

property_price_list = [tag.get_text()[0:6] for tag in price_of_property_tags]
count = 0
print('\nPrices:')
for price in property_price_list:
    count += 1
    print(f'{count}. {price}')

address_of_property_tags = soup.select(selector='.list-card-addr')
print(type(address_of_property_tags))
print(address_of_property_tags)
print(len(address_of_property_tags))
print(f'\nget Text:')
count = 0
for tag in address_of_property_tags:
    count += 1
    print(f'{count}. {tag.get_text()}')

property_address_list = [tag.get_text() for tag in address_of_property_tags]
count = 0
print('\naddresses:')
for address in property_address_list:
    count += 1
    print(f'{count}. {address}')



link_of_property_tags = soup.select(selector='.list-card-img')
print(type(link_of_property_tags))
print(link_of_property_tags)
print(len(link_of_property_tags))
print(f'\nget Link:')
count = 0
for tag in link_of_property_tags:
    count += 1
    try:
        print(f'{count}. {tag["href"]}')
    except Exception:
        print(f'{count}. {tag}')

property_link_list = []
for tag in link_of_property_tags:
    try:
        if 'http' not in tag['href']:
            href = f'https://www.zillow.com{tag["href"]}'
        else:
            href = tag['href']
        property_link_list.append(href)
    except Exception:
        pass

count = 0
print('\nlinks:')
for link in property_link_list:
    count += 1
    print(f'{count}. {link}')



#Create Chrome Driver
servicer = webdriver.chrome.service.Service(os.environ.get('CHROME_DRIVER_PATH'))
driver = webdriver.Chrome(service=servicer)


#Connect Driver to Website
driver.get(GOOGLE_DOC)


for index in range(len(property_price_list)):
    #Create selenium.webdriver.remote.webelement.WebElements
    address_we = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    address_we.send_keys("Hey")
    price_we = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    link_we = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    submit_we = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')))


    #Enter Data
    address_we.send_keys(property_address_list[index])
    price_we.send_keys(property_price_list[index])
    link_we.send_keys(property_link_list[index])
    submit_we.click()
    time.sleep(4)
    add_another_response_we = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    add_another_response_we.click()




time.sleep(120)




