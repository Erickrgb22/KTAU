from re import sub
import time
import logging
import structlog
from tqdm import tqdm

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium.options.common.base import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LOG CONFIGURATIONS
timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
shared_processors = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    timestamper,
]
structlog.configure(
    processors=shared_processors + [
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

formatter = structlog.stdlib.ProcessorFormatter(
    processor=structlog.dev.ConsoleRenderer(),
    foreign_pre_chain=shared_processors,
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger= logging.getLogger('Operaciones')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# APPIUM CONFIGRATION

def initialize_appium_client():
    logger.info('Iniciando Cliente Appium')
    
    # Configuración de las opciones de Appium
    options = AppiumOptions()
    options.load_capabilities(
        {
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
    )

    # Barra de progreso para la inicialización
    with tqdm(total=3, desc="Inicializando Cliente Appium", unit='step') as pbar:
        # Simulando pasos de inicialización
        time.sleep(1)  # Simula un paso de configuración
        pbar.update(1)  # Actualiza la barra de progreso

        time.sleep(1)  # Simula otro paso de configuración
        pbar.update(1)  # Actualiza la barra de progreso

        # Establecer la conexión con el servidor Appium
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        pbar.update(1)  # Actualiza la barra de progreso al completar la conexión

    logger.info('Cliente Appium Iniciado')
    return driver
driver = initialize_appium_client()

# APPIUM OPERATIONS

def wait_for_element(by, value, timeout=30):
    try:
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
            #element = driver.find_element(by, value)
            return element  # Retorna el elemento si se encuentra
    except Exception:
        logger.error(f'No se encontro el elemento {value} en {timeout}s')
    raise Exception(f'Elemento {value} no encontrado en {timeout}s por {by}')

def find_by_swipe(by, value, max_intentos=5):
    logger.info(f'Buscando Elemento deslizando: {value} intentos: {max_intentos}')
    intentos = 0
    while intentos < max_intentos:
        try:
            # Intentar encontrar el elemento
            logger.info(f"Buscando elemento: {value} intento #{intentos}")
            elemento = driver.find_element(by, value)
            return elemento  # Retorna el elemento encontrado
        except Exception:
            logger.warning(f"Elemento '{value}' no encontrado. Deslizando hacia abajo...")
            driver.swipe(220, 580, 220, 400, 400)
            time.sleep(3)  # Esperar un momento para que la pantalla se estabilice
            intentos += 1
    raise Exception(
        f"Elemento '{value}' no encontrado después de {max_intentos} intentos"
    )

def ingresar_monto(monto):
    for caracter in monto:
        n = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=caracter)
        n.click()

def void_txn():
    logger.info('Anulando Transaccion')
    driver.tap([(248, 548)], 5)
    void_btn = wait_for_element(AppiumBy.ACCESSIBILITY_ID, 'Anular')
    void_btn.click()
    contiuar = wait_for_element(AppiumBy.ACCESSIBILITY_ID, 'Continuar')
    contiuar.click()
    time.sleep(10)
    logger.info('Venta Anulada')

def login(input_serial, input_user, input_password):
    logger.info(f'Inciando Sesión con los siguientes {input_serial} : {input_user} : {input_password}')
    serial = wait_for_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        value='new UiSelector().className("android.widget.EditText").instance(0)',
    )
    serial.click()
    serial.send_keys(input_serial)
    user = driver.find_element(
        by=AppiumBy.ANDROID_UIAUTOMATOR,
        value='new UiSelector().className("android.widget.EditText").instance(1)',
    )
    user.click()
    user.send_keys(input_user)
    driver.execute_script("mobile: hideKeyboard")
    password = driver.find_element(
        by=AppiumBy.ANDROID_UIAUTOMATOR,
        value='new UiSelector().className("android.widget.EditText").instance(2)',
    )
    password.click()
    password.send_keys(input_password)
    driver.execute_script("mobile: hideKeyboard")
    hide = driver.find_element(
        by=AppiumBy.ANDROID_UIAUTOMATOR,
        value='new UiSelector().className("android.view.View").instance(5)',
    )
    hide.click()
    hide.click()
    login = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Ingresar")
    login.click()
    loading = wait_for_element(
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Iniciando Sesión")'
    )
    print(loading.get_attribute("content-desc"))
    check_login = wait_for_element(
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Bienvenido")'
    )
    print(check_login.get_attribute("content-desc"))


def venta(monto, tip='', currency='', ajust='', void=False, sleep_time=1):
    try:
        logger.info(f'Enviando Venta: {monto} {tip} {currency} {void}')
        venta = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Venta directa")
        venta.click()
        time.sleep(sleep_time)
        logger.info('Digitando monto')
        ingresar_monto(monto)
        logger.info('Procesando Venta')
        procesar = driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().description("Procesar")',
        )
        procesar.click()
        if tip != '':
            logger.info(f'Propina Inicial: {tip}')
            tip_amount = wait_for_element(AppiumBy.ACCESSIBILITY_ID, f'{tip}')
            tip_amount.click()
        else:
            logger.info('Sin Propina Inicial')
        driver.swipe(150, 400, 150, 200, 100)
        logger.info('Procediendo con la venta ...') 
        proceder = driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiSelector().description("Proceder")',
        )
        proceder.click()
    
        if currency != '':
            logger.warning('Enviando Venta DCC, verificar que DCC este activo en el DMS')
            logger.info(f'DCC {currency}')
            ratelookup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, f"//*[contains(@content-desc, '{currency}')]")
                )
            )
            if ratelookup:
                ratelookup.click()
        else:
            logger.info('No DCC')
        
        logger.info('Procesando Venta: Acerque, Inserte o Dezlice Tarjeta!')
        finalizar = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Finalizar")
        finalizar.click()
        logger.info('Venta Finalizada') 
        time.sleep(sleep_time)
    
        if ajust != '':
            logger.info(f'Ajustando venta al: {ajust}')
            driver.tap([(248, 548)], 5)
            ajust_btn = wait_for_element(AppiumBy.ACCESSIBILITY_ID, 'Ajustar')
            ajust_btn.click()
            ajust_amount = wait_for_element(AppiumBy.ACCESSIBILITY_ID, f'{ajust}')
            ajust_amount.click()
            proceder_btn = wait_for_element(AppiumBy.ACCESSIBILITY_ID, 'Proceder')
            proceder_btn.click()
            logging.info(f'Venta Ajustada al: {ajust}')
            time.sleep(10)
        else:
            logger.info('Venta Sin Ajuste')
        if void is True:
            void_txn()
            time.sleep(10)
        else:
            logger.info('Venta Sin Anulacion')
    except Exception:
        logger.exception('Se fallo al ejecutar la venta')

