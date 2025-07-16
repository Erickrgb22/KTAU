# 15 Jul 2025 ~ Erick Gilmore
# KTAU Main File
#


import json

# Appium imports
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions

# Selenium imports
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Main Code

with open("capabilities.json", "r") as cap_file:
    config = json.load(cap_file)
print(config)
options = AppiumOptions()
options.load_capabilities(config)
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
