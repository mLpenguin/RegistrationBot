# Class Registration Bot
Class registration bot for the Three Rivers Systems student portal. This automatically waits for the proper registration time, logs into the student portal and registers for classes.


# Features
- Automatically logs into student portal.
- Waits until registration time to submit class choices.
- Auto-refreshes webpage until registration option is available.
- Provides summary at the end listing classes that were able and unable to be registered for.

# Requirements
- Google Chrome Browser
- Python 3.7
- Selenium
- Webdriver Manager

# How to Use
1. Create 'config.ini' with website url, class list, username and password (See example below).
2. Create file ('classList.txt') with a list of classes to register for.
3. Run registration.py.

## Sample file configuration:
config.ini:
```
[main]
website = STUDENT PORTAL URL
classList = classList.txt
user = USERNAME
pass = PASSWORD
```

## Sample ClassList file
classList.txt
```
BIOL230LEC01
BIOL340LECU
BIOL430LECU
BIOL470LECU
COLL420LEC02
PHIL310LEC02
```


# Known Issues
- Countdown clock may get out of sync after extended period of time
- Not fully tested. Worked successfully once.