def recarga(monto, numero, operadora):
    logger.info(f'Enviando Recarga de: {monto} al numero: {numero} operadora: {operadora}')
    time.sleep(1)
    recarga = wait_for_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("Recargas")',
    )
    recarga.click()
    logger.info(f'Digitando Telefono {numero}')
    telefono = wait_for_element(
        AppiumBy.XPATH, "//android.widget.ScrollView/android.widget.ImageView"
    )
    telefono.click()
    telefono.send_keys(numero)
    logger.info('Telefono Ingresado, Cerrando Teclado')
    driver.hide_keyboard()
    logger.info('Seleccionando operadora: {operadora}')
    match operadora:
        case "CLARO":
            op_btn = driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().description("RECARGAS\nCLARO\n\n\n\n\n\n")',
            )
            op_btn.click()
        case "ALTICE":
            op_btn = driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().description("RECARGAS\nALTICE\n\n\n\n\n")',
            )
            op_btn.click()
        case "VIVA":
            op_btn = driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().description("RECARGAS\nVIVA\n\n\n\n\n\n\n")',
            )
            op_btn.click()
        case _:
            logger.error('No se ingreso una operadora valida')
    logger.info(f'Ingresando monto: {monto}')
    monto_tx = driver.find_element(
        by=AppiumBy.CLASS_NAME, value="android.widget.EditText"
    )
    monto_tx.click()
    monto_tx.send_keys(monto)
    logger.info('Monto Ingresado, Cerrando Teclado')
    driver.hide_keyboard()
    #    driver.swipe(100, 400, 100, 200, 100)
    logger.info('Procesando Recarga...')
    procesar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Procesar")
    procesar.click()
    logger.info('Procediendo con la recarga')
    proceder = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Proceder")
    proceder.click()
    logger.info('Recarga en proceso: Acerque, Inserte o Dezlice Tarjeta!')
    finalizar = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Finalizar")
    finalizar.click()
    logger.info('Recarga finalizada')


