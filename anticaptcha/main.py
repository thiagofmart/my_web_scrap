from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
import Extractor
class PERF_webdriver(Chrome):
    def __init__(self, PROXY: None|str = None,configure_proxy: bool = False, **kwargs):
        options = ChromeOptions()
        # Configurando o PROXY (se tiver)
        if configure_proxy and not PROXY: options.add_argument(f"--proxy-server={os.environ.get('PROXY')}")
        if configure_proxy and PROXY: options.add_argument(f"--proxy-server={PROXY}")
        super().__init__(
            service=Service(ChromeDriverManager().install()),
            options=options,
            **kwargs
            )
        self.implicitly_wait(5)
    
    def _select_option(self, select_element: WebElement, option_value: str, case_sensitive: bool = False):
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

    def solve_captcha(self, url, captcha_key, solver, input_id):
        solver.set_verbose(1)
        solver.set_key("6da5a1ce1fc268eacca71af38627e55d")
        solver.set_website_url(url)
        solver.set_website_key(captcha_key)
        solution = solver.solve_and_return_solution()
        if solution:
            print(solution)
            driver.execute_script(f"document.getElementById('{input_id}').innerHTML = '{solution}'")
            return solution
        else:
            print(solution.err_string)
            if type(solver)==int:
                raise Exception("Invalid API Key")
            return solver.err_string


if __name__=="__main__":
    # PROXY não estava funcionando no GeckoDriver
    # https://hidemy.name/en/proxy-list/?type=s#list
    api_key = ""
    IP = "185.231.114.140"
    PORT = "8585"
    PROXY = "{IP}:{PORT}"
    driver = PERF_webdriver() 
    # test_proxy(IP)
    # Extractor.SP.consultar_divida_ativa(driver, "CNPJ", "06330557000177")














