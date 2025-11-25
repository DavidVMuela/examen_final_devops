FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

ENV FLASK_ENV=production
ENV PORT=8080

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]