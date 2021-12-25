# pyinstaller registration.spec registration.py --onefile --icon=icon.ico
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager

import os, time, random, configparser

import datetime
from datetime import date
from datetime import datetime as datetime1

#Perameters during Disclaimer
# 1 defualt login

# Perameters during Instructions
# timeroff
# nodelay
# 1
# 2

config = configparser.ConfigParser()
config.read(r'config.ini')

#PERAMETERS
fileLoc = str(config['main']['classList'])
RegistrationURL = str(config['main']['website'])
version = '11.18.19'
enableCountDown = True


#Settings:
maxNumberofRegistrationAttempts = 10
delay = random.randint(2,5) #3-5 #Delay on Registration webserver is about 2 sec. Webserver is 2sec slower
    #type "nodelay" in instructions page for no delay
    #type "1" in instructions page for 1 sec delay
    #type "2" in instructions page for 2 sec delay
default_Term = "CHS SP 2021"
BrowserTimeoutSeconds = 5
CountdownTimeout = int(60 * 2) #  # of Min #Countodwn action every 2 min

#Default Login:
default_u = str(config['main']['user'])
default_p = str(config['main']['pass'])




#Parse File for Class List
classList = []
#Default Target Time
h = 7
m = 0
s = 0

def PrintDisclaimer():
    #Disclaimer
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#     DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER      #")
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#  This SOFTWARE PRODUCT is provided by THE PROVIDER \"as is\" and \"with all faults.\" THE          #")
    print ("#  PROVIDER makes no representations or warranties of any kind concerning the safety,            #")
    print ("#  suitability, lack of viruses, inaccuracies, typographical errors, or other harmful components #")
    print ("#  of this SOFTWARE PRODUCT. There are inherent dangers in the use of any software, and you are  #")
    print ("#  solely responsible for determining whether this SOFTWARE PRODUCT is compatible with your      #")
    print ("#  equipment and other software installed on your equipment. You are also solely responsible     #")
    print ("#  for the protection of your equipment and backup of your data, and THE PROVIDER will not be    #")
    print ("#  liable for any damages you may suffer in connection with using, modifying, or distributing    #")
    print ("#  this SOFTWARE PRODUCT.                                                                        #")
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#     DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER  |  DISCLAIMER      #")
    print ("#------------------------------------------------------------------------------------------------#")

    response = input("Press ENTER to accept the disclaimer and continue...")
    if(response == ""):
        t = 99
    else:
        t = response

    return response

def PrintInstructions():
    print('\n')
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#                                        Version: %s                                       #" % version)
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#        INSTRUCTIONS  |  INSTRUCTIONS  |  INSTRUCTIONS  |  INSTRUCTIONS  |  INSTRUCTIONS        #")
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#  In order to use this program, it needs to have a file with all the class names that you want  #")
    print ("#  to register for. By default, \"classList.txt\" is automatically registered however, any \"*.txt\" #")
    print ("#  file will work. Each class needs to be placed on each line with nothing else in the file. The #")
    print ("#  class name is the abbreviation that is in all the class list for the semester. An example of  #")
    print ("#  the txt file is as follows:                                                                   #")
    print ("#  classList.txt:                                                                                #")
    print ("#    *ARMU120LEC                                                                                 #")
    print ("#    *BIOL240XONL                                                                                #")
    print ("#    *BIOL210LLAB02                                                                              #")
    print ("#------------------------------------------------------------------------------------------------#")
    print ("#        INSTRUCTIONS  |  INSTRUCTIONS  |  INSTRUCTIONS  |  INSTRUCTIONS  |  INSTRUCTIONS        #")
    print ("#------------------------------------------------------------------------------------------------#")
    return input("Press the ENTER button to continue...")

