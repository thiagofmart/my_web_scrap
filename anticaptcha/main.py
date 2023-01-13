from selenium.webdriver.common.by import By
from time import sleep
from utils import *
from anticaptchaofficial.recaptchav2enterpriseproxyless import *


def _select_option(select_element, option_value: str, case_sensitive: bool = False):
    options_elements = select_element.find_elements(By.TAG_NAME, "option")
    if case_sensitive:
        options_values = [option.get_attribute("value") for option in options_elements]
    else:
        option_value = option_value.upper()
        options_values = [option.get_attribute("value").upper() for option in options_elements]
        
    if option_value in options_values:
        options_elements[options_values.index(option_value)].click() 
    else:
        raise Exception(f'Opção Inválida!\n\nA opção: "{option_value}" não foi encontrado na lista de opções')


def solve_captcha(url, captcha_key, solver, input_id):
    solver.set_verbose(1)
    solver.set_key("")
    solver.set_website_url(url)
    solver.set_website_key(captcha_key)
    solution = solver.solve_and_return_solution()
    if solution:
        print(solution)
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{solution}'")
        return solution
    else:
        print(solution.err_string)
        return solver.err_string

def consultar(tipo_pesquisa: str, valor: str, tipo_debito: str|None = None):
    driver.get("https://www.dividaativa.pge.sp.gov.br/sc/pages/consultas/consultarDebito.jsf")
    # input 1
    _select_option(
        select_element=driver.find_element(By.ID, 'consultaDebitoForm:decLblTipoConsulta:opcoesPesquisa'), 
        option_value=tipo_pesquisa,
        )
    sleep(2)
    # input 2
    value_span = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div[2]/span/form/span/div/div[2]/table/tbody/tr/td[1]/div/span/div/span")
    value_span.find_element(By.TAG_NAME, "input").send_keys(valor)

    # input 3 (optional)
    if tipo_debito:
        _select_option(
            select_element=driver.find_element(By.ID, 'consultaDebitoForm:decTxtTipoConsulta:tiposDebitosCnpj'), 
            option_value=tipo_debito,
            )
    solution = solve_captcha(
        url="https://www.dividaativa.pge.sp.gov.br/sc/pages/consultas/consultarDebito.jsf",
        captcha_key = driver.find_element(By.ID, "recaptcha").get_attribute("data-sitekey"),
        solver = recaptchaV2EnterpriseProxyless(),
        input_id = "g-recaptcha-response"
        )
    if solution:
        driver.find_element(By.XPATH, '//*[@id="consultaDebitoForm:j_id64_body"]/div[2]/input[2]').click()

if __name__=="__main__":
    # PROXY não estava funcionando no GeckoDriver
    # https://hidemy.name/en/proxy-list/?type=s#list
    api_key = ""
    IP = "185.231.114.140"
    PORT = "8585"
    PROXY = "{IP}:{PORT}"
    driver = create_driver() 
    driver.implicitly_wait(5)
    # test_proxy(IP)
    # consultar("CNPJ", "06330557000177")














