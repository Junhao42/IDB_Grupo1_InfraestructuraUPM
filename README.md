# IDB_Grupo1_InfraestructuraUPM


En este repositorio se va a desarrollar una infraestructura para publicaciones científicas de la UPM.

## Generación de datos estáticos 

Para poner en marcha la aplicación primero será necesario guardar en la carpeta CrearCsvs un fichero .txt con los DOIs de las publicaciones de los artículos aceptados en  http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/issue/view/286. Tras ello es necesario crear la imagen a partir del dockerfile ya existente usando el mandato:

```dockerfile
docker build -t datosestaticos .
```
Después, podemos levantar el contenedor que creará los archivos que necesitemos:

```dockerfile
docker compose up
```

De este forma se ejecutará el fichero generarCsv.py y generarán los ficheros:

  - Documents.csv: contiene meta-información de las publicaciones
  - Authors.csv: contiene el número de publicaciones por autor

Por otro lado, también se generarán los ficheros JSON, necesarios para realizar los siguientes apartados


## Generación de datos dinámicos

Se emplea la infraestructura de hadoop para la generación del fichero Keywords.csv, que contiene el número de apariciones de un término concreto o cualquiera de sus sinónimos. Se puede encontrar dicha infraestructura en  https://github.com/bigdatainf/hadoop-deployment.git, que está basada en el repositorio big-data-europe/docker-hadoop.

Antes de generar el fichero es necesario preparar la infraestructura de hadoop, para ello se deben crear las imágenes pertinentes en las carpetas:
  - base
  - datanode
  - namenode
  - historyserver
  - nodemanager
  - resourcemanager

Cada una de ellas se encuentra en su carpeta correspondiente dentro de la carpeta hadoop-deployment1. En cada una de ellas existe un archivo .bash que crea las imágenes.
Por otro lado, será necesario copiar el fichero metadatos.json del directorio CrearCsvs, en la carpeta /yarn/jobs. Este fichero contiene los datos sobre los que realizaremos el map-reduce
Para obtener el fichero es necesario emplear la imagen proporcionada en la carpeta yarn y ejecutar los siguientes comandos en la terminal:

1. Entrar en la consola hdfs
```cmd
docker exec -it namenode /bin/bash
```

2. Es recomendable crear una carpeta (por ejemplo, "prueba") donde guardaremos los ficheros:

```cmd
hdfs dfs -mkdir -p /prueba/
```

3. Subimos el archivo metadatos.json que hemos generado a la carpeta que hemos creado:

```cmd
hdfs dfs -put metadatos.json /prueba/
```

4. Guardamos un snapshot desde IntellIJ al hacer un asembly y compile de los códigos java proporcionados en la carpeta keywords, esto generará un fichero "elt-hadoop-1.0-SNAPSHOT-jar-with-dependencies.jar" que se tendrá que añadir a la carpeta ./hadoop-deployment/yarn/jobs. Por otro lado también será necesario modificar las palabras que se quieran filtrar:

```py
    private String[] targetWords = {"paper", "Question", "of"};
```

5. Ejecutar el fichero .jar en la consola, esto realizará un mapReduce del fichero que se le proporcione:

```cmd
hadoop jar elt-hadoop-1.0-SNAPSHOT-jar-with-dependencies.jar org.bigdatainf.TMDB_Runner /prueba/metadatos.json /prueba/keywords_output
```

6. Se puede guardar el fichero en local para ver los datos:

```cmd
hdfs dfs -get /prueba/keywords_output/part-r-00000 /app/keywords_output
```

## Soporte para consultas simples

### Articles

Se emplea ElasticSearch para generar un listado ordenado de artículos en los que un autor específico ha participado. Nos apoyaremos de un fichero python para realizar las peticiones web y realizar algunas operaciones simples si son necesarias.

Para desarrollar este punto, tan solo es necesario moverse hasta la carpeta elasticSearch y construir la imagen.

```cmd
docker build -t mi-elasticsearch .
```

Tras ello creamos un contenedor docker montando un volumen en la carpeta data, donde se encuentran los archivos con los datos que usaremos, previamente deberemos haber copiado todos los archivos json (salvo metadatos.json) que se han creado en la carpeta CrearCsvs:

```cmd
"docker run -p 9200:9200 -v "ruta\elasticSearch\data":/usr/share/elasticsearch/data mi-elasticsearch
```

Por último, ejecutamos el fichero .ipynb donde se realizarán las consultas al contenedor docker de elasticSeach mediante el modulo requests de python y se ordenarán los resultados.

### Texts

El objetivo de este apartado es obtener un listado ordenado de párrafos, junto con el título del artículo al que pertenecen, que contienen un término específico. Para ello, de forma similar a la generación del fichero Keywords.csv, se empleará la infraestructura proporcionada por hadoop para realizar map-reduce. Para ello, emplearemos el mismo contenedor que hemos usado anteriormente. Tendremos que copiar los archivos que sean necesarios a la carpeta jobs (asegurarnos de que existe metadatos.json en dicha carpeta), dentro de yarn, y tras ello, repetir los pasos que hicimos en keywords. Además tendríamos que cambiar el mapper, el runner y el reducer y actualizar .jar, sus nuevos códigos se encuentran dentro de la carpeta texts.

```cmd
hadoop jar .jar org.bigdatainf.TMDB_Runner /prueba/metadatos.json /prueba/salidaText
```

```cmd
hdfs dfs -get /prueba/salidaText/part-r-00000 /app/salidaText.txt
```

## Soporte para consultas complejas

### Collaborators

Se realizará un listado ordenado de autores relacionados con un autor específico utilizando neo4j, una base de datos centrada en grafos, dado que estamos trabajando con datos con una gran interconectividad, donde priman las relaciones entre nodos.

Para ello, levantaremos un contenedor que tendrá un cluster de nodos de neo4j con varios cores. El proceso es sencillo, primero copiamos el fichero docs.csv, que hemos generado en la carpeta CrearCsvs dentro de la carpeta neo4j/data/core1/backups, teniendo que hacerlo para cada core. Tras ello, accedemos a la interfaz web de uno de los cores (pueden verse dentro del archivo docker-compose.yml) y ya podriamos cargar datos y hacer consultas. Un ejemplo de como cargar los datos sería:

```sql
LOAD CSV WITH HEADERS FROM 'file:///docs.csv' AS row
```
Tanto la forma en la que hemos creado los nodos y las relaciones como la consulta que proponemos, se encuentran en el fichero de texto consulta.txt.

### Words

El objetivo es buscar el número de palabras en el corpus cuya longitud es de un tamaño específico. Para ello, se empleará el método `grep` que se encuentra disponible en los métodos predefinidos en hadoop. 

Para ello primero es necesario añadir el fichero abstracts.csv en la carpeta `/hadoop-deployment1/yarn/jobs` al igual que en apartados anteriores

```cmd
hdfs dfs -put abstract.csv /prueba
```

```cmd
cd $HADOOP_HOME/share/hadoop/mapreduce/ 
```

En este ejemplo buscamos aquellas palabras que tienen una longitud de 4, en caso de querer hacer una consulta diferente, solo es necesario cambiar el número de dígitos a buscar en la expresión regular.

```cmd
yarn jar hadoop-mapreduce-examples-3.3.5.jar grep /prueba/abstracts.csv /prueba/words '\b\w{4}\b'
```


```cmd
hdfs dfs -ls /prueba/words
```


```cmd
hdfs dfs -get /prueba/words/part-r-00000 /app/words_conteo.txt
```