def calculateTimeDifference(hour, minute, second, delay):
    now = datetime.datetime.now()
    minute = f"{(minute):02d}"
    second = f"{(second+delay):02d}"

    #print (len(second))


    s1 = str(hour) + ":" + str(minute) + ":" + str(second)
    #print(s1)
    s2 = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    #print (s2)
    FMT = '%H:%M:%S'


    tdelta = datetime1.strptime(s1, FMT) - datetime1.strptime(s2, FMT)
    if (tdelta.total_seconds() < 0):
        tdelta = datetime1.strptime(s2, FMT) - datetime1.strptime(s1, FMT)
        tdelta = 86400 - tdelta.total_seconds()
        return tdelta
    else:
        return tdelta.total_seconds()

def countdown(hour, minute, second, delay):
    remainingSeconds = int(calculateTimeDifference(hour, minute, second, delay))
    print ('\n')
    print ("#-------------------------------------#")
    print ("#     Countdown Till Registration     #")
    print ("#-------------------------------------#")
    while remainingSeconds>0:
        mins, secs = divmod(remainingSeconds, 60)
        hours, mins = divmod(mins, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))
        print(timeformat, end='\r')
        if (remainingSeconds%CountdownTimeout == 0):
            countdownRepeatedTask()

        
        time.sleep(1)
        remainingSeconds = int(calculateTimeDifference(hour, minute, second, delay))
        #print (remainingSeconds)
    #Zero
    mins, secs = divmod(remainingSeconds, 60)
    hours, mins = divmod(mins, 60)
    timeformat = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))
    print(timeformat, end='\r')
    time.sleep(1)

def countdownRepeatedTask():
    browser.refresh()
    ##print ("Countdown timer action")

def SetRegistrationTime(hour, minute):
    print ('\n')
    print ("#-------------------------------------#")
    print ("#      Select Registration Time       #")
    print ("#-------------------------------------#")
    print ("#  The default registration time is:  #")
    print ("#               %i:%02i                  #" % (hour,minute))
    print ("#-------------------------------------#")
    ynTime = input("Use this time? (Y/N): ")
    if (ynTime.lower() == "n"):
        print ('\n')
        hour=-1 #Force change of values
        minute=-1
        while (hour<0 or hour>=24):
            print ("#-------------------------------------#")
            print ("#      Select Registration Time       #")
            print ("#-------------------------------------#")
            print ("# What is the HOUR for registration:  #")
            print ("#        Between 0 and 23             #")
            hour = int(input("Hour = "))
        print ('\n')
        while (minute<0 or minute>=60):    
            print ("#-------------------------------------#")
            print ("#      Select Registration Time       #")
            print ("#-------------------------------------#")
            print ("#What is the MINUTE for registration: #")
            print ("#        Between 0 and 59             #")
            minute = int(input("Minute = "))
        print ('\n')
        print ("#-------------------------------------#")
        print ("#        New Registration Time        #")
        print ("#-------------------------------------#")
        print ("#    The new registration time is:    #")
        print ("#               %i:%02i                 #" % (hour,minute))
        print ("#-------------------------------------#")
        input("Press the ENTER button to continue...")
    else:
        print ("Using default time of  %i:%02i" % (hour,minute))
    return hour, minute

def LoginInformation():
    notDone = True
    while (notDone):
        print('\n')
        print ("#-------------------------------------#")
        print ("#         Enter your USERNAME         #")
        print ("#-------------------------------------#")
        print ("#                                     #")
        user = input("USERNAME: ")
        #print('\n')
        print ("#-------------------------------------#")
        print ("#         Enter your PASSWORD         #")
        print ("#-------------------------------------#")
        print ("#                                     #")
        passw = input("PASSWORD: ")
        #print('\n')
        print ("#-------------------------------------#")
        print ("#          Login Information          #")
        print ("#-------------------------------------#")
        print ("# * Username: %s" % (user))
        print ("# * Password: %s" % (passw))
        confirmLogin = input("Is the following login credentials Correct? (Y/N)")
        confirmLogin = confirmLogin.lower()
        if confirmLogin == 'y' or confirmLogin == 'yes':
            notDone = False
            return (user, passw)
        else:
            notDone = True
            print ("Restarting because response was not \"y\" or \"yes\"")