def pago_servicio(contrato, no_contrato, solo_consulta):
    def consulta(contrato):
        logger.info(f"Consultando Factura {contrato} {no_contrato}")
        pago = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="P. Servicios")
        pago.click()
        logger.info(f'Seleccionando Proveedor {contrato}')
        proveedor = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Escoge un proveedor")
        proveedor.click()

        def formatear_contrato(texto_contrato):
            texto_cortado = texto_contrato[:20]
            texto_formateado = texto_cortado.ljust(20)
            return texto_formateado
        logger.info(f'Seleccionando contrato {contrato}')
        time.sleep(2)
        select_contrato = find_by_swipe(
            AppiumBy.ACCESSIBILITY_ID, f"{formatear_contrato(contrato)}"
        )
        select_contrato.click()
        logger.info('Contrato Seleccionado')
        logger.info('Ingresando numero de contrato')
        numero_contrato = wait_for_element(
            AppiumBy.CLASS_NAME, "android.widget.EditText"
        )
        numero_contrato.click()
        numero_contrato.send_keys(no_contrato)
        logger.info('Numero de contrato ingresado, cerrando teclado')
        driver.execute_script("mobile: hideKeyboard")
        logger.info('Consultando Factura')
        consultar = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Consultar factura")
        consultar.click()
        time.sleep(2)
        logger.info('Factura Consultada')

    def pagar():
        logger.info("Pagando Factura")
        driver.swipe(250, 540, 250, 320, 200)
        logger.info('Proceder con pago de Factura')
        proceder_p = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Proceder pago")
        proceder_p.click()
        logger.info('Procesando Pago de Factura, Acerque, Inserte o Dezlice Tarjeta!')
        proceder = wait_for_element(by=AppiumBy.ACCESSIBILITY_ID, value="Proceder")
        proceder.click()
        finalizar = wait_for_element(by=AppiumBy.ACCESSIBILITY_ID, value="Finalizar")
        finalizar.click()
        logger.info('Pago de Factura Finalizado')

    if solo_consulta:
        consulta(contrato)
        time.sleep(1)
        back = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Atrás")
        back.click()
        yes = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Si")
        yes.click()
        logger.info('Consulta realizada')
    else:
        consulta(contrato)
        time.sleep(1.5)
        pagar()

def subsidio(monto:str, subsidio:str, void : bool=False):
    logger.info(f'Enviando Subsidio monto: {monto} tipo: {subsidio}, anulado {void}')
    sub = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Subsidios")
    sub.click()
    logger.info(f'Seleccionando Subsidio {subsidio}')
    sub_sel = wait_for_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(10)',
    )
    time.sleep(0.4)
    sub_sel.click()
    sub_pick = wait_for_element(AppiumBy.ACCESSIBILITY_ID, subsidio)
    time.sleep(0.4)
    sub_pick.click()
    logger.info('Subsidio Seleccionando')
    logger.info(f'Ingresando monto: {monto}')
    ingresar_monto(monto)
    logger.info('Procesar Subcidio')
    proc = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Procesar")
    proc.click()
    proc_2 = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Procesar")
    proc_2.click()
    logger.info('Procesando Subcidio')
    finalizar = wait_for_element(AppiumBy.ACCESSIBILITY_ID, "Finalizar")
    finalizar.click()
    logger.info('Subsidio Finalizado')

    if void is True:
        void_txn()
    else:
        logger.info('Subsidio sin Anular')
