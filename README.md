# IDB_Grupo1_InfraestructuraUPM


En este repositorio se va a desarrollar una infraestructura para publicaciones científicas de la UPM.

## Generación de datos estáticos 

Para poner en marcha la aplicación primero será necesario guardar en la carpeta con el docker-compose.yml carpeta un fichero .txt con los dois de las publicaciones de los artículos aceptados en  http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/issue/view/286 con:

```dockerfile
docker compose up
```

Esto ejecutará el fichero generarCsv.py y generará los ficheros:

  - Documents.csv: contiene meta-información de las publicaciones
  - Authors.csv: contiene el número de publicaciones por autor

Por otro lado también se generarán los ficheros .json necesarios para realizar los siguientes apartados.


## Generación de datos dinámicos

Se emplea la infraestructura de hadoop para la generación del fichero Keywords.csv, que contiene el número de apariciones de un término concreto o cualquiera de sus sinónimos. Se puede encontrar dicha infraestructura en  https://github.com/bigdatainf/hadoop-deployment.git, que está basada en el repositorio big-data-europe/docker-hadoop.

Antes de generar el fichero es necesario preparar la infraestructura de hadoop, para ello se deben crear las imágenes pertinentes en las carpetas:
  - base
  - datanode
  - historyserver
  - namenode
  - nodemanager
  - resourcemanager

Estos se encuentran en hadoop-deployment1

Para obtener el fichero es necesario emplear la imagen proporcionada en la carpeta yarn y ejecutar los siguientes comandos en la terminal:

1. Entrar en la consola hdfs
```cmd
docker exec -it namenode /bin/bash
```

2. Es recomendable crear una carpeta (por ejemplo, "practica2" donde guardaremos los ficheros:

```cmd
hdfs dfs -mkdir -p /practica2/
```

3. Subimos el archivo metadatos.json que hemos generado a la carpeta que hemos creado:

```cmd
hdfs dfs -put metadatos.json /practica2/
```

4. Guardamos un snapshot desde IntellIJ al hacer un asembly y compile de los códigos java proporcionados en la carpeta, esto generará un fichero "elt-hadoop-1.0-SNAPSHOT-jar-with-dependencies.jar" que se tendrá que añadir a la carpeta ./hadoop-deployment/yarn/jobs. Por otro lado también será necesario modificar las palabras que se quieran filtrar:

```py
    private String[] targetWords = {"paper", "Question", "of"};
```

5. Ejecutar el fichero .jar en la consola, esto realizará un mapReduce del fichero que se le proporcione:

```cmd
hadoop jar elt-hadoop-1.0-SNAPSHOT-jar-with-dependencies.jar org.bigdatainf.TMDB_Runner /practica2/metadatos.json /practica2/keywords_output
```

6. Se puede guardar el fichero en local para ver los datos:

```cmd
hdfs dfs -get /practica2/keywords_output/part-r-00000 /app/keywords_output
```

## Soporte para consultas simples

### Articles

Se emplea ElasticSearch mapReduce para generar un listado ordenado de artículos en los que un autor específico ha participado.


### Texts

El objetivo de este apartado es obtener un listado ordenado de párrafos, junto con el título del artículo al que pertenecen, que contienen un término específico. Para ello, similar a la generación del fichero Keywords.csv se empleará la infraestructura proporcionada por hadoop para realizar map-reduce 


## Soporte para consultas complejas

### Collaborators

Se realizará un listado ordenado de autores relacionados con un autor específico utilizando neo4j, una base de datos centrada en grafos, dado el hecho que estamos tratando con datos con gran interconectividad, donde priman las relaciones entre nodos.

Se empleará la imagen de neo4j en local para realizar la prueba

### Words

Se emplearán 
