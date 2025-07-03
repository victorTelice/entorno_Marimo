# Imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos al contenedor
COPY pruebacsv.py .
COPY centros-de-consumo-energetico-de-la-administracion-autonoma-de-castilla-y-leon.csv .

# Instala dependencias
RUN pip install --no-cache-dir \
    marimo==0.14.9 \
    pandas \
    matplotlib \
    plotly \
    folium \
    duckdb

# Expone el puerto donde correrá Marimo
EXPOSE 4000

# Comando por defecto para ejecutar la app
CMD ["marimo", "run", "pruebacsv.py", "--port", "4000", "--host", "0.0.0.0"]
