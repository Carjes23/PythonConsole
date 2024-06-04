#!/bin/sh

# Nombre del recurso
RESOURCE_NAME=PythonConsoleIF

# Ruta del script actual
SCRIPT_PATH=$( cd $(dirname $0) ; pwd )
cd "${SCRIPT_PATH}"

# Crear un directorio temporal
TMP_DIR=$(mktemp -d)

# Crear el archivo .desktop en el directorio temporal
cat <<EOL > "${TMP_DIR}/${RESOURCE_NAME}.desktop"
[Desktop Entry]
Version=1.0
Name=$RESOURCE_NAME
Comment=Descripción de tu aplicación
Exec=${SCRIPT_PATH}/dist/${RESOURCE_NAME}
Icon=${SCRIPT_PATH}/icon.ico
Terminal=false
Type=Application
Categories=Utility;Application;
EOL

# Crear los directorios necesarios y copiar los archivos
mkdir -p "${HOME}/.local/share/applications"
cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${HOME}/.local/share/applications/"

# Limpiar el directorio temporal
rm "${TMP_DIR}/${RESOURCE_NAME}.desktop"
rmdir "${TMP_DIR}"

# Actualizar la base de datos de aplicaciones de escritorio si es necesario
if [ -d "${HOME}/.local/share/applications" ]; then
    if command -v update-desktop-database > /dev/null; then
      update-desktop-database "${HOME}/.local/share/applications"
    fi
fi

echo "Instalación completada."
