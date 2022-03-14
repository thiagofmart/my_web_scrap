import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from time import sleep


sites = ["linkedin", "catho", "infojobs", "empregos.com.br", "sine", "vagas.com", "indeed.com.br", "ciee", "emprega brasil"]
email='thiago.fm2@hotmail.com'
common_pass = 'thiago.fm2'
df = pd.DataFrame(columns=['LOCAL', 'VALOR', 'EMPRESA'])

browser = Firefox()
browser.implicitly_wait(15)
cargo = 'Faturista'
local = 'São Paulo, Brasil'


def log_linkedin(browser):
    browser.get('https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    browser.find_element('css selector', '[id="username"]').send_keys(email)
    browser.find_element('css selector', '[id="password"]').send_keys(common_pass)
    browser.find_element('css selector', '[aria-label="Entrar"]').click()

def linkedin_extract_data_from_opportunity(browser):
    empresa = browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]').text
    local = browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]').text
    desc = browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[2]').text
    if 'R$' in desc:
        ind = desc.find('R$')
        salario = desc[ind:ind+10].replace('.', '').replace('R$', '')
        for character in salario:
            if not character.isdigit() and character!=',':
                salario = salario.replace(character, '')
        salario = salario.replace(',', '.')
        salario = float(salario)
    else:
        salario = browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[3]/div/h2').text
    return local, desc, empresa, salario

def scrap_linkedin(browser, cargo):
    global df
    df = pd.DataFrame(columns='EMPRESA LOCAL SALARIO DESC'.split())
    browser.get(f'https://www.linkedin.com/jobs/search/?geoId=105871508&keywords={cargo}&location=S%C3%A3o%20Paulo%2C%20Brasil')
    sleep(1.5)
    ul = browser.find_element('xpath', '/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul')
    list_li = ul.find_elements('tag name', 'li')
    for li in list_li:
        sleep(1.5)
        if not '\n' in li.text:
            pass
        else:
            pprint(li.text)
            try:
                links = li.find_elements('tag name', 'a')
                link_oferta = links[0]
                link_oferta.click()
                local, desc, empresa, salario = linkedin_extract_data_from_oportunit(browser)
                link_empresa = links[-1]
                dct = {
                'EMPRESA':empresa,
                'LOCAL':local,
                'SALARIO':salario,
                'DESC':desc,
                }
                df_dictionary = pd.DataFrame([dct])
                df = pd.concat([df, df_dictionary], ignore_index=True)
            except:
                pass
    return df
