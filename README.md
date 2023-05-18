# IDB_Grupo1_InfraestructuraUPM


En este repositorio se va a desarrollar una infraestructura para publicaciones científicas de la UPM.

Para poner en marcha la aplicación primero será necesario guardar en la carpeta con el docker-compose.yml carpeta un fichero .txt con los dois de las publicaciones de los artículos aceptados en  http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/issue/view/286 con:

```dockerfile
docker compose up
```

Esto ejecutará el fichero generarCsv.py y generará los ficheros:

  - Documents.csv: contiene meta-información de las publicaciones
  - Authors.csv: contiene el número de publicaciones por autor

Por otro lado también se generarán los ficheros .json necesarios para realizar los siguientes apartados.

