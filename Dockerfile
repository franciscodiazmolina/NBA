# Usa una imagen de Python ligera
FROM python:3.9-slim

# Crea un directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos al contenedor
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Configurar Kaggle (Asegurate de que kaggle.json esté en el repo o usar Secret Manager)
RUN mkdir -p /root/.kaggle && cp kaggle.json /root/.kaggle/kaggle.json && chmod 600 /root/.kaggle/kaggle.json

# Descargar y extraer dataset de Kaggle
RUN kaggle datasets download -d wyattowalsh/basketball && \
    unzip basketball.zip -d basketball_data && \
    rm basketball.zip

# Expone el puerto 8080
EXPOSE 8080

# Comando para ejecutar la app
CMD ["python", "app.py"]