def ClassFileName():
    fileList=os.listdir()
    updatedFileList = []
    fileChoice = 0

    for x in fileList:
        if '.txt' in x:
            updatedFileList.append(x)
    #print ('\n')
    
    found = False
    for x in updatedFileList:
        if (fileLoc in x):
            found = True
    if found:
        return 'classList.txt'
    else:       
        print('\n')   
        while (fileChoice <= 0 or fileChoice > len(updatedFileList)):
            print ("#-------------------------------------#")
            print ("#        Select File to Parse         #")
            print ("#-------------------------------------#")
            print ("#  Choose the file to parse for the   #")
            print ("#   list of classes to register for   #")
            print ("#   *******************************   #")
            z = 0
            for x in updatedFileList:
                z = z + 1
                print ("#    %i - %s" % (z, x))
            print ("#   *******************************   #")
            
            fileChoice = int(input("Select a number: ")) #Error when nothing is entered
        return updatedFileList[fileChoice-1]

def ParseFile(fileName):
    fileHandler = open(fileName, 'r')
    for line in fileHandler: 
        line = line.strip()
        line = str(line.upper() + "C")
        classList.append([line, 0])
    fileHandler.close() 

def SelectTerm():

    print ('\n')

    print ("#-------------------------------------#")
    print ("#            Enter a term             #")
    print ("#-------------------------------------#")
    print ("#  Example:                           #")
    print ("#  CHS FA 2019                        #")
    print ("#  chs sp 2020                        #")
    print ("#  *Case does not matter*             #")
    print ("#-------------------------------------#")
    t = input("Enter the Term: ")
    return t.upper()

def Overview():
    confirmRegistration = 'r'
    while (confirmRegistration != 'y' and confirmRegistration != 'yes'):
        print ('\n')
        print ("#-------------------------------------#")
        print ("#             OVERVIEW                #")
        print ("#-------------------------------------#")
        print ("# Classes:")
        for element in classList: #Print classes that could not be found
            print ("# * " + element[0])
        print ("#*************************************#")
        print ("# Registration Time:  %i:%02i" % (h,m))
        print ("#*************************************#")
        print ("# Term:  %s" % (term))
        print ("#-------------------------------------#")
        print ("# Username: %s" % u)
        printPassword = p[0] + "*"*(len(p)-2) + p[len(p)-1]

        print ("# Password: %s" % printPassword)
        print ("# Delay: %i" % delay)
        print ('\n')
        confirmRegistration = input("Attempt to Register for These Classes (Y/N)")
        confirmRegistration = confirmRegistration.lower()
        if confirmRegistration == 'y' or confirmRegistration == 'yes':
            print ('Proceding')
        else:
            ccRegistreation = input("Are you sure you want to exit the program? (Y/N)")
            ccRegistreation = ccRegistreation.lower()
            if ccRegistreation == 'y' or ccRegistreation == 'yes':
                print ('\n')
                print ("Exiting Program because response was \"y\" or \"yes\"")
                input("Press Enter to continue...")
                exit()

def WaitUntilIDLoads(id):
    element = WebDriverWait(browser, BrowserTimeoutSeconds).until(ec.presence_of_element_located((By.ID, id)))

def WaitUntilNameLoads(n):
    element = WebDriverWait(browser, BrowserTimeoutSeconds).until(ec.presence_of_element_located((By.NAME, n)))

#browser.implicitly_wait(3) 

#Disclamer #Need to fix
useDefaultLogin = 1
PrintDisclaimer()

#Print Instructions
answer = PrintInstructions()
if (answer == '0'):
    delay = 0
    print('NO DELAY')
elif (answer == 'timeroff'):
    enableCountDown = False
elif (answer == '1'):
    delay = int(answer)
    print('DELAY: ' + str(delay))
elif (answer == '2'):
    delay = int(answer)
    print('DELAY: ' + str(delay))


#Registration Time
h, m = SetRegistrationTime(h, m)

#Select Class List File
fileLoc = ClassFileName()

#Parse File
ParseFile(fileLoc)

