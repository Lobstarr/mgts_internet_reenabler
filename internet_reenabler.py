from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import subprocess


def tracert_ip(address):
    proc = subprocess.Popen("tracert -w 1000 -d %s" % address, shell=True,
                            stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line.strip() == "":
            pass
        else:
            text = line.strip().decode('866')
            # print(text)
            print(text.split('  ')[::-1][0])
            if text.split('  ')[::-1][0] == address:
                return True
        if not line:
            break
    proc.wait()
    return False


def check_route_1_1(address):
    proc = subprocess.Popen("tracert -w 1000 -d %s" % address, shell=True,
                            stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if line.strip() == "":
            pass
        else:
            text = line.strip().decode('866')
            # print(text)
            print(text.split('  ')[::-1][0])
            if text.split('  ')[::-1][0] == '192.168.165.1':
                return True
        if not line:
            break
    proc.wait()
    return False


def ping_ip(address):
    try:
        proc = subprocess.check_output("ping -n 1 %s" % address, shell=True)
    except:
        return False

    return True


def fix_router_settings():
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    # chrome_options.add_argument("--headless")
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

    login_field = driver.find_element(By.ID, 'Frm_Username')
    login_field.clear()
    login_field.send_keys("mgts")
    password_field = driver.find_element(By.ID, 'Frm_Password')
    password_field.clear()
    password_field.send_keys("mtsoao")
    submit_password = driver.find_element(By.ID, 'LoginId')
    submit_password.click()
    driver.refresh()
    # network_section = driver.find_element(By.XPATH,
    #                                       '//*[@id="menu0"]/table/tbody/tr/td/table/tbody/tr[16]')
    network_section = driver.find_element(By.ID, 'DhcpMode0')
    network_section.click()

    pass

    print(driver.page_source)
    driver.quit()


if __name__ == '__main__':
    # ping_test_ips = ['8.8.8.8', '77.88.8.8', '192.168.166.1']
    # ping_result = False
    # for ip in ping_test_ips:
    #     for i in range(3):
    #         if ping_ip(ip):
    #             ping_result = True
    #
    # if check_route_1_1(ping_test_ips[0]):
    #     fix_router_settings()
    fix_router_settings()
