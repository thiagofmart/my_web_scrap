import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from time import sleep
import unidecode


sites = ["linkedin", "catho", "infojobs", "empregos.com.br", "sine", "vagas.com", "indeed.com.br", "ciee", "emprega brasil"]

browser = Firefox()
browser.implicitly_wait(10)


class Linkedin():
    """
USAGE:
linkedin = Linkedin(browser)
linkedin.log(email='', password='')
linkedin.scrap_opportunities(role='faturista')
print(linkedin.df)
    """
    def __init__(self, browser):
        self.browser = browser
        self.df = pd.DataFrame(columns='ENTERPRISE LOCATION WAGE DESC'.split())


    def log(self, email, password):
        self.browser.get('https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        self.browser.find_element('css selector', '[id="username"]').send_keys(email)
        self.browser.find_element('css selector', '[id="password"]').send_keys(password)
        self.browser.find_element('css selector', '[aria-label="Entrar"]').click()


    def extract_data_from_opportunity(self):
        enterprise = self.browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]').text
        location = self.browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]').text
        desc = self.browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[2]').text
        if 'R$' in desc:
            ind = desc.find('R$')
            wage = desc[ind:ind+10].replace('.', '').replace('R$', '')
            for character in wage:
                if not character.isdigit() and character!=',':
                    wage = wage.replace(character, '')
            wage = wage.replace(',', '.')
            wage = float(wage)
        else:
            wage = self.browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[3]/div/h2').text
        return location, desc, enterprise, wages


    def scrap_opportunities(self, role):
        self.browser.get(f'https://www.linkedin.com/jobs/search/?geoId=105871508&keywords={role}&location=S%C3%A3o%20Paulo%2C%20Brasil')
        sleep(1.5)
        ul = self.browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul')
        list_li = ul.find_elements('tag name', 'li')
        for li in list_li:
            sleep(1.5)
            if not '\n' in li.text:
                pass
            else:
                links = li.find_elements('tag name', 'a')
                if len(links)>0:
                    link_oferta = links[0]
                    link_oferta.click()
                    try:
                        location, desc, enterprise, wage = self.extract_data_from_opportunity()
                    except:
                        location, desc, enterprise, wage = None, None, None, None
                    dct = {
                    'ENTERPRISE':enterprise,
                    'LOCATION':location,
                    'WAGE':wage,
                    'DESC':desc,
                    }
                    df_dictionary = pd.DataFrame([dct])
                    self.df = pd.concat([self.df, df_dictionary], ignore_index=True)

class Catho():
    """
USAGE:
catho = Catho(browser)
catho.log(email='', password='')
catho.scrap_opportunities(self, role='faturista')
    """
    def __init__(self, browser):
        self.browser = browser
        self.df = pd.DataFrame(columns='ENTERPRISE LOCATION WAGE DESC'.split())


    def log(self, email, password):
        self.browser.get('https://seguro.catho.com.br/signin/')
        sleep(2)
        popup = self.browser.find_elements('xpath', '/html/body/div[2]/div/div[2]/section/div/div[3]/div[1]/button')
        if len(popup)>0:
            popup[0].click()
        self.browser.find_element('css selector', '[type="email"]').send_keys(email)
        self.browser.find_element('css selector', '[type="password"]').send_keys(password)
        self.browser.find_element('css selector', '[type="submit"]').click()


    def extract_data_from_opportunity(self, li):
        self.browser.implicitly_wait(2.5)
        popup = self.browser.find_elements('css selector', '[id="apply-modal-ok-button"]')
        self.browser.implicitly_wait(10)
        if len(popup)>0:
            popup[0].click()
        li.click()
        sleep(1)
        enterprise = li.find_element('xpath', './article/article/header/div/p').text
        wage = li.find_element('xpath', './article/article/header/div/div[2]/div[1]').text
        desc = li.find_element('xpath', './article/article/div/div[1]/span').text
        location = li.find_element('xpath', './article/article/header/div/div[2]/button/a').text
        li.find_element('xpath', './article/article/div/div[1]/button').click()
        return location, desc, enterprise, wage


    def scrap_opportunities(self, role, location=''):
        self.browser.get(f'https://www.catho.com.br/vagas/')
        self.browser.find_element('css selector', '[id="keyword"]').send_keys(role)
        self.browser.find_element('css selector', '[id="location"]').send_keys(location)
        self.browser.find_element('css selector', '[id="downshift-1-item-0"]').click()
        self.browser.find_element('css selector', '[title="Buscar vagas"]').click()
        sleep(1.5)
        pgs = self.browser.find_element('xpath', '/html/body/div[1]/div[4]/main/div[3]/div/div/section/div[2]/nav/a[6]').text
        for pg in range(1, int(pgs)):
            sleep(1)
            ul = self.browser.find_element('xpath', '/html/body/div[1]/div[4]/main/div[3]/div/div/section/ul')
            list_li = ul.find_elements('tag name', 'li')
            scroll=0
            for li in list_li:
                if '\n' in li.text:
                    self.browser.execute_script(f"window.scrollTo(0, {scroll})")
                    scroll+=300
                    try:
                        location, desc, enterprise, wage = self.extract_data_from_opportunity(li)
                    except:
                        location, desc, enterprise, wage = None, None, None, None
                    dct = {
                    'ENTERPRISE':enterprise,
                    'LOCATION':location,
                    'WAGE':wage,
                    'DESC':desc,
                    }
                    df_dictionary = pd.DataFrame([dct])
                    self.df = pd.concat([self.df, df_dictionary], ignore_index=True)
            sleep(1)
            self.browser.implicitly_wait(2.5)
            popup = self.browser.find_elements('css selector', '[id="apply-modal-ok-button"]')
            self.browser.implicitly_wait(10)
            if len(popup)>0:
                sleep(2)
                popup[0].click()
            buttons = self.browser.find_elements('css selector', '[rel="nofollow"]')
            for button in buttons:
                if button.text == 'Próximo':
                    button.click()
                    break

def test_linkedin(email, password):
    global linkedin
    linkedin = Linkedin(browser)
    linkedin.log(email=email, password=password)
    linkedin.scrap_opportunities(role='faturista', location='São Paulo - SP')
    linkedin.df.to_excel('./linkedin_data.xlsx')

def test_catho(email, password):
    global catho
    catho = Catho(browser)
    catho.log(email=email, password=password)
    sleep(0.5)
    catho.scrap_opportunities(role='faturista', location='São Paulo - SP')
    catho.df.to_excel('./catho_data.xlsx')
