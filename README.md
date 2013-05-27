# Manejo de Automatas Finitos
###### Procesamiento de Lenguajes Formales - USACH 2013

### Requisitos
* El programa está escrito en Python 2.7
* Fue probado en OSX Mountain Lion y en Ubuntu 10.04

### Funciones disponibles
* Minimizacion de AFD
  * Esta funcion minimiza un AFD leído desde un archivo y guarda el resultado en otro archivo. 
    * ```python plf.py minimizar <archivo de datos> <archivo de resultado>```. Por ejemplo: ```python plf.py minimizar data.txt resultado.txt```
* Transformacion de AFND a AFD
  * Esta funcion transforma un AFND leído desde un archivo y lo guarda en otro, además da la opción de minimizar el resultado automaticamente
    * ```python plf.py afd <archivo de datos> <archivo de resultado> [minimo]```. Por ejemplo: ```python plf.py minimizar data.txt resultado.txt minimo```
    
### Formato de archivos
Los AF se escriben en archivos de texto con las siguientes caracteristicas:
* Cada linea representa un nodo y tiene varios parametros separados por espacio
  * Primer parametro: Nombre del nodo. Este no puede ser del tipo "tempNUMERO", cualquier otra palabra alfanumérica está permitida
  * Segundo parametro: Nodo final. Identifica si e nodo es final con una "S" si lo es o una "N" en caso contrario
  * Siguientes parametros: Transiciones. Las transiciones se definen como ```simbolo:nodo```, sin espacios. El simbolo "E" se usa para la palabra vacía.

Ejemplo de AF en archivo:
```A S 0:A 1:B
B N 0:B 1:C
C N 0:A 1:C```

En el repositorio se encuentran 2 archivos de datos:
* data.txt: AFD con 12 nodos. No minimizado.
* data2.txt: AFND con 17 nodos. Incluye transiciones vacías.

Los archivos de resultado se escriben con el mismo formato indicado.
