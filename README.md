# MercadoPaginas - Edición Flask

Este proyecto es una versión basada en Python y Flask del sitio web original de MercadoPaginas. Sirve como un catálogo simple y elegante para mostrar y vender sitios web prediseñados. El proyecto original basado en PHP ha sido refactorizado para utilizar un framework web moderno de Python para facilitar su mantenimiento y desarrollo.

## Estructura del Proyecto

```
.
├── app.py              # Archivo principal de la aplicación Flask
├── requirements.txt    # Dependencias de Python
├── .gitignore          # Archivos a ignorar por Git
├── static/             # Archivos estáticos (CSS, JavaScript, imágenes)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/          # Plantillas HTML (Jinja2)
    ├── index.html
    └── demos/
        └── ... (archivos HTML para las demos de los sitios)
```

## Prerrequisitos

- Python 3.8 o superior
- Módulos `pip` y `venv` para Python (generalmente incluidos, pero puede ser necesario instalarlos por separado en algunos sistemas, por ejemplo, `sudo apt install python3-venv`)

## Instalación y Configuración

Sigue estos pasos para poner en marcha la aplicación en tu servidor local.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/correo11011correo-netizen/Mercadopaginas.git
    cd Mercadopaginas
    ```

2.  **Crea y activa un entorno virtual:**
    Es muy recomendable utilizar un entorno virtual para gestionar las dependencias específicas del proyecto.

    *   **En Linux/macOS:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

    *   **En Windows:**
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```

3.  **Instala las dependencias:**
    Con tu entorno virtual activado, instala los paquetes necesarios desde el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución de la Aplicación

Una vez completada la instalación, puedes ejecutar el servidor de desarrollo:

```bash
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000` en tu navegador web.

El servidor se ejecuta en modo de depuración, lo que significa que se recargará automáticamente cuando realices cambios en el código.
