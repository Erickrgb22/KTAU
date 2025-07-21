# 15 Jul 2025 ~ Erick Gilmore
#
# Driver Factory
#
# This file is for handling the Appium Drivers
# here lives the class that lets us create Driver Objects
#

# imports
import json
from json.decoder import JSONDecodeError
from appium import webdriver
from appium.options.common.base import AppiumOptions


class DriverFactory(webdriver.Remote):  # type: ignore
    def __init__(self, caps_file):
        try:
            print(f"Loading caps_file: {caps_file}")
            with open(caps_file, "r") as cf:
                capabilities = json.load(cf)

            print(f"caps_file Loaded: {caps_file}")
            print("Starting AppiumOptions")
            options = AppiumOptions()
            print("Loading capabilities")
            options.load_capabilities(capabilities)
            print("Starting Driver")
            driver = webdriver.Remote("https:\\127.0.0.1:4723", options=options)  # type: ignore

        except FileNotFoundError:
            raise Exception(f"File {caps_file} not found!")
        except JSONDecodeError:
            raise Exception(f"Bad Json File: {caps_file}")

    # Example usage
