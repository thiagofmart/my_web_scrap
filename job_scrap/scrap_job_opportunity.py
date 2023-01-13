import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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


    def extract_data_from_opportunity(self, li):
        links = li.find_elements('tag name', 'a')
        link_oferta = links[1]
        link_oferta.send_keys(Keys.CONTROL + Keys.RETURN)
        tab_windows = self.browser.window_handles
        self.browser.switch_to.window(tab_windows[1])
        enterprise=''
        while enterprise=='':
            enterprise = self.browser.find_element('css selector', '[class="jobs-unified-top-card__company-name"]').text
            location = self.browser.find_element('css selector', '[class="jobs-unified-top-card__bullet"]').text
        self.browser.find_element('css selector', '[aria-label="Clicar para ver mais detalhes"]').click()
        desc = self.browser.find_element('css selector', '[id="job-details"]').text
        if 'R$' in desc:
            ind = desc.find('R$')
            wage = desc[ind:ind+10].replace('.', '').replace('R$', '')
            for character in wage:
                if not character.isdigit() and character!=',':
                    wage = wage.replace(character, '')
            wage = wage.replace(',', '.')
            wage = float(wage)
        else:
            wage = self.browser.find_element('css selector', '[id="SALARY"]').text
            wage = wage.split('\n')[0]

        while len(tab_windows) >= 2:  #close new tab
            self.browser.close()
            tab_windows = self.browser.window_handles
        self.browser.switch_to.window(tab_windows[0])
        sleep(1)
        return location, desc, enterprise, wage


    def scrap_opportunities(self, role, location):
        self.browser.get(f'https://www.linkedin.com/jobs/search/')
        self.browser.find_element('css selector', '[id="jobs-search-box-keyword-id-ember31"]').send_keys(role)
        self.browser.find_element('css selector', '[id="jobs-search-box-location-id-ember31"]').send_keys(Keys.CONTROL + 'a')
        self.browser.find_element('css selector', '[id="jobs-search-box-location-id-ember31"]').send_keys(Keys.DELETE)
        self.browser.find_element('css selector', '[id="jobs-search-box-location-id-ember31"]').send_keys(location)
        sleep(1.5)
        self.browser.find_element('css selector', '[id="jobs-search-box-location-id-ember31"]').send_keys(Keys.ENTER)
        sleep(1.5)
        results = self.browser.find_element('css selector', '[class="jobs-search-results__list list-style-none"]')
        list_li = results.find_elements('tag name', 'li')
        for li in list_li:
            if 'ember' in li.get_attribute('id'):
                self.browser.execute_script("arguments[0].scrollIntoView();", li)
                location, desc, enterprise, wage = self.extract_data_from_opportunity(li)
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
catho.scrap_opportunities(role='faturista')
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
        buttons = self.browser.find_elements('css selector', '[rel="nofollow"]')
        pgs = int(buttons[-3].text)
        for pg in range(1, int(pgs)):
            sleep(1)
            results = self.browser.find_element('css selector', '[id="search-result"]')
            list_li = results.find_elements('tag name', 'li')
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

class Vagas():
    """
USAGE:
vagas = Vagas(browser)
vagas.log(email='thiago.fm2@hotmail.com', password='thiago.fm2')
vagas.scrap_opportunities(role='faturista')
    """
    def __init__(self, browser):
        self.browser = browser
        self.df = pd.DataFrame(columns='ENTERPRISE LOCATION WAGE DESC'.split())


    def log(self, email, password):
        self.browser.get('https://www.vagas.com.br/login-candidatos')
        self.browser.find_element('css selector', '[id="login_candidatos_form_usuario"]').send_keys(email)
        self.browser.find_element('css selector', '[id="login_candidatos_form_senha"]').send_keys(password)
        sleep(2)
        self.browser.find_element('css selector', '[id="login_candidatos_form_senha"]').send_keys(Keys.ENTER)


    def extract_data_from_opportunity(self, li):
        li.find_element('tag name', 'a').send_keys(Keys.CONTROL + Keys.RETURN) #open on new tab
        tab_windows = self.browser.window_handles
        self.browser.switch_to.window(tab_windows[1])
        enterprise = ''
        while enterprise == '':
            location  = self.browser.find_element('css selector', '[class="info-localizacao"]').text
            desc = self.browser.find_element('css selector', '[data-testid="JobDescription"]').text
            enterprise = self.browser.find_element('css selector', '[class="job-shortdescription__company"]').text
            wage = self.browser.find_element('xpath', '/html/body/div[1]/section[2]/main/article/header/div/ul/li[1]/div').text
        while len(tab_windows) >= 2:  #close new tab
            self.browser.close()
            tab_windows = self.browser.window_handles
        self.browser.switch_to.window(tab_windows[0])
        sleep(1)
        return location, desc, enterprise, wage

    def scrap_opportunities(self, role, location=''):
        self.browser.get(f'https://www.vagas.com.br/meu-perfil')
        self.browser.find_element('css selector', '[aria-label="Busca de cargos"]').send_keys(role)
        self.browser.find_element('css selector', '[aria-label="Busca de cidades"]').send_keys(location)
        self.browser.find_element('xpath', '/html/body/div[1]/div/header/div[1]/div[3]/div/section/div/div[3]/button').click()
        ul = self.browser.find_element('css selector', '[id="todasVagas"]')
        list_li = ul.find_elements('tag name', 'li')
        for li in list_li:
            location, desc, enterprise, wage = self.extract_data_from_opportunity(li)
            dct = {
            'ENTERPRISE':enterprise,
            'LOCATION':location,
            'WAGE':wage,
            'DESC':desc,
            }
            df_dictionary = pd.DataFrame([dct])
            self.df = pd.concat([self.df, df_dictionary], ignore_index=True)


def test_linkedin(email, password):
    global linkedin
    linkedin = Linkedin(browser)
    linkedin.log(email=email, password=password)
    linkedin.scrap_opportunities(role='faturista', location='São Paulo')
    linkedin.df.to_excel('./OUTPUT/linkedin_data.xlsx')

def test_catho(email, password):
    global catho
    catho = Catho(browser)
    catho.log(email=email, password=password)
    sleep(0.5)
    catho.scrap_opportunities(role='faturista', location='São Paulo - SP')
    catho.df.to_excel('./OUTPUT/catho_data.xlsx')

def test_vagas(email, password):
    global vagas
    vagas = Vagas(browser)
    vagas.log(email=email, password=password)
    sleep(0.5)
    vagas.scrap_opportunities(role='faturista', location='São Paulo - SP')
    vagas.df.to_excel('./OUTPUT/vagas_data.xlsx')
