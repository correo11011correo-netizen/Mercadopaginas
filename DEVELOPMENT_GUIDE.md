# Guía de Desarrollo de Mercadopaginas

Este documento explica cómo configurar y ejecutar un entorno de desarrollo local para Mercadopaginas que permite la edición en vivo.

## Requisitos

1.  Tener [Docker](https://www.docker.com/products/docker-desktop/) instalado y en ejecución en tu máquina.
2.  Haber clonado este repositorio.

## Flujo de Trabajo para "Editar en Vivo"

Este método te permite ejecutar la aplicación en un contenedor Docker en tu máquina, pero montando el código fuente local directamente dentro del contenedor. Esto significa que cualquier cambio que guardes en tus archivos se reflejará instantáneamente en la aplicación en ejecución sin necesidad de reconstruir la imagen.

### Paso 1: Construir la Imagen de Desarrollo

Navega al directorio raíz del repositorio en tu terminal y ejecuta el siguiente comando para construir la imagen de Docker. Esto solo necesitas hacerlo la primera vez o cuando cambies las dependencias en `requirements.txt`.

```bash
docker build -t mercadopaginas-dev .
```

### Paso 2: Ejecutar el Contenedor con un Volumen Montado

Ahora, inicia el contenedor. El siguiente comando hace dos cosas importantes:
1.  `-p 8080:8080`: Mapea el puerto 8080 de tu máquina al puerto 8080 del contenedor.
2.  `-v "$(pwd)":/app`: Monta el directorio actual (`pwd`) en la ruta `/app` dentro del contenedor.

```bash
docker run -p 8080:8080 -v "$(pwd)":/app mercadopaginas-dev
```

### Paso 3: ¡A Editar!

¡Listo! La aplicación ahora está corriendo y puedes acceder a ella en tu navegador en `http://localhost:8080`.

Ahora puedes abrir los archivos del proyecto en tu editor de código favorito. **Cada vez que guardes un cambio en un archivo, el servidor Gunicorn dentro del contenedor se reiniciará automáticamente para reflejar el cambio.**
