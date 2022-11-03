import requests
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = Chrome(options=options)
browser.implicitly_wait(5)


def logar():
    browser.get('https://habbok.me/')
    browser.find_element(By.XPATH, 
        '//*[@id="habbinc-login-username"]'
    ).send_keys(username)
    browser.find_element(By.XPATH,
        '//*[@id="habbinc-login-senha"]'
    ).send_keys(password)
    browser.find_element(By.XPATH,
        "/html/body/div[2]/div/div[1]/div/div/div[2]/form/button"
    ).click()
    browser.get('https://habbok.me/nitro')


def extrair():
    items_div = browser.find_element(By.XPATH,
        '//*[@id="draggable-windows-container"]/div[1]/div/div[3]/div/div[2]/div/div[1]/div'
    )
    list_items = items_div.find_elements(By.TAG_NAME,
        "div"
    )
    for element in list_items:
        style = element.get_attribute('style').strip()
        index = style.index('url(')+len('url(')+1
        icon_url = style[23:-3] 
        download_from_url(icon_url)
        print(icon_url)
        
def download_from_url(url):
    response = requests.get(url)
    file_name = url[url.rindex('/'):]
    open(f'./output/icon/{file_name}', 'wb').write(response.content)
    ####
    url_nitro = f'https://nitro.habbok.me/bundled/furniture/{file_name[:-9]}.nitro'
    response_nitro = requests.get(url_nitro)
    print(url_nitro)
    open(f'./output/nitro/{file_name[:-9]}.nitro', 'wb').write(response_nitro.content)


if __name__ == '__main__':
    #browser.get('https://habbok.me/')    
    username = input('Digite, seu username: ')
    password = input('Digite, seu password: ')
    logar()
    while True:
        i = input('Deseja extrair (S/n): ')
        if i.upper() == 'S':
            extrair()
        else:
            break 
