#!/bin/bash

# Colores para mejor legibilidad
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}--- Extrayendo Capabilities para Appium ---${NC}"

# 1. Obtener el UDID/DeviceName
DEVICE_ID=$(adb devices | grep -w "device" | awk '{print $1}' | head -n 1)

if [ -z "$DEVICE_ID" ]; then
  echo "Error: No se detectó ningún dispositivo. Revisa la conexión USB y el Debugging."
  exit 1
fi

# 2. Obtener Package y Activity de la ventana activa
# Es necesario que tengas la app abierta en el celular
FOCUS_DATA=$(adb -s $DEVICE_ID shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp')
APP_PACKAGE=$(echo $FOCUS_DATA | cut -d' ' -f4 | cut -d'/' -f1)
APP_ACTIVITY=$(echo $FOCUS_DATA | cut -d'/' -f2 | cut -d'}' -f1)

# 3. Obtener Idioma y Región configurados en el sistema
LANGUAGE=$(adb -s $DEVICE_ID shell getprop persist.sys.language)
LOCALE=$(adb -s $DEVICE_ID shell getprop persist.sys.country)

# 4. Mostrar resultados formateados
echo -e "${GREEN}Copia estos valores en tu appium_caps:${NC}"
echo "-------------------------------------------"
echo "appium:deviceName: \"$DEVICE_ID\""
echo "appium:appPackage: \"$APP_PACKAGE\""
echo "appium:appActivity: \"$APP_ACTIVITY\""
echo "appium:language:   \"${LANGUAGE:-es}\""
echo "appium:locale:     \"${LOCALE:-VE}\""
echo "-------------------------------------------"

if [ "$APP_PACKAGE" == "com.google.android.apps.nexuslauncher" ]; then
  echo -e "\n${BLUE}Nota: Parece que estás en el Launcher. Abre la App de Kinpos para obtener el Package y Activity correctos.${NC}"
fi
