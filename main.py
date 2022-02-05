from selenium import webdriver
import time
import telebot
from telebot import types

api_telegram = 'ТОКЕН'
bot = telebot.TeleBot(api_telegram, parse_mode='html')

last_zakaz = []

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver')
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    return driver

def get_page():
    driver = get_driver()
    driver.get('https://www.fl.ru/projects/?kind=1#/')
    time.sleep(10)
    btn1 = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/a')
    btn1.click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/div/div[1]/input[5]').click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/ul/li[4]/span').click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/table/tbody/tr/td[1]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/ul/li[8]/span').click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div/table/tbody/tr/td[2]/a').click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/form/div[4]/div/button').click()
    time.sleep(2)
    return driver

while True:
    driver = get_page()
    for post in driver.find_elements_by_class_name('b-post'):
        name = post.find_element_by_tag_name('h2').text
        if name in last_zakaz:
            pass
        else:
            price = post.find_element_by_class_name('b-post__price').text
            opisanie = post.find_element_by_class_name('b-post__txt').text
            link = f'https://www.fl.ru/projects/{post.get_attribute("id").split("project-item")[1]}'
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Перейти', url=f'{link}'))
            bot.send_message(chat_id=400352935, text=f'{name}\n<b>{price}</b>\n{opisanie}', reply_markup=markup)
            last_zakaz.append(name)
    driver.close()
    time.sleep(60)