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


def check_route_1_1(address):
    proc = subprocess.Popen("tracert -w 1000 -d %s" % address, shell=True,
                            stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line.strip() == "":
            pass
        else:
            line_text_decoded = line.strip().decode('866')
            line_text_list = line_text_decoded.split('  ')
            if '192.168.1.1' in line_text_list:
                print('Route leads to 192.168.1.1')
                return True
        if not line:
            break
    proc.wait()
    print('Route normal')
    return False


def ping_ip(address):
    try:
        proc = subprocess.check_output("ping -n 1 %s" % address, shell=True)
        text = proc.decode('866')
        print('PING to', address, 'successful')

        return True
    except:
        print('PING to', address, 'failed')
        return False


def fix_router_settings():
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_valid_range=365)),
    #                           options=chrome_options)
    chromedriver_path = 'C:\\ESD\\chromedriver.exe'
    if not chromedriver_path:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_options)
    else:
        driver = webdriver.Chrome(service=Service(chromedriver_path),
                                  options=chrome_options)
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

    first_dhcp_port_select = Select(driver.find_element(By.XPATH, '//*[@id="Frm_DhcpModeSelect0"]'))
    first_dhcp_port_select.select_by_visible_text('Wan')
    print('Wan on port0 selected')
    time.sleep(1)

    submit_dhcp_ports = driver.find_element(By.XPATH, '//*[@id="Btn_Submit"]')
    # submit_dhcp_ports.click()
    submit_dhcp_ports.send_keys(Keys.ENTER)

    print('Settings submitted')
    time.sleep(10)

    driver.quit()
    print('Browser closed')


if __name__ == '__main__':
    ping_test_ips = ['8.8.8.8', '77.88.8.8', '192.168.166.1']
    ping_result = False
    for ip in ping_test_ips:
        for i in range(2):
            if not ping_ip(ip):
                ping_result = False
    if not ping_result and check_route_1_1(ping_test_ips[0]):
        fix_router_settings()
