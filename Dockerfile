# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente del directorio local al contenedor
COPY . .

# Expón el puerto en el que el contenedor escuchará
EXPOSE 8080

# Establece el comando para ejecutar el script de Python
CMD ["python", "utiliti.py"]
