from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re



class WashingMachine:
    def __init__(self, name: str, attribs: dict):
        self.name = name
        self.price = []
        self.urls = []
        self.attrs = attribs


def scrape_washing_machine():
    torob = webdriver.Chrome('chromedriver.exe')
    torob.get('https://torob.com/browse/201/%D9%85%D8%A7%D8%B4%DB%8C%D9%86-%D9%84%D8%A8%D8%A7%D8%B3-%D8%B4%D9%88%DB%8C%DB%8C-washing-machine/')
    # torob.minimize_window()
    washing_machines = {}

    # base_site
    pattern1 = re.compile(r'\d\s?kg', re.IGNORECASE)
    pattern2 = re.compile(r'washing machine', re.IGNORECASE)
    for i in range(1, 6):
        attribs = {}

        # getting_names
        wm_xpath = f'//*[@id="layout-wrapp"]/div[2]/div/div[2]/div[2]/div[3]/div/div/div[{i}]/a/div/h2'
        tablet_name = torob.find_elements(By.XPATH, wm_xpath)
        name = tablet_name[0].text.split("ا")[-1]
        name_word_list = name.split(" ")
        new_name = ""
        for word in name_word_list:
            if word.isascii() == True:
                new_name += word+" "
        matches1 = pattern1.finditer(new_name)
        for match in matches1:
            d = new_name[match.span()[0]: match.span()[1]]
            new_name = new_name.replace(d, "")
        matches2 = pattern2.finditer(new_name)
        for match in matches2:
            d = new_name[match.span()[0]: match.span()[1]]
            new_name = new_name.replace(d, "")

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

        washing_machines[new_name] = WashingMachine(new_name, attribs)

        torob.get('https://torob.com/browse/201/%D9%85%D8%A7%D8%B4%DB%8C%D9%86-%D9%84%D8%A8%D8%A7%D8%B3-%D8%B4%D9%88%DB%8C%DB%8C-washing-machine/')
        sleep(2)
    torob.close()

    # first_site
    digikala = webdriver.Chrome('chromedriver.exe')
    for name in washing_machines.keys():
        url = name.replace(" ", "%20")
        inner_price_list2 = []
        try:
            digikala.get(
                f'https://www.digikala.com/search/washing-machines/?q={url}')
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
                    washing_machines[name].price.append(price)
                    inner_price_list2.append(price)
                except:
                    break
                # appending_product_link
                try:
                    link_xpath = f'''//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a'''
                    link = digikala.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    washing_machines[name].urls.append(link)
                except:
                    pass
                washing_machines[new_name] = WashingMachine(new_name, attribs)

        except:
            pass
    digikala.close()

    # second_site
    divar = webdriver.Chrome('chromedriver.exe')
    divar.get(f'https://divar.ir/s/tehran/washing-machines/')
    searchbar_xpath = '''//*[@id="app"]/header/nav/div/div[2]/div/div/div[1]/form/input'''
    searchbar = divar.find_elements(By.XPATH, searchbar_xpath)
    for name in washing_machines.keys():
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
                    washing_machines[name].price.append(price)
                except:
                    break
                # appending_product_urls
                try:
                    link_xpath = f'''//*[@id="app"]/div[2]/main/div[1]/div/div/div/div[{i}]/a'''
                    link = divar.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    washing_machines[name].urls.append(link)
                except:
                    pass
                washing_machines[new_name] = WashingMachine(new_name, attribs)

            divar.back()
            sleep(2)
        except:
            pass
    divar.close()

    # third_site
    torob = webdriver.Chrome('chromedriver.exe')
    p = re.compile(r'[۰-۹]*٫?[۰-۹]*٫[۰-۹]*')

    for name in washing_machines.keys():
        url = name.replace(" ", "%20")
        try:
            torob.get(f'https://torob.com/search/?query={url}')
            sleep(2)
            for i in range(1, 6):
                # appending_product_price
                try:
                    price_xpath = f'''//*[@id="layout-wrapp"]/div[2]/div/div/div[2]/div[2]/div/div/div[{i}]/a/div/div[3]'''
                    price = torob.find_elements(By.XPATH, price_xpath)
                    price = price[0].text
                    matches = p.finditer(price)
                    for match in matches:
                        price = match.group(0)
                    washing_machines[name].price.append(price)
                except:
                    break
                # appending_product_link
                try:
                    link_xpath = f'''//*[@id="layout-wrapp"]/div[2]/div/div/div[2]/div[2]/div/div/div[{i}]/a'''
                    link = torob.find_elements(By.XPATH, link_xpath)
                    link = link[0].get_attribute("href")
                    washing_machines[name].urls.append(link)
                except:
                    pass
                washing_machines[new_name] = WashingMachine(new_name, attribs)

        except:
            pass
    torob.close()

    for wm in washing_machines.values():
        wm.UP = dict(zip(wm.urls, wm.price))


    return washing_machines
