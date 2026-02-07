# Configuración Esencial del Servidor (Apache + WSGI)

Este documento describe las configuraciones críticas de Apache y WSGI necesarias para que la aplicación `Mercadopaginas` funcione en un entorno de producción. **Estas son solo referencias; los archivos de configuración reales del servidor pueden tener ajustes específicos.**

## Archivo de Configuración de WSGI (ej: `/etc/apache2/conf-available/wsgi-mercadopaginas.conf`)

Define el proceso daemon de WSGI para la aplicación Python. Asegúrate de que `python-home` y `python-path` apunten a las ubicaciones correctas en tu servidor.

```apache
WSGIDaemonProcess mercadopaginas python-home=/usr python-path=/var/www/html/Mercadopaginas
```

## Configuración del Virtual Host (ej: `/etc/apache2/sites-available/mercadopaginas-le-ssl.conf`)

Esta es la configuración principal para tu dominio, incluyendo SSL.

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName www.mercadopaginas.com
    ServerAlias mercadopaginas.com
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html/Mercadopaginas/templates

    # Sirve index.html por defecto desde el DocumentRoot
    DirectoryIndex index.html

    # Permite el acceso a los archivos de plantilla (Jinja2)
    <Directory /var/www/html/Mercadopaginas/templates>
        Require all granted
    </Directory>

    # Alias para servir archivos estáticos (CSS, JS, imágenes) directamente por Apache
    Alias /static /var/www/html/Mercadopaginas/static
    <Directory /var/www/html/Mercadopaginas/static>
        Require all granted
    </Directory>

    # El WSGIProcessGroup debe coincidir con el nombre definido en WSGIDaemonProcess
    WSGIProcessGroup mercadopaginas
    # Redirige todo el tráfico que no es estático a la aplicación Python
    WSGIScriptAlias / /var/www/html/Mercadopaginas/wsgi.py

    # Logs de errores y acceso
    ErrorLog /var/log/apache2/error.log
    CustomLog /var/log/apache2/access.log combined

    # Configuración SSL (generada por Certbot, si aplica)
    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/mercadopaginas.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/mercadopaginas.com/privkey.pem
</VirtualHost>
</IfModule>
```
