from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Mobile:
    def __init__(self, name: str, attribs: dict):
        self.name = name
        self.price = []
        self.urls = []
        self.UP = {}
        self.attrs = attribs


def scrape_mobile():
    mobiles = {}

    # base_site
    torob = webdriver.Chrome('chromedriver.exe')
    torob.get(
        'https://torob.com/browse/94/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-mobile/')
    for i in range(1, 6):
        attribs = {}
        # getting_names
        phone_xpath = f'//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div[{i}]/a/div/h2'
        phone_name = torob.find_elements(By.XPATH, phone_xpath)
        name = phone_name[0].text.split("|")[0]
        name_word_list = name.split(" ")
        new_name = ""
        for word in name_word_list:
            if word.isascii() == False:
                name_word_list.remove(word)
            else:
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

        mobiles[new_name] = Mobile(new_name, attribs)
        # model_instance = product(name=new_name, price=mobiles[new_name].price, urls=mobiles[new_name].urls)
        # model_instance.save()
        torob.get(
            'https://torob.com/browse/94/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-mobile/')
        
        sleep(2)
    torob.close()

    # first_site
    digikala = webdriver.Chrome('chromedriver.exe')
    price_digikala = []
    for name in mobiles.keys():
        url = name.replace(" ", "%20")
        try:
            digikala.get(
                f'https://www.digikala.com/search/mobile-phone/?q={url}')
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
                    mobiles[name].price.append(price)
                except:
                    break
                # appending_product_link
                try:
                    link_xpath = f'''//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a'''
                    link = digikala.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    mobiles[name].urls.append(link)
                except:
                    pass
                # model_instance = product(name=name, price=mobiles[new_name].price, urls=mobiles[new_name].urls)
                # model_instance.save()
        except:
            pass
    digikala.close()

    # second_site
    divar = webdriver.Chrome('chromedriver.exe')
    divar.get(f'https://divar.ir/s/tehran/mobile-phones/')
    searchbar_xpath = '''//*[@id="app"]/header/nav/div/div[2]/div/div/div[1]/form/input'''
    searchbar = divar.find_elements(By.XPATH, searchbar_xpath)

    for name in mobiles.keys():
        try:
            searchbar[0].send_keys(name)
            searchbar[0].send_keys(Keys.RETURN)
            sleep(2)
            for i in range(1, 6):

                # appending_product_prices
                try:
                    price_xpath = f'''//*[@id="app"]/div[2]/main/div[2]/div/div/div/div[{i}]/a/article/div/div[1]/div[2]'''
                    price = divar.find_elements(By.XPATH, price_xpath)
                    price = price[0].text
                    price = price.split(" ")[0]
                    mobiles[name].price.append(price)
                except:
                    break

                # appending_product_urls
                try:
                    link_xpath = f'''//*[@id="app"]/div[2]/main/div[2]/div/div/div/div[{i}]/a'''
                    link = divar.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    mobiles[name].urls.append(link)
                except:
                    pass
            divar.back()
            sleep(2)
        except:
            pass
    divar.close()

    # third_site
    kimia_online = webdriver.Chrome('chromedriver.exe')
    for name in mobiles.keys():
        url = name.replace(" ", "%20")
        try:
            kimia_online.get(
                f'https://www.kimiaonline.com/catalog/search?q={url.lower()}&category=||category:%da%af%d9%88%d8%b4%db%8c+%d9%85%d9%88%d8%a8%d8%a7%db%8c%d9%84!!2!!&as=false&isc=false&sid=true')
            sleep(3)
            for i in range(1, 6):

                # appending_product_prices
                try:
                    price_xpath = f'''//*[@id="km-search"]/div[3]/section/div/div[4]/div/div[2]/section[1]/section/div[{i}]/div[2]/div[3]/div[2]/div[2]/span'''
                    price = kimia_online.find_elements(By.XPATH, price_xpath)
                    price = price[0].text
                    price = price.split(" ")[0]
                    mobiles[name].price.append(price)
                except:
                    break

                # appending_product_urls
                try:
                    link_xpath = f'''//*[@id="km-search"]/div[3]/section/div/div[4]/div/div[2]/section[1]/section/div[{i}]/div[1]/a'''
                    link = kimia_online.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    mobiles[name].urls.append(link)
                except:
                    pass
                # model_instance = product(name=name, price=mobiles[new_name].price, urls=mobiles[new_name].urls)
                # model_instance.save()
        except:
            pass
    kimia_online.close()

    for mobile in mobiles.values():
        mobile.UP = dict(zip(mobile.urls, mobile.price))
    return mobiles
