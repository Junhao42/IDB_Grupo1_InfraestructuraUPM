# Utiliza una imagen base de Python
FROM python:3.9

# Copia los archivos de tu aplicación al contenedor
COPY . /app

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias de tu aplicación
RUN pip install pandas
RUN pip install requests

# Especifica el comando por defecto para ejecutar tu aplicación (opcional)
CMD ["python", "generarCsv.py"]