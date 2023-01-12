from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import os
from time import sleep
from collections.abc import Iterable
import urllib
import zipfile
from pathlib import Path
from utils import *
import json

"""
Os webdrivers_managers possuem limite de 60 requests por hora.
Os downloads são realizados através do repositório git oficial dos webdrivers.
Para evitar problemas com os pull requests automáticos é válido configurar
a variável de ambiente GH_TOKEN (Github Token), 
"""
def create_driver(PROXY: None|str = None, configure_proxy: bool = False, extensions: list|tuple|set = []):  
    options = ChromeOptions()
    # Configurando o PROXY (se tiver)
    if configure_proxy and not PROXY: options.add_argument(f"--proxy-server={os.environ.get('PROXY')}")
    if configure_proxy and PROXY: options.add_argument(f"--proxy-server={PROXY}")
    # Adicionando os plugins e extensões
    options.add_extension('./plugin.zip')
    # for extension in extensions: options.add_extension(extension)

    driver = Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
        )
    return driver


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

    captcha_iframe = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div[2]/span/form/span/div/div[2]/table/tbody/tr/td[2]/span/span/div[1]/div/div/iframe")
    solve_captcha(iframe=captcha_iframe, by=By.ID, reference="recaptcha-anchor")


def download_anti_captcha_plugin():
    url = 'https://antcpt.com/anticaptcha-plugin.zip'
    # download the plugin
    filehandle, _ = urllib.request.urlretrieve(url)
    print(filehandle)
    # unzip it
    with zipfile.ZipFile(filehandle, "r") as f:
        f.extractall("plugin")


def configure_API_key_in_anti_captcha_plugin_file(api_key):
    file = Path('./plugin/js/config_ac_api_key.js')
    file.write_text(file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

    # zip plugin directory back to plugin.zip
    zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk("./plugin"):
            for file in files:
                path = os.path.join(root, file)
                zip_file.write(path, arcname=path.replace("./plugin/", ""))
    zip_file.close()


if __name__=="__main__":
    # PROXY não estava funcionando no GeckoDriver
    # https://hidemy.name/en/proxy-list/?type=s#list
    api_key = ""
    IP = "185.231.114.140"
    PORT = "8585"
    PROXY = "{IP}:{PORT}"
    #download_anti_captcha_plugin()
    #configure_API_key_in_anti_captcha_plugin_file(api_key)
    driver = create_driver(extensions=[]) #./plugin.zip not working as expected...
    driver.implicitly_wait(5)
    # test_proxy(IP)
    # test_plugin_anticaptcha()














