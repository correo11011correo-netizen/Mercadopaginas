# Guía de Recreación Completa del Servidor Web

Este documento contiene todos los pasos necesarios para desplegar la aplicación `Mercadopaginas` en una nueva instancia de máquina virtual (VM) de Debian en Google Cloud.

**Prerrequisitos:**
-   Tener `gcloud` CLI instalado y autenticado en tu máquina local.
-   Tener un proyecto de Google Cloud.
-   El dominio (`mercadopaginas.com`) debe estar apuntando a la IP de la nueva instancia una vez creada.

---

### Paso 1: Crear y Configurar la Instancia en Google Cloud

1.  **Crear la nueva VM.** (Reemplaza `project-2eb71890-6e93-4cfd-a00` si es necesario). Las etiquetas `http-server` y `https-server` son cruciales para las reglas de firewall.

    ```bash
    gcloud compute instances create mercadopaginas-web-server \
        --project=project-2eb71890-6e93-4cfd-a00 \
        --zone=us-central1-a \
        --machine-type=e2-micro \
        --network-tier=PREMIUM \
        --maintenance-policy=MIGRATE \
        --provisioning-model=STANDARD \
        --service-account=237618992928-compute@developer.gserviceaccount.com \
        --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
        --tags=http-server,https-server \
        --create-disk=auto-delete=yes,boot=yes,device-name=instance-1,image=projects/debian-cloud/global/images/debian-11-bullseye-v20240415,mode=rw,size=10,type=projects/gce-ssd-images/zones/us-central1-a/diskTypes/pd-balanced \
        --no-shielded-secure-boot \
        --shielded-vtpm \
        --shielded-integrity-monitoring \
        --labels=goog-ec-src=vm_add-gcloud \
        --reservation-affinity=any
    ```

2.  **Crear las reglas de firewall** para permitir tráfico web (si no existen):

    ```bash
    gcloud compute firewall-rules create allow-http --target-tags http-server --allow tcp:80
    gcloud compute firewall-rules create allow-https --target-tags https-server --allow tcp:443
    ```

### Paso 2: Instalar Dependencias del Sistema

1.  **Conéctate a la nueva instancia:**

    ```bash
    gcloud compute ssh mercadopaginas-web-server --zone=us-central1-a
    ```

2.  **Actualiza el sistema e instala todo el software necesario:**

    ```bash
    sudo apt-get update
    sudo apt-get install -y apache2 git python3 python3-pip libapache2-mod-wsgi-py3 python3-certbot-apache
    ```

### Paso 3: Clonar el Repositorio y Configurar Permisos

1.  **Clona el repositorio** en el directorio correcto:

    ```bash
    sudo git clone https://github.com/correo11011correo-netizen/Mercadopaginas /var/www/html/Mercadopaginas
    ```

2.  **Establece los permisos correctos.** Esto es fundamental. Reemplaza `nestorfabianriveros2014` con el nombre de usuario con el que te conectas por SSH si es diferente.

    ```bash
    # Asigna la propiedad al usuario y al grupo de Apache
    sudo chown -R nestorfabianriveros2014:www-data /var/www/html/Mercadopaginas

    # Asigna permisos de escritura al grupo para directorios
    sudo find /var/www/html/Mercadopaginas -type d -exec chmod 775 {} \;

    # Asigna permisos de lectura al grupo para archivos
    sudo find /var/www/html/Mercadopaginas -type f -exec chmod 664 {} \;
    ```

### Paso 4: Instalar Dependencias de Python

1.  **Instala las librerías de Python** listadas en `requirements.txt`:

    ```bash
    sudo pip3 install -r /var/www/html/Mercadopaginas/requirements.txt
    ```

### Paso 5: Configurar Apache y WSGI

1.  **Crea el archivo de configuración para el proceso WSGI:**

    ```bash
    sudo tee /etc/apache2/conf-available/wsgi-mercadopaginas.conf <<EOF
    WSGIDaemonProcess mercadopaginas python-home=/usr python-path=/var/www/html/Mercadopaginas
    EOF
    ```

2.  **Crea el archivo de Virtual Host para el puerto 80 (HTTP):**

    ```bash
    sudo tee /etc/apache2/sites-available/mercadopaginas.conf <<EOF
    <VirtualHost *:80>
        ServerName www.mercadopaginas.com
        ServerAlias mercadopaginas.com
        ServerAdmin webmaster@localhost

        # Alias para servir archivos estáticos (CSS, JS, imágenes)
        Alias /static /var/www/html/Mercadopaginas/static
        <Directory /var/www/html/Mercadopaginas/static>
            Require all granted
        </Directory>

        # Configuración para que Flask/WSGI maneje el resto
        WSGIProcessGroup mercadopaginas
        WSGIScriptAlias / /var/www/html/Mercadopaginas/wsgi.py
        <Directory /var/www/html/Mercadopaginas>
            Require all granted
        </Directory>

        ErrorLog /var/log/apache2/error.log
        CustomLog /var/log/apache2/access.log combined
    </VirtualHost>
    EOF
    ```

3.  **Deshabilita el sitio por defecto y habilita todas las nuevas configuraciones:**

    ```bash
    sudo a2dismod mpm_event
    sudo a2enmod mpm_prefork wsgi headers
    sudo a2enconf wsgi-mercadopaginas
    sudo a2dissite 000-default.conf
    sudo a2ensite mercadopaginas.conf
    ```

4.  **Reinicia Apache** para aplicar los cambios:

    ```bash
    sudo systemctl restart apache2
    ```
    *En este punto, el sitio ya debería funcionar por HTTP.*

### Paso 6: Habilitar SSL (HTTPS) con Certbot

1.  **Ejecuta Certbot.** Seguirá las instrucciones interactivas para obtener y configurar el certificado SSL para `mercadopaginas.com` y `www.mercadopaginas.com`. Generalmente, pedirá un email y aceptar los términos de servicio.

    ```bash
    sudo certbot --apache
    ```

2.  **Certbot modificará tu configuración automáticamente,** creando un archivo `mercadopaginas-le-ssl.conf` y configurando la redirección de HTTP a HTTPS.

### Paso 7: Verificación Final

Apache se reiniciará automáticamente después de que Certbot termine. El sitio web debe estar completamente funcional en `https://www.mercadopaginas.com`.

Puedes verificarlo con `curl`:

```bash
curl -I https://www.mercadopaginas.com
```
Deberías ver una respuesta `HTTP/1.1 200 OK`.

```