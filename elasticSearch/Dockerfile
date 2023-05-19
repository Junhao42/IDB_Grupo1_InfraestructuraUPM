FROM docker.elastic.co/elasticsearch/elasticsearch:7.15.1

# Instalar plugin ingest-attachment para procesamiento de archivos
RUN elasticsearch-plugin install --batch ingest-attachment

# Establecer configuraciones adicionales de Elasticsearch
ENV discovery.type=single-node
ENV http.cors.enabled=true
ENV http.cors.allow-origin=*

# Añadir la configuración para aumentar el vm.max_map_count
RUN echo "vm.max_map_count=262144" >> /etc/sysctl.conf

# Crea el directorio para el volumen
RUN mkdir -p /usr/share/elasticsearch/data

# Establece los permisos adecuados para el directorio del volumen
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

# Expone el puerto 9200 para acceder a Elasticsearch
EXPOSE 9200

# Define el comando de inicio del contenedor
CMD ["elasticsearch"]