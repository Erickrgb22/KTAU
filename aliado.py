import time
from device import Device
from loggerman import loggerman
from appium.webdriver.common.appiumby import AppiumBy
from thedriverfactory import DriverFactory

logger = loggerman(__name__)


class Aliado(Device):
    class AppLocators:
        class Login:
            DMS_ID = (AppiumBy.CLASS_NAME, "android.widget.EditText")
            INIT = (AppiumBy.ACCESSIBILITY_ID, "Inicializar")
            USERNAME = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(0)',
            )
            PASSWORD = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(1)',
            )
            CHECK_PASSWORD = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.view.View").instance(6)',
            )
            LOGIN = (AppiumBy.ACCESSIBILITY_ID, "Ingresar")
            BACK = (AppiumBy.ACCESSIBILITY_ID, "Volver")

        class Main:
            PLUS = (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("Agregar\nPestaña 3 de 5")',
            )

        class Transactions:
            SALE = (AppiumBy.ACCESSIBILITY_ID, "Venta")

            class Sale:
                BASE_AMMOUNT = (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.EditText").instance(0)',
                )
                PROCESS = (AppiumBy.ACCESSIBILITY_ID, "Procesar")

            class ChInChOut:
                pass

    def __init__(self, driver, batch_upload_time=10):
        super().__init__(driver)
        self.open_batch = 0
        self.batch_upload_time = batch_upload_time
        self.timeout = 30
        self.actual_screen = None

    def login(self, dms_id, username, password, check_password=False):
        if self.is_element_present(*self.AppLocators.Login.INIT):
            self.write_text(*self.AppLocators.Login.DMS_ID, dms_id)
            self.click(*self.AppLocators.Login.INIT)
        else:
            self.write_text(*self.AppLocators.Login.USERNAME, username)
            self.write_text(*self.AppLocators.Login.PASSWORD, password)
            if check_password:
                self.click(*self.AppLocators.Login.CHECK_PASSWORD)
            self.click(*self.AppLocators.Login.LOGIN)

    def open_transaction(self):
        self.click(*self.AppLocators.Main.PLUS)
        self.actual_screen = "transaction"

    def sale(self, ammount, tip=None):
        pass


if __name__ == "__main__":
    appium_server_url = "http://127.0.0.1:4723"
    appium_caps = {
        "platformName": "Android",
        "appium:automationName": "uiautomator2",
        "appium:deviceName": "0fca9bcf0406",
        "appium:appPackage": "com.kinpos.posmultiplatform.ba_pa",
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
    appium_driver = driver_factory.get_appium()
    app = Aliado(appium_driver)
    input("Press Enter to start the login process...")
    app.login("D180ERICK1", "egilmore_comerce", "ba.ERGB.22", True)
