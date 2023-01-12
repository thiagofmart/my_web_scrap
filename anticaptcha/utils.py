


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


def solve_captcha(iframe, by: str, reference: str):
    driver.switch_to.frame(frame_reference=iframe) # Focando no Iframe
    driver.find_element(by, reference).click() # Start Captcha
    img_list = driver.find_elements(By.TAG_NAME, "img")
    # SOLVE_CAPTCHA(IMG, VERIFY_BUTTON)
    driver.switch_to.default_content() # Tirando o Foco do Iframe
    return img_list


def test_proxy(IP):
    driver.get("https://www.myip.com/")
    ip = driver.find_element(By.ID, "ip").text
    assert ip==IP, "Configuração de proxy NÃO esta funcionando"


def test_plugin_anticaptcha():
    driver.get('https://anti-captcha.com/demo/?page=recaptcha_v2_textarea')
    # filling form
    driver.find_element_by_css_selector('#login').send_keys('Test login')
    driver.find_element_by_css_selector('#password').send_keys('Test password')


def acp_api_send_request(driver, message_type, data={}):
    message = {
		# this receiver has to be always set as antiCaptchaPlugin
        'receiver': 'antiCaptchaPlugin',
        # request type, for example setOptions
        'type': message_type,
        # merge with additional data
        **data
    }
    # run JS code in the web page context
    # preceicely we send a standard window.postMessage method
    return driver.execute_script(f"return window.postMessage({json.dumps(message)};")

