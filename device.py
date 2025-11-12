# Erick Gilmore 2025
#
# This file defines the Device class for interacting with POS devices.

# import time  # For sleep

from appium.webdriver.common.appiumby import AppiumBy  # For AppiumBy locator strategies
from selenium.webdriver.support.ui import WebDriverWait  # For Waiting for elements
from selenium.webdriver.support import (
    expected_conditions as EC,
)  # For waiting conditions like presence_of_element_located
from selenium.common.exceptions import (
    TimeoutException,
)  # If a timeout occurs finding an element
# from selenium.common.exceptions import (
#    NoSuchElementException,
# )  # If a element is not found

from loggerman import loggerman

# Call The Loggerman
logger = loggerman(__name__)


# It contains the low level methods to interact with the device using Appium.
# These methods are used by the higher level classes to perform actions on the device.
class Device:
    def __init__(self, driver):
        self.driver = driver  # You must pass an Appium driver instance here
        pass

    def wait_element(
        self, *, by=None, value=None, element=None, wait_for="presence", timeout=10
    ):
        if wait_for == "clickable":
            wait_condition = EC.element_to_be_clickable
        elif wait_for == "visible":
            wait_condition = EC.visibility_of_element_located
        else:
            wait_condition = EC.presence_of_element_located

        logmsg = f"Waiting for element {value if value else 'provided element'} with condition {wait_for}"
        logger.info(logmsg)

        try:
            wait = WebDriverWait(self.driver, timeout)
            if element:
                return wait.until(wait_condition(element))
            elif by and value:
                return wait.until(wait_condition((by, value)))
            else:
                raise ValueError("Either element or both by and value must be provided")
        except TimeoutException:
            logger.error(
                f"Timeout waiting for element {value if value else 'provided element'} with condition {wait_for}"
            )
            raise

    def swipe_find(
        self, by, value, attempts=5, timeout=1
    ):  # Swipe to find an element, with a number of attempts
        current_attempts = 0
        while current_attempts < attempts:
            try:
                logger.info(f"Looking for element {value} attempt #{current_attempts}")
                element = self.wait_element(by=by, value=value, timeout=timeout)
                return element  # Return the element if found
            except TimeoutException:
                logger.warning(
                    f"Element not found, swiping to find it. Attempt {current_attempts + 1}/{attempts}"
                )
                self.driver.swipe(220, 580, 220, 400, 400)
        logger.error(f"Element '{value}' not found after {attempts} swipes.")
        raise Exception(f"Element '{value}' not found after {attempts} swipes.")

    def click(
        self, by=None, value=None, element=None, timeout=10
    ):  # Click an element, wait for it if not provided
        if element is None and (by is None or value is None):
            raise ValueError("Either element or both by and value must be provided")
        if element:
            logger.info("Elemnt Provided, waiting to be clickable")
            clickable_element = self.wait_element(
                element=element, wait_for="clickable", timeout=timeout
            )
        else:
            logger.info(f"Waiting for {value} to be clickable")
            clickable_element = self.wait_element(
                by=by, value=value, wait_for="clickable", timeout=timeout
            )
        logger.info(f"Clicking on {value if value else 'provided element'}")
        clickable_element.click()
        logger.info(f"Clicked on {value if value else 'provided element'}")

    def write_text(
        self, by=None, value=None, timeout=30, element=None, text=""
    ):  # write text into an element, wait for it if not provided
        if element is None and (by is None or value is None):
            raise ValueError("Either element or both by and value must be provided")
        if element:
            logger.info(f"Writing {text} on provided element")
            self.click(element=element)
            element.send_keys(text)
            logger.info(f"Text {text} written on provided element")
        else:
            logger.info(f"Writing {text} on {value}")
            element = self.wait_element(by=by, value=value, timeout=timeout)
            self.click(element=element)
            element.send_keys(text)
            logger.info(f"Text {text} written on provided element")

    def hide_keyboard(self):
        logger.info("Hiding keyboard")
        try:
            self.driver.hide_keyboard()
            logger.info("Keyboard hidden")
        except Exception as e:
            logger.error(f"Error hiding keyboard: {e}")
            raise

    def type_amount(self, amount, timeout=2):
        logger.info(f"Typing amount: {amount}")
        for char in amount:
            self.click(by=AppiumBy.ACCESSIBILITY_ID, value=char, timeout=timeout)
