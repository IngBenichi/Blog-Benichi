# Imagen base con Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios (requirements primero para aprovechar la cache de Docker)
COPY requirements.txt requirements.txt

# Instalar dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Variables de entorno para la configuración (esto se puede sobreescribir desde docker-compose)
ENV PYTHONUNBUFFERED=1

# Exponer el puerto que usará Django
EXPOSE 8000

# Usar Gunicorn en lugar del servidor de desarrollo
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
