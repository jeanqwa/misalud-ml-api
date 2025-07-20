# Imagen base
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto que usará gunicorn
EXPOSE 10000

# Comando para iniciar gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
