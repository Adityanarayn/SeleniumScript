from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import datetime
import os 

def getData(s):
    st = s.find("[")
    en = s.find("]")
    g = s[st+1:en]
    f = list(g.split(","))
    return f

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
download_path = dir_path + "\\Downloads"+str(datetime.datetime.timestamp(datetime.datetime.now()))
if not os.path.exists(download_path):
    os.mkdir(download_path)
print(download_path)

driver = webdriver.Chrome(
	executable_path="C:\\Users\\vatsa\\Downloads\\chromedriver_win32\\chromedriver.exe")

driver.get('<url>')
driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/input").click()
driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/input").send_keys("<admin>")
driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/input").click()
driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/input").send_keys("<password>")
driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/input").send_keys(Keys.RETURN)
driver.implicitly_wait(10)
driver.maximize_window()
driver.find_element(By.XPATH, "/html/body/div[2]/aside/section/ul/li[6]/a/span[1]").click()
driver.implicitly_wait(10)
driver.find_element(By.XPATH, "/html/body/div[2]/aside/section/ul/li[6]/ul/li[1]/a").click()
driver.implicitly_wait(10)
table = []
count = 0
while(1):
    count = count+1
    length = len(driver.find_elements(By.XPATH, "/html/body/div[2]/div[1]/section[2]/div/div/div/div[2]/table/tbody/tr"))
    for i in range(1, length+1):
        dct = {}
        try:
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/section[2]/div/div/div/div[2]/table/tbody/tr[{}]/td[10]/a".format(i)).click()
            dct["Product Name"] = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[1]/div/div[1]/input').get_attribute('value')
            dct["Product Slug"] = driver.find_element(By.XPATH, '//*[@id="slug"]').get_attribute('value')
            dct["Product Sequence"] = driver.find_element(By.XPATH, '//*[@id="sequence"]').get_attribute('value')
            dct["Product Price"] = driver.find_element(By.XPATH, '//*[@id="price"]').get_attribute('value')
            dct["Product Offer Price"] = driver.find_element(By.XPATH, '//*[@id="offer_price"]').get_attribute('value')
            dct["Product SKU"] = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[4]/div/div[1]/input').get_attribute('value')
            s1 = Select(driver.find_element(By.XPATH, '//*[@id="is_featured"]'))
            dct["Product Is Featured"] = s1.first_selected_option.text
            s2 = Select(driver.find_element(By.XPATH, '//*[@id="brand"]'))
            dct["Product Brand"] = s2.first_selected_option.text
            s3 = Select(driver.find_element(By.XPATH, '//*[@id="tax"]'))
            dct["Product Tax"] = s3.first_selected_option.text
            dct["Product Short Description"] = driver.find_element(By.XPATH, '//*[@id="short_description"]').get_attribute("innerHTML")
            dct["Product Description"] = driver.find_element(By.XPATH, '//*[@id="description"]').get_attribute("innerHTML")
            dct["Product Image"] = driver.find_element(By.XPATH, '//*[@id="tab1"]/div[8]/a/img').get_attribute('src')
            dct["Product URL"] = driver.current_url
            try:
                n = dct["Product Image"].rfind('/')
                urllib.request.urlretrieve(dct["Product Image"], r"{}\{}".format(download_path, dct["Product Image"][n+1:]))
                dct["Image Local Path"] = r"{}\{}".format(download_path, dct["Product Image"][n+1:])
            except Exception as err:
                print(err)
            dct["Thumb Image"]= driver.find_element(By.XPATH, '//*[@id="tab1"]/div[9]/a/img').get_attribute('src')
            try:
                n = dct["Thumb Image"].rfind('/')
                urllib.request.urlretrieve(dct["Thumb Image"], r"{}\{}".format(download_path, dct["Thumb Image"][n+1:]))
                dct["Thumb Image Local Path"] = r"{}\{}".format(download_path, dct["Thumb Image"][n+1:])
            except Exception as err:    
                print(err)
            dct["Zoom Image"]= driver.find_element(By.XPATH, '//*[@id="tab1"]/div[10]/a/img').get_attribute('src')
            try:
                n = dct["Zoom Image"].rfind('/')
                urllib.request.urlretrieve(dct["Zoom Image"], r"{}\{}".format(download_path, dct["Zoom Image"][n+1:]))
                dct["Zoom Image Local Path"] = r"{}\{}".format(download_path, dct["Zoom Image"][n+1:])
            except Exception as err:
                print(err)
            try:
                driver.find_element(By.XPATH, '//*[@id="choice_form"]/div/ul/li[2]/a').click()
                ss = driver.find_element(By.XPATH, '//*[@id="tab2"]/script[5]').get_attribute("innerHTML")
                lst = getData(ss)
                dct["categories"] = []
                for num in lst:
                    dct["categories"].append(driver.find_element(By.XPATH, f"//*[@data-value={num}]").text.split("\n")[0])
            except Exception as err:
                print(err)
            driver.back()
            table.append(dct)
        except NoSuchElementException as err:
            print(err)
    try:
        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/section[2]/div/div/div/div[2]/div/nav/ul/li[15]/a").click()
    except Exception as err:
        print(err)
        break
df = pd.DataFrame(table)
_time = datetime.datetime.now()
csv_file_name = str(datetime.datetime.timestamp(_time)) + "table.csv"
df.to_csv(str(csv_file_name))
driver.close()


# //li[@data-value="334"]/text()