#Select Term
term = SelectTerm()
if (term == ""):
    term = default_Term
#term = "CHS FA 2019"

#Login Information
if (useDefaultLogin == 1):
    u = default_u
    p = default_p
else:
    u, p = LoginInformation()

#Overview
Overview()


if (enableCountDown):
    countdown(h, m, s, 0)

chrome_options = Options()  

#chrome_options.add_argument("--headless")  
chrome_options.add_experimental_option("detach", True)
#chrome_options.binary_location = "chrome/ChromiumPortable/ChromiumPortable.exe"
#browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'chromedriver.exe')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#Driver is same as installed chrome version

#browser = webdriver.Chrome()

browser.get(RegistrationURL)
#time.sleep(1)
#browser.implicitly_wait(3) 
##Clear Dialog Box
    ##alert = browser.switch_to.alert
    ##alert.accept()
#Login
WaitUntilIDLoads('txtUsername')
username= browser.find_element_by_id('txtUsername')
username.send_keys(u)


password = browser.find_element_by_id('txtPassword')
password.send_keys(p)


#Select Term
el = browser.find_element_by_id('idterm')
for option in el.find_elements_by_tag_name('option'):
    if option.text == term:
        option.click()
        break  

browser.find_element_by_id('btnLogin').click()

#Click Registration Button
WaitUntilIDLoads('spregunoffreg')
browser.find_element_by_id('spregunoffreg').click()


#Refresh Registration Page
RegistrationNumberofAttempts = 0
while RegistrationNumberofAttempts < maxNumberofRegistrationAttempts:

    try:
        WaitUntilIDLoads('btnBottomRegister')
        break
    except:
        browser.refresh()
        RegistrationNumberofAttempts += 1
        print("Register button not found... Refreshing again. Try number: " +str(RegistrationNumberofAttempts))
        if (maxNumberofRegistrationAttempts == RegistrationNumberofAttempts):
            print("Timeout Exception")
            exit()


"""

        try:
            WaitUntilIDLoads('btnBottomRegister')
        except:
            print("Timeout Exception")
            exit()
"""

#Calculation of number of pages
numOfPages = browser.find_elements_by_class_name('Portal_Grid_Pager')
totalNumPages = numOfPages[0].text
length = len(totalNumPages)

totalNumPages = int(totalNumPages[(length-2):(length-1)])

#totalNumPages = 1
def AllRegistered():
    allClassesRegistered  = True
    q = 0
    while (allClassesRegistered and  q < len(classList)):
        if (classList[q][1] == 0):
            allClassesRegistered = False
        q = q + 1
    return allClassesRegistered

#Check checkboxes
page = 1
while (not AllRegistered() and page <= totalNumPages):
    #print (i)
    WaitUntilNameLoads('AddCourse')  #Wait till page loads
    for className in classList: #Run through class list and check any classes that are shown
            #print (className[0])
            if className[1] == 0:
                try: 
                    browser.find_element_by_id(className[0]).click()
                    #print ("Clicked")
                    className[1] = 1
                except:
                    #print ("Class not found on this page")
                    pass

    page = page + 1
    print ("On page: " + str(page))
    ##print (totalNumPages)
    if (page <= totalNumPages):
        browser.find_element_by_link_text(str(page)).click()

#Click register
print ("Register Clicked")
WaitUntilIDLoads("btnRegister")
browser.find_element_by_id("btnRegister").click()
time.sleep(1)
alert1 = browser.switch_to.alert
alert1.accept()


#Summary
print ("#-------------------------------------#")
print ("#    Classes Able to Be Registered    #")
print ("#-------------------------------------#")
for element in classList: #Print classes that could  be found
    if (element[1] == 1):
        print ("# * " + element[0])
print ("#-------------------------------------#")
print ("#-------------------------------------#")
print ("#  Classes NOT Able to Be Registered  #")
print ("#-------------------------------------#")
for element in classList: #Print classes that could not be found
    if (element[1] == 0):
        print ("# * " + element[0])
print ("#-------------------------------------#")
input("Press ENTER to exit...")