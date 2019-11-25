import time

from selenium import webdriver

from python3_anticaptcha.NoCaptchaTaskProxyless import NoCaptchaTaskProxyless

ANTICAPTCHA_KEY = ""
WEB_URL = "https://www.google.com/recaptcha/api2/demo"
SITE_KEY = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"

post_xpath = '//*[@id="recaptcha-demo-submit"]'
recaptcha_xpath = '//*[@id="g-recaptcha-response"]'

# setup selenium
browser_options = webdriver.ChromeOptions()
browser_options.headless = True
browser_options.add_argument("--disable-gpu")
browser_options.add_argument("--no-sandbox")
browser_options.add_argument("disable-infobars")
browser_options.add_argument("--disable-extensions")
# run browser
browser = webdriver.Chrome(executable_path="./chromefile/chromedriver", options=browser_options)
# open page
browser.get(WEB_URL)
# prepare captcha solver
captcha_obj = NoCaptchaTaskProxyless(anticaptcha_key=ANTICAPTCHA_KEY)
# solve recaptcha
browser.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
# wait script finish
time.sleep(1)
recaptcha_element = browser.find_element_by_xpath(recaptcha_xpath)
recaptcha_element.click()
recaptcha_element.clear()
# get captcha solution
captcha_result = captcha_obj.captcha_handler(websiteURL=WEB_URL, websiteKey=SITE_KEY)
# insert captcha solution
recaptcha_element.send_keys(captcha_result["solution"]["gRecaptchaResponse"])
# wait success insertion
time.sleep(2)
# push post button
post_button = browser.find_element_by_xpath(post_xpath)
browser.execute_script("arguments[0].click();", post_button)
# OR
# post_button.click()

time.sleep(5)
browser.quit()
