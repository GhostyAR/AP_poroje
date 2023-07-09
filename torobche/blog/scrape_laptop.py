from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Laptop:
    def __init__(self, name: str, attribs: dict):
        self.name = name
        self.price = []
        self.urls = []
        self.UP = {}
        self.attrs = attribs


def scrape_laptop():
    laptops = {}

    torob = webdriver.Chrome('chromedriver.exe')
    torob.get('https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop/')
    # torob.minimize_window()

    for i in range(1, 6):
        attribs = {}

        # getting_names
        laptop_xpath = f'//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div[{i}]/a/div/h2'
        laptop_name = torob.find_elements(By.XPATH, laptop_xpath)
        name = laptop_name[0].text.split("|")[0]
        name_word_list = name.split(" ")
        new_name = ""
        for word in name_word_list:
            if word.isascii() == True:
                new_name += word+" "
        new_name = new_name.removesuffix("  ")

        # getting_product_attributes
        link_xpath = f'''//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div[{i}]/a'''
        link = torob.find_elements(By.XPATH, link_xpath)
        link[0].click()
        sleep(2)
        for j in range(2, 12):
            key_xpath = f'''//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[4]/div/div/div/div[{j}]/div[1]'''
            value_xpath = f'''//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[4]/div/div/div/div[{j}]/div[2]'''
            key = torob.find_elements(By.XPATH, key_xpath)[0].text
            value = torob.find_elements(By.XPATH, value_xpath)[0].text
            attribs[key] = value

        laptops[new_name] = Laptop(new_name, attribs)
        torob.get(
            'https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop/')
        sleep(2)
    torob.close()

    # first_site
    digikala = webdriver.Chrome('chromedriver.exe')
    for name in laptops.keys():
        url = name.replace(" ", "%20")
        try:
            digikala.get(f'https://www.digikala.com/search/laptop/?q={url}')
            sleep(3)
            for i in range(1, 6):
                # appending_product_price
                try:
                    price_xpath = f'''//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div/span'''
                    price = digikala.find_elements(By.XPATH, price_xpath)
                    if "٪" in price[0].text:
                        price_xpath = f'''//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div[2]/span'''
                        price = digikala.find_elements(By.XPATH, price_xpath)
                    price = price[0].text
                    laptops[name].price.append(price)
                except:
                    break
                # appending_product_link
                try:
                    link_xpath = f'''//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a'''
                    link = digikala.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    laptops[name].urls.append(link)
                except:
                    pass
        except:
            pass
    digikala.close()
    # 1m 26.3s

    # second_site
    divar = webdriver.Chrome('chromedriver.exe')
    divar.get(f'https://divar.ir/s/tehran/laptop-notebook-macbook')
    searchbar_xpath = '''//*[@id="app"]/header/nav/div/div[2]/div/div/div[1]/form/input'''
    searchbar = divar.find_elements(By.XPATH, searchbar_xpath)
    for name in laptops.keys():
        try:
            searchbar[0].send_keys(name)
            searchbar[0].send_keys(Keys.RETURN)
            sleep(2)
            for i in range(1, 6):
                # appending_product_prices
                try:
                    price_xpath = f'''//*[@id="app"]/div[2]/main/div[1]/div/div/div/div[{i}]/a/article/div/div[1]/div[2]'''
                    price = divar.find_elements(By.XPATH, price_xpath)
                    price = price[0].text
                    price = price.split(" ")[0]
                    laptops[name].price.append(price)
                except:
                    break
                # appending_product_urls
                try:

                    link_xpath = f'''//*[@id="app"]/div[2]/main/div[1]/div/div/div/div[{i}]/a'''
                    link = divar.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    laptops[name].urls.append(link)
                except:
                    pass
            divar.back()
            sleep(2)
        except:
            pass
    divar.close()

    # third_site
    toprayan = webdriver.Chrome('chromedriver.exe')
    price_kimia_online = []
    for name in laptops.keys():
        url = name.replace(" ", "+")
        try:
            toprayan.get(
                f'https://toprayan.com/category/laptop-and-ultrabook/list?SearchKey={url}&search-top=')
            sleep(3)
            for i in range(1, 6):
                try:
                    price_xpath = f'''//*[@id="listing-result"]/div[1]/div/div[{i}]/div/div/div[2]/div/div[2]/div'''
                    price = toprayan.find_elements(By.XPATH, price_xpath)
                    price = price[0].text.split(" ")[0]
                    laptops[name].price.append(price)
                except:
                    break
                try:
                    link_xpath = f'''//*[@id="listing-result"]/div[1]/div/div[{i}]/div/a'''
                    link = toprayan.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    laptops[name].urls.append(link)
                except:
                    pass
        except:
            pass
    toprayan.close()

    for laptop in laptops.values():
        laptop.UP = dict(zip(laptop.urls, laptop.price))
    return laptops
