# Manejo de Automatas Finitos
###### Procesamiento de Lenguajes Formales - USACH 2013

### Integrantes
* Valentino Carmona
* Eric Pérez
* Juan Pablo Verdejo

### Requisitos
* El programa está escrito en Python 2.7
* Fue probado en OSX Mountain Lion y en Ubuntu 10.04

### Funciones disponibles
* Minimizacion de AFD
  * Esta funcion minimiza un AFD leído desde un archivo y guarda el resultado en otro archivo. 
    * ```python plf.py minimizar <archivo de datos> <archivo de resultado>```.
    * Por ejemplo: ```python plf.py minimizar data.txt resultado.txt```
* Transformacion de AFND a AFD
  * Esta funcion transforma un AFND leído desde un archivo y lo guarda en otro, además da la opción de minimizar el resultado automaticamente
    * ```python plf.py afd <archivo de datos> <archivo de resultado> [minimo]```.
    * Por ejemplo: ```python plf.py afd data2.txt resultado.txt minimo```
* Validar secuencia
  * Esta funcion valida una secuencia dado un AF
    * ```python plf.py validar <archivo de datos> [secuencia] (Si no se pasa una secuencia se analiza la palabra vacia) ```.
    * Por ejemplo: ```python plf.py validar data.txt 101```
* Complementar AFD
  * Esta funcion complementa un AF
    * ```python plf.py complemento <archivo de datos> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py complemento data.txt resultado.txt```
* "Potenciar" AFD
  * Esta funcion potencia a "n" un AF
    * ```python plf.py potencia <archivo de datos> <archivo de resultado> <potencia [entero]>```.
    * Por ejemplo: ```python plf.py potencia data.txt resultado.txt 3```
* Estrella de kleene a AF
  * Esta funcion aplica la funcion estrella de kleene a un AF
    * ```python plf.py kleene <archivo de datos> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py kleene data.txt resultado.txt```
* Aceptar palabra vacia
  * Esta funcion permite que el AF acepte la palabra vacia, es decir AF U {<palabra vacia>}
    * ```python plf.py aceptarVacia <archivo de datos> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py aceptarVacia data.txt resultado.txt```
* NO aceptar palabra vacia
  * Esta funcion elimina la aceptacion de la palabra vacia en un AF, es decir AF - {<palabra vacia>}
    * ```python plf.py aceptarVacia <archivo de datos> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py aceptarVacia data.txt resultado.txt```
* Union de AFs
  * Esta funcion une 2 AFs
    * ```python plf.py union <archivo de datos 1> <archivo de datos 2> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py union data.txt data2.txt resultado.txt```
* Concatenacion de AFs
  * Esta funcion concatena 2 AFs
    * ```python plf.py concatenacion <archivo de datos 1> <archivo de datos 2> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py concatenacion data.txt data2.txt resultado.txt```
* Interseccion de AFs
  * Esta funcion intersecta 2 AFs
    * ```python plf.py interseccion <archivo de datos 1> <archivo de datos 2> <archivo de resultado> ```.
    * Por ejemplo: ```python plf.py interseccion data.txt data2.txt resultado.txt```
    
### Formato de archivos
Los AF se escriben en archivos de texto con las siguientes caracteristicas:
* Cada linea representa un nodo y tiene varios parametros separados por espacio
  * Primer parametro: Nombre del nodo. Este no puede ser del tipo "tempNUMERO", cualquier otra palabra alfanumérica está permitida.
  * Segundo parametro: Nodo final. Identifica si e nodo es final con una "S" si lo es o una "N" en caso contrario.
  * Siguientes parametros: Transiciones. Las transiciones se definen como ```simbolo:nodo```, sin espacios. El simbolo "E" se usa para la palabra vacía.

####_*IMPORTANTE*_: El primer nodo del archivo se asumirá como el nodo inicial.

Ejemplo de AF en archivo:
<pre>A S 0:A 1:B
B N 0:B 1:C
C N 0:A 1:C</pre>

En el repositorio se encuentran 2 archivos de datos:
* data.txt: AFD con 12 nodos. No minimizado.
* data2.txt: AFND con 17 nodos. Incluye transiciones vacías.

Los archivos de resultado se escriben con el mismo formato indicado.

### Repositorio
Repositorio hosteado en [github](https://github.com/jpverdejo/plf)
