# MercadoPaginas - Edición Flask

Este proyecto es una versión basada en Python y Flask del sitio web original de MercadoPaginas. Sirve como un catálogo simple y elegante para mostrar y vender sitios web prediseñados.

## Ejecución de la Aplicación (Local)

Para desarrollo local, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/correo11011correo-netizen/Mercadopaginas.git
    cd Mercadopaginas
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # En Linux/macOS:
    python3 -m venv .venv && source .venv/bin/activate
    # En Windows:
    # python -m venv .venv && .\.venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000`.

---

## Documentación de Despliegue en Servidor (Producción)

Esta sección documenta la configuración actual del servidor en producción.

### Resumen de la Pila Tecnológica

-   **Proveedor Cloud:** Google Cloud Platform (GCP)
-   **Instancia:** VM con Debian 11 (Bullseye)
-   **Servidor Web:** Apache 2.4
-   **Servidor de Aplicación:** Módulo `mod_wsgi` para Python 3
-   **Framework:** Flask
-   **Seguridad:** Certificado SSL/TLS de Let's Encrypt (gestionado con Certbot)

### Pasos Clave de la Configuración

1.  **Clonación del Repositorio:** El proyecto se clona en `/var/www/html/Mercadopaginas`.

2.  **Dependencias del Sistema:** Se instalan paquetes esenciales:
    -   `python3-pip`
    -   `apache2`
    -   `libapache2-mod-wsgi-py3`
    -   `certbot` y `python3-certbot-apache`

3.  **Dependencias de Python:** Las dependencias del proyecto se instalan globalmente usando `pip3 install -r requirements.txt`.

4.  **Configuración de Apache (`mod_wsgi`):**
    -   **Script de Entrada WSGI:** Se crea un archivo `wsgi.py` en la raíz del proyecto para que `mod_wsgi` pueda encontrar la instancia de la aplicación Flask.
    -   **Configuración del Sitio:**
        -   Se crea un archivo de configuración global en `/etc/apache2/conf-available/wsgi-mercadopaginas.conf` para definir el proceso `WSGIDaemonProcess` de forma centralizada y evitar conflictos.
        -   El archivo principal de configuración SSL es `/etc/apache2/sites-available/mercadopaginas-le-ssl.conf`. Este archivo gestiona las peticiones HTTPS para `www.mercadopaginas.com` y `mercadopaginas.com`, y las pasa a la aplicación Flask a través de `WSGIScriptAlias`.
        -   El archivo `/etc/apache2/sites-available/mercadopaginas.conf` gestiona las peticiones HTTP y las redirige automáticamente a HTTPS.

5.  **Permisos de Archivos:** El directorio del proyecto `/var/www/html/Mercadopaginas` tiene como propietario al usuario y grupo `www-data` (`chown -R www-data:www-data ...`) para que Apache pueda leer los archivos de la aplicación.

6.  **Configuración de Firewall (GCP):**
    -   Se han creado reglas de firewall en GCP para permitir el tráfico entrante en los puertos:
        -   **TCP 80 (HTTP):** Para la redirección inicial y la validación de Certbot.
        -   **TCP 443 (HTTPS):** Para el tráfico seguro del sitio.
    -   Estas reglas se aplican a la instancia mediante etiquetas de red.

7.  **Certificado SSL:** Se utiliza `certbot` para obtener y renovar automáticamente los certificados SSL/TLS, y para configurar Apache.
