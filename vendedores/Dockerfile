# Usar la imagen base más ligera de Python 3.12
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el Pipfile y el Pipfile.lock (si lo tienes) al contenedor
COPY Pipfile Pipfile.lock /app/

# Instalar pipenv y las dependencias de la aplicación
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy

# Copiar el resto de los archivos de tu aplicación
COPY . /app

# Comando para ejecutar la aplicación
CMD ["pipenv", "run", "python", "app.py", "production"]