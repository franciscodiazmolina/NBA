# Utilizar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos y la aplicación
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto que utilizará la aplicación
EXPOSE 8080

# Establecer el comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
