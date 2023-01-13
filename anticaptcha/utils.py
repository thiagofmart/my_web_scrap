from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import os



def create_driver(PROXY: None|str = None, configure_proxy: bool = False):  
    """
    Os webdrivers_managers possuem limite de 60 requests por hora.
    Os downloads são realizados através do repositório git oficial dos webdrivers.
    Para evitar problemas com os pull requests automáticos é válido configurar
    a variável de ambiente GH_TOKEN (Github Token), 
    """
    options = ChromeOptions()
    # Configurando o PROXY (se tiver)
    if configure_proxy and not PROXY: options.add_argument(f"--proxy-server={os.environ.get('PROXY')}")
    if configure_proxy and PROXY: options.add_argument(f"--proxy-server={PROXY}")
    
    driver = Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
        )
    return driver

