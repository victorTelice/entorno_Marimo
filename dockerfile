# Dockerfile
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer el puerto donde correrá marimo
EXPOSE 8888

# Comando por defecto para correr Marimo
CMD ["marimo", "run", "app.py", "--host=0.0.0.0", "--port=8888"]