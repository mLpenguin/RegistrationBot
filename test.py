
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import os, time, random

import datetime
from datetime import date
from datetime import datetime as datetime1

RegistrationURL = r"file://Webpages/Unofficial Registration.html"
BrowserTimeoutSeconds = 5



chrome_options = Options()  

#chrome_options.add_argument("--headless")  
chrome_options.add_experimental_option("detach", False)
#chrome_options.binary_location = "chrome/ChromiumPortable/ChromiumPortable.exe"
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'chrome/chromedriver.exe')

browser.get(RegistrationURL)

def WaitUntilIDLoads(id):
    element = WebDriverWait(browser, BrowserTimeoutSeconds).until(ec.presence_of_element_located((By.ID, id)))


browser.find_element_by_id("ARMU120LECC").click()

#Click register
print ("Register Clicked")
WaitUntilIDLoads("btnBottomRegister")
browser.find_element_by_id("btnBottomRegister").click()
alert1 = browser.switch_to.alert
print(alert1.text)
alert1.accept()

#from keyboard import press
#press('enter')




''' Calculate time of webserver and delay

import urllib.request
from dateutil.parser import parse
from datetime import date
import datetime
import pytz

def tz2ntz(date_obj, tz, ntz):

    # date_obj: datetime object
    # tz: old timezone
    # ntz: new timezone

    if isinstance(date_obj, datetime.date) and tz and ntz:
       date_obj = date_obj.replace(tzinfo=pytz.timezone(tz))
       return date_obj.astimezone(pytz.timezone(ntz))
    return False

before = datetime.datetime.now()
fp = urllib.request.urlopen("https://student/login.asp").info().get('Date')
after = datetime.datetime.now()
g = parse(fp)
b = tz2ntz(g, 'GMT', 'US/Pacific' )

b = b.replace(tzinfo=None)

print (" Comp time after: " + str(after))
print ("Comp time before: " + str(before))
print ("  Comp time diff: " + str(after-before))


print ("Webserver Time: " + str(b))
print (b-after)

'''