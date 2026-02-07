# MercadoPaginas - Edición Flask

Este proyecto es una versión basada en Python y Flask del sitio web original de MercadoPaginas, diseñado para ser desplegado en un servidor de producción con Apache y `mod_wsgi`.

---

## Despliegue Rápido en una Instancia Debian Nueva

Esta guía te permitirá desplegar el proyecto en una nueva instancia de Google Cloud (o cualquier servidor Debian/Ubuntu) desde cero.

### Prerrequisitos

1.  Una instancia de VM Debian 11 (Bullseye) en Google Cloud.
2.  Un nombre de dominio apuntando a la IP externa de tu instancia.
3.  `gcloud` CLI instalado y configurado en tu máquina local.

### Paso 1: Configurar el Firewall de GCP

Desde tu terminal local, ejecuta estos comandos para permitir el tráfico web a tu instancia. Reemplaza `your-instance-name` con el nombre de tu VM.

```bash
# Permitir tráfico HTTP (Puerto 80)
gcloud compute firewall-rules create allow-http --allow tcp:80 --target-tags=http-server

# Permitir tráfico HTTPS (Puerto 443)
gcloud compute firewall-rules create allow-https --allow tcp:443 --target-tags=https-server

# Aplicar las etiquetas a tu instancia
gcloud compute instances add-tags your-instance-name --tags=http-server,https-server
```

### Paso 2: Clonar el Repositorio en la Instancia

Conéctate a tu instancia vía SSH y clona este repositorio. Es recomendable clonarlo en `/var/www/` para mantener una estructura organizada.

```bash
# Conéctate a tu instancia
gcloud compute ssh your-instance-name

# Conviértete en superusuario
sudo -i

# Crea el directorio y clona el proyecto
mkdir -p /var/www/
cd /var/www/
git clone https://github.com/correo11011correo-netizen/Mercadopaginas.git
cd Mercadopaginas

# Establece los permisos correctos para Apache
chown -R www-data:www-data .
```

### Paso 3: Ejecutar el Script de Despliegue

El repositorio incluye un script que automatiza toda la configuración del servidor.

```bash
# Desde /var/www/Mercadopaginas, ejecuta:
./deploy.sh
```
El script se encargará de instalar todas las dependencias y configurar Apache para servir el sitio en HTTP. **Importante:** Asegúrate de haber editado el archivo `mercadopaginas.conf` creado por el script si tu dominio no es `mercadopaginas.com`.

### Paso 4: Configurar SSL con Certbot

El último paso es asegurar tu sitio con un certificado SSL gratuito.

1.  **Instala Certbot:**
    ```bash
    sudo apt-get install -y certbot python3-certbot-apache
    ```

2.  **Ejecuta Certbot:**
    Sigue las instrucciones en pantalla. Certbot detectará tu dominio desde la configuración de Apache, obtendrá un certificado y configurará automáticamente el sitio para HTTPS, incluyendo la redirección.
    ```bash
    sudo certbot --apache
    ```

¡Y listo! Tu aplicación ahora está desplegada y sirviéndose de forma segura.

---

## Modificación y Desarrollo Local

Para realizar cambios o añadir nuevas funcionalidades, sigue estos pasos para configurar un entorno de desarrollo en tu máquina local.

1.  **Clonar el repositorio (si aún no lo has hecho):**
    ```bash
    git clone https://github.com/correo11011correo-netizen/Mercadopaginas.git
    cd Mercadopaginas
    ```

2.  **Crear y activar un entorno virtual:**
    Esto aísla las dependencias del proyecto y evita conflictos con otros proyectos de Python.
    ```bash
    # Crear el entorno virtual (solo se hace una vez)
    python3 -m venv .venv

    # Activar el entorno (debes hacerlo cada vez que empieces a trabajar)
    source .venv/bin/activate
    ```
    *Nota: Si estás en Windows, la activación se hace con `.\\.venv\\Scripts\\activate`.*

3.  **Instalar las dependencias:**
    Con el entorno activado, instala las librerías necesarias.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el servidor de desarrollo:**
    El servidor de Flask se recargará automáticamente cada vez que guardes un cambio en los archivos.
    ```bash
    python app.py
    ```

5.  **Visualizar la página:**
    Abre tu navegador web y visita [http://127.0.0.1:5000](http://127.0.0.1:5000) para ver la aplicación en funcionamiento.

¡Ahora estás listo para modificar el código! Cuando termines, simplemente detén el servidor en la terminal con `Ctrl + C`.
