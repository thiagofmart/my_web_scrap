from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from anticaptchaofficial.recaptchav2enterpriseproxyless import *
from selenium.webdriver.common.by import By
import pandas as pd


#### NORTE
class AC:
    pass
class AP:
    pass
class AM:
    pass
class PA:
    pass
class RO:
    pass
class RR:
    pass
class TO:
    pass

#### NORDESTE
class AL:
    pass
class BA:
    pass
class CE:
    pass
class MA:
    pass
class PB:
    pass
class PE:
    pass
class PI:
    pass
class RN:
    pass
class SE:
    pass
class SP:
    def consultar_divida_ativa(driver, tipo_pesquisa: str, valor: str, tipo_debito: str|None = None):
        driver.get("https://www.dividaativa.pge.sp.gov.br/sc/pages/consultas/consultarDebito.jsf")
        # input 1
        driver._select_option(
            select_element=driver.find_element(By.ID, 'consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa'), 
            option_value=tipo_pesquisa,
            )
        sleep(2) # <-- CORRIGIR ESSE SLEEP E COLOCAR UM WEBDRIVERWAIT NO LUGAR
        # input 2
        value_span = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div[2]/span/form/span/div/div[2]/table/tbody/tr/td[1]/div/span/div/span")
        value_span.find_element(By.TAG_NAME, "input").send_keys(valor)

        # input 3 (optional)
        if tipo_debito:
            driver._select_option(
                select_element=driver.find_element(By.ID, 'consultaDebitoForm:decTxtTipoConsulta:tiposDebitosCnpj'), 
                option_value=tipo_debito,
                )
        
        solution = driver.solve_captcha(
            url="https://www.dividaativa.pge.sp.gov.br/sc/pages/consultas/consultarDebito.jsf",
            captcha_key = driver.find_element(By.ID, "recaptcha").get_attribute("data-sitekey"),
            solver = recaptchaV2EnterpriseProxyless(),
            input_id = "g-recaptcha-response",
            )
        if solution:
            driver.find_element(By.XPATH, '//*[@id="consultaDebitoForm:j_id64_body"]/div[2]/input[2]').click()
            html_table = driver.find_element(By.ID, "consultaDebitoForm:consultaDebitoSearchResultBlock").get_attribute("innerHTML")
            extracted_list = pd.read_html(html_table)
            df = extracted_list[0]
            assert type(df) == pd.DataFrame, "Erro ao extrair Divida Ativa SP"
            return df
#### SUDESTE
class ES:
    pass
class MG:
    pass
class RJ:
    pass
class SP:
    pass

#### SUL
class PR:
    pass
class RS:
    pass
class SC:
    pass

#### CENTRO-OESTE
class DF:
    pass
class GO:
    pass
class MT:
    pass
class MS:
    pass
    