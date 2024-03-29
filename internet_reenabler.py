from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import subprocess
import time
import platform
import configparser
from os import path


def check_route(address):
    if platform.system().lower() == 'windows':
        command = ['tracert', '-w', '1000', '-h', '10', '-d', address]
        encoding = '866'
        shell = True
    else:
        command = ['traceroute', '-m', '10', '-n', address]
        encoding = 'UTF-8'
        shell = False

    proc = subprocess.Popen(command, shell=shell,
                            stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line.strip() == "":
            pass
        else:
            line_text_decoded = line.strip().decode(encoding)
            line_text_list = [i.strip() for i in line_text_decoded.split(' ') if i.strip() != '']
            if line_text_list:
                print(line_text_list)
            if '192.168.1.1'.strip() in line_text_list:
                print('Route leads to 192.168.1.1')
                return False
        if not line:
            break
    proc.wait()
    print('Route normal')
    return True


def ping_ip(address):
    if platform.system().lower() == 'windows':
        packets_param = '-n'
    else:
        packets_param = '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', packets_param, '1', '-w', '1000', address]

    try:
        proc = subprocess.check_output(command, shell=True)
        text = proc.decode('866')
        if proc:
            print('PING to', address, 'successful')
            return True
        else:
            print('PING to', address, 'failed')
            return False
    except:
        print('PING to', address, 'exited with error')
        return False


def fix_router_settings():
    chrome_options = Options()
    if platform.system().lower() == 'windows':
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        # chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works

        if not chromedriver_path:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                      options=chrome_options)
        else:
            driver = webdriver.Chrome(service=Service(chromedriver_path),
                                      options=chrome_options)
    else:
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        driver = webdriver.Chrome(options=chrome_options)

    router_address = "http://192.168.1.1"
    driver.get(router_address)
    assert "http://192.168.1.1/" == driver.current_url
    print('Got page at', router_address)
    login_field = driver.find_element(By.ID, 'Frm_Username')
    login_field.clear()
    login_field.send_keys("mgts")

    password_field = driver.find_element(By.ID, 'Frm_Password')
    password_field.clear()
    password_field.send_keys("mtsoao")

    submit_password = driver.find_element(By.ID, 'LoginId')
    submit_password.click()
    print('login done')

    driver.switch_to.frame('mainFrame')
    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.ID, 'mmNet'))
    # network_section = driver.find_element(By.XPATH,
    #                                       '//*[@id="menu0"]/table/tbody/tr/td/table/tbody/tr[16]')
    network_section = driver.find_element(By.ID, 'mmNet')
    network_section.click()
    print('Opened network settings')
    time.sleep(1)

    lan_section = driver.find_element(By.XPATH, '//*[@id="menu0"]/table/tbody/tr/td/table/tbody/tr[12]')
    lan_section.click()
    print('Opened lan settings')
    time.sleep(1)

    dhcp_port_section = driver.find_element(By.XPATH, '//*[@id="menu0"]/table/tbody/tr/td/table/tbody/tr[12]')
    dhcp_port_section.click()
    print('Opened dhcp-port settings')
    time.sleep(1)

    first_dhcp_port = driver.find_element(By.XPATH, '//*[@id="Frm_DhcpModeSelect0"]')
    first_dhcp_port_select = Select(first_dhcp_port)
    first_dhcp_port_select.select_by_visible_text('Wan')
    print('Wan on port0 selected')
    time.sleep(1)

    driver.set_page_load_timeout(15)
    # first_dhcp_port.submit()
    submit_dhcp_ports = driver.find_element(By.XPATH, '//*[@id="Btn_Submit"]')
    # submit_dhcp_ports.click()
    submit_dhcp_ports.send_keys(Keys.ENTER)

    print('Settings submitted')
    time.sleep(10)

    driver.quit()
    print('Browser closed')


def check_internet_and_fix(ping_test_ips):
    ping_result = False
    for ip in ping_test_ips:
        for i in range(2):
            if not ping_ip(ip):
                ping_result = False
    if not ping_result and not check_route(ping_test_ips[0]):
        # fix_router_settings()

        return False
    else:
        return True


def generate_config(filename):
    with open(filename, 'w+') as file:
        config_template = ''
        file.write(config_template)


if __name__ == '__main__':
    config_filename = 'internet_reenabler.ini'
    if not path.isfile(config_filename):
        generate_config(config_filename)

    config = configparser.ConfigParser()
    config.read('internet_reenabler.ini')

    test_ips_with_ping = config['global']['test_ips_with_ping'].split(',')
    chromedriver_path = config['global']['chromedriver_path']
    retries = int(config['global']['retries'])

    for this_try in range(retries):
        if check_internet_and_fix(test_ips_with_ping):
            break
        time.sleep(15)
    print('Done')
