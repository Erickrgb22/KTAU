import time
from device import Device
from loggerman import loggerman
from appium.webdriver.common.appiumby import AppiumBy
from thedriverfactory import DriverFactory

logger = loggerman(__name__)


class PortalApp(Device):
    def __init__(self, driver, batch_upload_time=10):
        super().__init__(driver)
        self.open_batch = 0
        self.batch_upload_time = batch_upload_time

    def login(self, serial, user, password, show_password=False):
        logger.info(f"Logging in with {serial} : {user} : {password}")
        self.write_text(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().className("android.widget.EditText").instance(0)',
            text=serial,
        )
        self.hide_keyboard()
        self.write_text(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().className("android.widget.EditText").instance(1)',
            text=user,
        )
        self.hide_keyboard()
        self.write_text(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().className("android.widget.EditText").instance(2)',
            text=password,
        )
        self.hide_keyboard()
        self.click(by=AppiumBy.ACCESSIBILITY_ID, value="Ingresar")

    def void_txn(self, timeout=30):
        logger.info("Voiding Transaction")
        self.driver.tap([(248, 548)], 5)
        # self.driver.tap([(377, 878)], 5)
        self.click(AppiumBy.ACCESSIBILITY_ID, "Anular")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Continuar")
        if self.wait_element(
            by=AppiumBy.ACCESSIBILITY_ID,
            value="Anulación exitosa ",
            timeout=timeout,  # << Double space here is intentional
        ):
            logger.info("Void Success")
        else:
            logger.error("Void Failed")
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)

    def ajust_txn(self, ajust, timeout=30):
        logger.info(f"Ajusting Transaction to {ajust}")
        self.driver.tap([(248, 548)], 5)
        # TODO: Implementar metodo para cordenadas variables segun modelo de dispositivo
        #
        # self.driver.tap([(377, 878)], 5)
        self.click(AppiumBy.ACCESSIBILITY_ID, "Ajustar")
        self.click(AppiumBy.ACCESSIBILITY_ID, f"{ajust}")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Proceder")
        if self.wait_element(
            by=AppiumBy.ACCESSIBILITY_ID, value="Ajuste exitoso", timeout=timeout
        ):
            logger.info("Ajust Success")
        else:
            logger.error("Ajust Failed")
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)

    def sale(self, *, amount="", tip="", dcc=False, currency="", ajust="", void=False):
        logger.info(f"Processing Sale {amount} {tip} {dcc} {ajust} {void}")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Venta directa")
        self.type_amount(amount)
        self.swipe_find(AppiumBy.ACCESSIBILITY_ID, "Procesar").click()
        if tip != "":
            self.click(AppiumBy.ACCESSIBILITY_ID, f"{tip}")
        self.click(element=self.swipe_find(AppiumBy.ACCESSIBILITY_ID, "Proceder"))
        logger.info("Processing Sale: Tap, Insert or Swipe Card!")

        if dcc:
            logger.info(f"Selecting DCC Currency {dcc}")
            flag = ""
            match currency:
                case "USD":
                    flag = "🇺🇸"
                case "KWD":
                    flag = "🇰🇼"
                case "JPY":
                    flag = "🇯🇵"
                case _:
                    flag = "🇩🇴"

            self.click(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value=f'new UiSelector().descriptionContains("{flag}")',
                timeout=60,
            )

        self.click(AppiumBy.ACCESSIBILITY_ID, "Finalizar", timeout=120)
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)
        if tip == "" and ajust != "":
            self.ajust_txn(ajust)
        else:
            logger.warning("You cant ajust a transaction with tip")
        if void:
            self.void_txn()

    def recharge(self, amount, phone, carrier, timeout=30):
        logger.info(f"Processing Recharge {amount} {phone} {carrier}")
        self.click(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("Recargas")',
        )
        self.click(
            AppiumBy.XPATH, "//android.widget.ScrollView/android.widget.ImageView"
        )
        self.write_text(
            by=AppiumBy.XPATH,
            value="//android.widget.ScrollView/android.widget.ImageView",
            text=phone,
        )
        self.hide_keyboard()
        match carrier:
            case "CLARO":
                self.click(
                    by=AppiumBy.ANDROID_UIAUTOMATOR,
                    value='new UiSelector().description("RECARGAS\nCLARO\n\n\n\n\n\n")',
                )
            case "ALTICE":
                self.click(
                    by=AppiumBy.ANDROID_UIAUTOMATOR,
                    value='new UiSelector().description("RECARGAS\nALTICE\n\n\n\n\n")',
                )
            case "VIVA":
                self.click(
                    by=AppiumBy.ANDROID_UIAUTOMATOR,
                    value='new UiSelector().description("RECARGAS\nVIVA\n\n\n\n\n\n\n")',
                )
            case _:
                logger.error("No se ingreso una operadora valida")
        self.write_text(
            by=AppiumBy.CLASS_NAME, value="android.widget.EditText", text=amount
        )
        self.hide_keyboard()
        self.swipe_find(AppiumBy.ACCESSIBILITY_ID, "Procesar").click()
        self.click(AppiumBy.ACCESSIBILITY_ID, "Proceder")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Finalizar", timeout=timeout)
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)

    def _format_contract(self, text):
        truncated = text[:20]
        text_formatted = truncated.ljust(20)
        return text_formatted

    def _query(self, contract, number):
        self.swipe_find(AppiumBy.ACCESSIBILITY_ID, "P. Servicios").click()
        self.click(AppiumBy.ACCESSIBILITY_ID, "Escoge un proveedor")
        contract_provider = self._format_contract(contract)
        self.swipe_find(AppiumBy.ACCESSIBILITY_ID, f"{contract_provider}").click()
        self.write_text(AppiumBy.CLASS_NAME, "android.widget.EditText", text=number)
        self.hide_keyboard()
        self.swipe_find(AppiumBy.ACCESSIBILITY_ID, "Consultar factura").click()
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)

    def pay(self, contract, number, timeout=120):
        self._query(contract, number)
        self.swipe_find(AppiumBy.ACCESSIBILITY_ID, "Proceder pago").click()
        self.click(AppiumBy.ACCESSIBILITY_ID, "Proceder")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Finalizar", timeout=timeout)
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)

    def subsidy(self, amount: str, subsidy_type: str, void=False, timeout=30):
        logger.info(f"Processing Subsidy {amount} {subsidy_type} {void}")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Subsidios")
        self.swipe_find(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.view.View").instance(10)',
        ).click()
        self.click(AppiumBy.ACCESSIBILITY_ID, subsidy_type)
        self.type_amount(amount)
        self.click(AppiumBy.ACCESSIBILITY_ID, "Procesar")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Procesar")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Finalizar", timeout=timeout)
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)

    def close(self, pwd: str = ""):
        logger.info("Closing Batch")
        self.click(AppiumBy.ACCESSIBILITY_ID, "Cierre")
        if pwd != "":
            self.type_amount(pwd)
        self.click(AppiumBy.ACCESSIBILITY_ID, "Continuar")
        logger.info("sleeping 3 seconds to let the app recover")
        time.sleep(3)


if __name__ == "__main__":
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
    appium_driver = driver_factory.get_appium()
    app = PortalApp(appium_driver)
    app.login("A80ERICK", "egilmore", "csi.ERGB.00")
    dcc_config = False
    app.sale(amount="1000", dcc=dcc_config)
    app.sale(amount="2000", tip="10%", dcc=dcc_config)
    app.sale(amount="3000", ajust="10%", dcc=dcc_config)
    app.sale(amount="4000", void=True, dcc=dcc_config)
    app.sale(amount="5000", ajust="10%", void=True, dcc=dcc_config)
    if dcc_config:
        app.sale(amount="1000", dcc=dcc_config, currency="USD")
        app.sale(amount="10000", dcc=dcc_config, currency="JPY")
        app.sale(amount="100000", dcc=dcc_config, currency="KWD")
    app.recharge("100", "1234567890", "CLARO")
    app.pay(
        "CLARO",
        "5555",
    )
    app.pay(
        "CAASD",
        "5555",
    )
    app.subsidy("1000", "BONO ESCOLAR")
    app.close()
