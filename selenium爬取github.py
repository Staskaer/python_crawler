from selenium import webdriver
import time
from redis import StrictRedis
from selenium.webdriver.common.keys import Keys

username_ = "zf5ml3k0"
password_ = "guizixiwu123456"
url_ = "https://github.com/login"
keyword = "python_spider"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


def login(browser, url):
    try:
        browser.get(url)
        username = browser.find_element_by_xpath("//input[@name='login']")
        password = browser.find_element_by_xpath("//input[@name = 'password']")
        username.send_keys(username_)
        password.send_keys(password_)
        button = browser.find_element_by_name("commit")
        button.click()

    except:
        print("login error")
        exit(-1)


def redis_login(host="localhost", port=6379, db=0, password="123456"):
    try:
        redis_ = StrictRedis(host=host, port=port, db=db, password=password)
        return redis_
    except:
        print("redis connect error")
        exit(-1)


def get_pages(browser):
    next_page = browser.find_element_by_xpath("//a[@class = 'next_page']")
    next_page.click()
    time.sleep(1)


def get_save_readme(browser, redis):
    try:
        key = browser.find_element_by_xpath(
            "//a[@data-pjax = '#js-repo-pjax-container']").text
        value = browser.find_element_by_tag_name("article").text
        redis.set(key, value)
    except:
        pass
    browser.close()


def main():
    redis_ = redis_login(db=0)
    # browser = webdriver.Chrome(options=chrome_options)  # 采用无头(headless)浏览器
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    login(browser=browser, url=url_)
    input_keyword = browser.find_element_by_name("q")
    input_keyword.send_keys(keyword)
    input_keyword.send_keys(Keys.ENTER)
    while True:
        a_list = browser.find_elements_by_xpath("//a[@class='v-align-middle']")
        for a in a_list:
            href = a.get_attribute("href")
            browser.execute_script("window.open('{}')".format(href))
            browser.switch_to.window(browser.window_handles[1])
            get_save_readme(browser=browser, redis=redis_)
            browser.switch_to.window(browser.window_handles[0])
        try:
            get_pages(browser=browser)
        except:
            break


main()
