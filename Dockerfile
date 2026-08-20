# Usamos una imagen oficial de Python ligera como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente y la carpeta de templates al contenedor
COPY . .

# Exponemos el puerto 8000 que usará FastAPI
EXPOSE 8000

# Comando para iniciar el servidor web cuando arranque el contenedor
# Usamos 0.0.0.0 para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]