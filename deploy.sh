#!/bin/bash
set -e

# --- Script de Despliegue para Mercadopaginas en Debian ---
# Este script asume que se ejecuta desde la raíz del repositorio clonado.

echo ">>> [Paso 1/5] Actualizando e instalando dependencias del sistema..."
sudo apt-get update
sudo apt-get install -y apache2 python3-pip libapache2-mod-wsgi-py3 git

echo ">>> [Paso 2/5] Instalando dependencias de Python..."
sudo pip3 install -r requirements.txt

# Obtiene la ruta absoluta del directorio del proyecto (ej: /var/www/html/Mercadopaginas)
PROJECT_DIR=$(pwd)
# Obtiene el nombre del directorio (ej: Mercadopaginas)
PROJECT_NAME=\${PROJECT_DIR##*/}

echo ">>> [Paso 3/5] Configurando Apache..."

# Crear la configuración centralizada de WSGI para evitar conflictos con Certbot
sudo bash -c "cat > /etc/apache2/conf-available/wsgi-\${PROJECT_NAME}.conf" <<EOF
# Define el proceso WSGI una sola vez de forma global
WSGIDaemonProcess \${PROJECT_NAME} python-home=/usr python-path=\${PROJECT_DIR}
EOF

# Crear la configuración del sitio para HTTP (Puerto 80)
# Certbot la usará como base para crear la configuración HTTPS
sudo bash -c "cat > /etc/apache2/sites-available/\${PROJECT_NAME}.conf" <<EOF
<VirtualHost *:80>
    ServerName www.mercadopaginas.com # Reemplazar con tu dominio
    ServerAlias mercadopaginas.com   # Reemplazar con tu dominio sin www

    ServerAdmin webmaster@localhost
    DocumentRoot \${PROJECT_DIR}

    # Usar el proceso WSGI definido globalmente
    WSGIProcessGroup \${PROJECT_NAME}
    WSGIScriptAlias / \${PROJECT_DIR}/wsgi.py

    <Directory \${PROJECT_DIR}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

echo ">>> [Paso 4/5] Habilitando la nueva configuración de Apache..."
sudo a2enconf "wsgi-\${PROJECT_NAME}"
sudo a2ensite "\${PROJECT_NAME}"
sudo a2dissite 000-default.conf

echo ">>> [Paso 5/5] Reiniciando Apache para aplicar los cambios..."
sudo systemctl restart apache2

echo "----------------------------------------------------"
echo "¡Configuración base completada!"
echo "El servidor HTTP ya está funcionando."
echo "El siguiente paso es configurar el SSL con Certbot."
echo "----------------------------------------------------"
