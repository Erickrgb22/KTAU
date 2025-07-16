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


class DriverFactory:
    @staticmethod
    def get_caps(caps_file):
        try:
            with open(caps_file, "r") as cf:
                capabilities = json.load(cf)
        except FileNotFoundError:
            raise Exception(f"File {caps_file} not found!")
        except JSONDecodeError:
            raise Exception(f"Bad Json File: {caps_file}")