def ajustes(pwd='', setting=''):
    settings = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Ajustes")
    settings.click()
    if pwd != "":
        for caracter in pwd:
            n = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=caracter)
            n.click()
    time.sleep(0.2)
    if setting != '':
        match setting:
            case 'Inicializar':
                inicializar = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Inicializar')
                inicializar.click()
            case _:
                print('|ERROR| No se ingreso un Ajuste Valido')

    #time.sleep(20)

def cierre(pwd: str =""):
    logger.info('Cerrando Lotes')
    cierre = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Cierre")
    cierre.click()
    if pwd != "":
        for caracter in pwd:
            n = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=caracter)
            n.click()
    cont = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continuar")
    cont.click()
    time.sleep(20)
    logger.info('Cierre Finalizado')


if __name__ == "__main__":
    logger.info("Probando Operaciones")
    while True:
        op = input('Que operacion deseas probar: ')
        logger.info(f'Probando {op}')
        match op:
            case 'cierre':
                pwd = input('Ingrese la Clave de 4 Digitos: ')
                cierre(pwd)
            case 'init':
                pwd = input('Ingrese la Clave de 6 Digitos: ')
                ajustes(pwd, 'Inicializar')
            case 'venta':
                monto = input('Ingresa el monto: ')
                tip = input('Ingresa el % de propina:')
                currency = input('Ingresa la moneda (DCC): ')
                ajust = input('Ingresa el % de Ajuste: ')
                if input('Anular? ') == 'Y':
                    void = True
                else:
                    void = False
                venta(monto,tip,currency,ajust,void)
            case 'pago servicio':
                contrato = input('Inresa el Prooveedor de Servicios: ')
                no_contrato = input('Ingresa el Numero de Contrato: ')
                if input('Solo Consultar Contrato?: Y/N ') == 'Y':
                    solo_consulta= True
                else:
                    solo_consulta =False
                pago_servicio(contrato, no_contrato, solo_consulta)
            case 'recarga':
                monto = input('Ingrese el Monto: ')
                numero = input('Ingrese el Numero Telefonico: ')
                operadora = input('Ingrese la Operadora: ')
                recarga(monto, numero, operadora)
            case 'subsidio':
                monto = input('Ingrese el Monto: ')
                sub = input('Ingrese el Tipo de Subsidio: ')
                if input('Anular? ') == 'Y':
                    void = True
                else:
                    void = False
                subsidio(monto, sub, void)
            case 'wait for element':
                try:
                   logger.info('Por defecto se usa AppiumBy.ACCESIBILITYID para buscar los elementos en esta prueba') 
                   value = input('Ingrese el Accesibility ID del Elemento a Buscar: ')
                   timeout = int(input('Ingrese el tiempo de espera: '))
                   elemento = wait_for_element(AppiumBy.ACCESSIBILITY_ID,value,timeout)
                   elemento.click()
                except Exception:
                    logger.error('No se encontro el elemento')
            case 'find by swipe':
                try:
                   logger.info('Por defecto se usa AppiumBy.ACCESIBILITYID para buscar los elementos en esta prueba') 
                   value = input('Ingrese el Accesibility ID del Elemento a Buscar: ')
                   max_intentos = int(input('Ingrese el numero de intentos: '))
                   elemento=find_by_swipe(AppiumBy.ACCESSIBILITY_ID,value,max_intentos)
                   elemento.click()
                except Exception:
                    logger.error('No se encontro el elemento')
            case _:
                if input('No seleccionaste nada, deseas salir? Y/N: ') == 'Y':
                    exit()
                else:
                    pass

