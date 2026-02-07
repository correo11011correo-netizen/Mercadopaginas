# Usar una imagen oficial de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Exponer el puerto en el que la aplicación se ejecutará
EXPOSE 8080

# Comando para iniciar la aplicación usando gunicorn
# Inicia 4 procesos ("workers") para manejar las peticiones
# Escucha en el puerto 8080 en todas las interfaces de red
# El punto de entrada es el objeto 'app' dentro del archivo 'app.py'
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8080", "app:app"]
