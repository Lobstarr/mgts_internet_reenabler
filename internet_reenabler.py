from selenium import webdriver
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
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    start_url = "https://duckgo.com"
    driver.get(start_url)
    print(driver.page_source.encode("utf-8"))
    driver.quit()


if __name__ == '__main__':
    ping_test_ips = ['8.8.8.8', '77.88.8.8', '192.168.166.1']
    ping_result = False
    for ip in ping_test_ips:
        for i in range(3):
            if ping_ip(ip):
                ping_result = True

    if check_route_1_1(ping_test_ips[0]):
        fix_router_settings()

