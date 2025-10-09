# Erick Gilmore 2025
# the driver factory creates and manages selenium and appium drivers

# Appium and Selenium imports are with alias for clarity, both have a webdriver class

# APPIUM Libs
from appium import webdriver as appium_webdriver
from appium.options.common.base import AppiumOptions

# SELENIUM Libs
from selenium import webdriver as selenium_webdriver

# LOGGERMAN Setup
from loggerman import loggerman

logger = loggerman(__name__)


class DriverFactory:
    def __init__(
        self,
        appium_server_url: str = "",
        appium_caps: dict = {},
    ):
        self.appium_server_url = appium_server_url
        logger.debug(f"Loads {self.appium_server_url=}")
        self.appium_caps = appium_caps
        logger.debug(f"Loads {self.appium_caps=}")
        # Define instance variables for drivers
        self._selenium = None
        self._appium = None

    def _setup_selenium(self):
        logger.info("Setting up Selenium WebDriver")
        # TODO: Add Errod handling for driver setup
        driver = selenium_webdriver.Chrome()
        logger.info("Selenium WebDriver setup complete")
        return driver

    def _setup_appium(self):
        logger.info("Setting up Appium WebDriver")
        # TODO: Add Error handling for driver setup
        driver = appium_webdriver.Remote(
            command_executor=self.appium_server_url,
            options=AppiumOptions().load_capabilities(self.appium_caps),
        )
        logger.info("Appium WebDriver setup complete")
        return driver

    def get_selenium(self):
        logger.info("Retrieving Selenium WebDriver")
        if self._selenium is None:
            logger.debug("Selenium WebDriver not initialized, setting up now")
            self._selenium = self._setup_selenium()
        return self._selenium

    def get_appium(self):
        logger.info("Retrieving Appium WebDriver")
        if self._appium is None:
            logger.debug("Appium WebDriver not initialized, setting up now")
            self._appium = self._setup_appium()
        return self._appium


if __name__ == "__main__":
    logger.warning("DriverFactory module test started")
    appium_server_url = "http://127.0.0.1:4723"
    appium_caps = {
        "platformName": "Android",
        "appium:automationName": "uiautomator2",
        "appium:deviceName": "A80",
        "appium:appPackage": "com.kinpos.posmultiplatform.vn",
        "appium:appActivity": ".MainActivity",
        "appium:language": "es",
        "appium:locale": "VE",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:noReset": "true",
        "appium:connectHardwareKeyboard": True,
    }

    driver_factory = DriverFactory(appium_server_url, appium_caps)
    web = driver_factory.get_selenium()
    web.get("https://www.google.com")
    web.quit()

    device = driver_factory.get_appium()
    device.quit()
