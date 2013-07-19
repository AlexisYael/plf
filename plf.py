from af import AF
from node import Node
import sys
import os.path
import copy


class PLF:
    def __init__(self):

        args = sys.argv

        validActions = ["minimizar", "afd", "validar", "complemento",
                        "potencia", "kleene", "aceptarVacia", "noAceptarVacia",
                        "union", "concatenacion", "interseccion"]

        if (len(args) < 2) or (args[1] not in validActions):
            print "Tienes que ingresar una accion valida."
            sys.exit()

        action = args[1]

        if action == "minimizar":
            return self._minimizar(args)

        if action == "afd":
            return self._toAFD(args)

        if action == "validar":
            return self._validar(args)

        if action == "complemento":
            return self._complemento(args)

        if action == "potencia":
            return self._potencia(args)

        if action == "kleene":
            return self._kleene(args)

        if action == "aceptarVacia":
            return self._aceptarVacia(args)

        if action == "noAceptarVacia":
            return self._noAceptarVacia(args)

        if action == "union":
            return self._union(args)

        if action == "concatenacion":
            return self._concatenacion(args)

        if action == "interseccion":
            return self._interseccion(args)

    # Metodo que carga un AF desde un archivo
    def _loadFromFile(self, af, filename):
        if not os.path.isfile(filename):
            print "El archivo indicado no existe."
            sys.exit()

        f = open(filename)

        # Leemos el archivo linea a linea
        for line in f:
            # Removemos el salto de linea final
            line = line.rstrip()

            # Dividimos la linea usando un espacio como separacion
            data = line.split()

            # Verificamos que tenga mas de 1 parametro
            # (Se requiere por lo menos el nombew y si es final o no)
            if len(data) > 1:
                # Usamos la primera palabra como nombre del nodo
                nodeName = data[0]

                # Usamos la segunda palabra para verificar si es un nodo final o no
                # Si es "S", es final, en otro caso no lo es
                final = True if data[1] == "S" else False

                # Creamos el nodo con esos 2 parametros y los borramos de la lista
                # Para luego iterar sobre las transiciones
                node = Node(nodeName, final)

                del data[:1]

                # Analizamos transicion a transicion
                for transition in data:
                    # Separamos la palabra usando ":", si la lista resultante tiene 2 entradas
                    # (Simbolo y estado al que avanza)
                    transition = transition.split(":")
                    if len(transition) == 2:
                        # Si es valido se agrega la transicion al nodo
                        node.addTransition(transition[0], transition[1])

                # Se agrega el nodo al AF
                af.addNode(node)

    # Metodo que escribe un AF en un archivo
    def _writeOnFile(self, af, filename):
        f = open(filename, "w")

        # Iteramos sobre los nodos del AF
        for nodeName, node in af.getNodes().iteritems():
            # Creamos un string con los 2 primeros parametros del nodo, el nombre y si es final o no
            line = "%s %s" % (node.getName(), "S" if node.isFinal() else "N")

            # Recorremos todas las transiciones del nodo
            for symbol, transition in node.getTransitions().iteritems():
                for destinationNode in transition:
                    # Agregamos cada transicion al string que se imprimira
                    line += " %s:%s" % (symbol, destinationNode)

            # Se agrega un salto de linea y se escribe en el archivo
            line += "\n"
            f.write(line)

        # Se cierra el archivo
        f.close()

    #Metodo que lanza el proceso de minimizacion de un AFD
    def _minimizar(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde el archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos la minimizacion
        af.minimize()

        # Escribimos el AD minimizado en un archivo
        self._writeOnFile(af, resultFile)

        print "Minimizacion terminada correctamente, el AFD de resultado esta en: %s" % (resultFile)

    # Metodo que lanza la transformacion de un AFND a un AFD
    def _toAFD(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado> [minimo]" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos el metodo que transforma el AFND a AFD
        af = af.toAFD()

        # Revisamos si el parametro "minimo" fue ingresado
        minimize = False
        if(len(args) > 4 and args[4] == "minimo"):
            minimize = True

        # En caso de ser pedido minimizamos el AFD
        if minimize:
            af.minimize()

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Paso a AFD %sterminado correctamente, el AFD de resultado esta en: %s" % ("minimo " if minimize else "", resultFile)

    # Metodo que valida si una secuencia es valida segun un AF dado
    def _validar(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 3):
            print "El uso del programa debe ser: %s %s <archivo de datos> [secuencia] (Si no se pasa secuencia se analizara la palabra vacia)" % (args[0], args[1])
            sys.exit()

        # Cargamos el nombre del archivo con el AF
        dataFile = args[2]

        # Verificamos si el parametro "secuence" fue pasado, en caso contrario
        # validaremos un string vacio
        secuence = ""
        if len(args) > 3:
            secuence = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde el archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos la validacion
        isValid = af.validateSecuence(secuence)

        # Imprimimos el resultado
        if isValid:
            print "La secuencia '%s' es valida segun el AF determinado en %s" % (secuence, dataFile)
        else:
            print "La secuencia '%s' NO es valida segun el AF determinado en %s" % (secuence, dataFile)

    # Metodo que lanza el proceso de complementacion de un AF
    def _complemento(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos el metodo que transforma el AFND a AFD
        af = af.toAFD()

        # Complementamos el AFD
        af.complement()

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Paso a AFD complementado correctamente, el AFD de resultado esta en: %s" % (resultFile)

    # Metodo que potencia un AF a "n"
    def _potencia(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado> <potencia>" % (args[0], args[1])
            sys.exit()

        n = 1
        try:
            n = int(args[4])
        except:
            print "El uso del programa debe ser: %s %s %s <archivo de resultado> <potencia>" % (args[0], args[1], args[2])
            sys.exit()

        # Cargamos el nombre del archivo con el AF
        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde el archivo
        self._loadFromFile(af, dataFile)

        # Concatenamos una copia del AF a si mismo n-1 veces
        n -= 1

        for i in xrange(n):
            copyAF = copy.deepcopy(af)

            af.concat(copyAF)

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        # Imprimimos el resultado
        print "AF elevado a la %s potencia. Resultado guardado en %s" % (str(n + 1), resultFile)

    # Metodo que lanza el proceso de estrella de kleene en un AF
    def _kleene(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos el proceso en el AFD
        af.kleene()

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "AF transformado a AF* correctamente. Resultado guardado en: %s" % (resultFile)

    # Metodo que lanza el proceso para aceptar la palabra vacia en un AF
    def _aceptarVacia(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos el proceso en el AFD
        af.aceptarVacia()

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Proceso de aceptacion de la palabra vacia en el AF terminado correctamente. Resultado guardado en: %s" % (resultFile)

    # Metodo que lanza el proceso para no aceptar la palabra vacia en un AF
    def _noAceptarVacia(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

        # Ejecutamos el proceso en el AFD
        af.noAceptarVacia()

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Proceso de NO aceptacion de la palabra vacia en el AF terminado correctamente. Resultado guardado en: %s" % (resultFile)

    # Metodo que lanza el proceso de union de 2 AFs
    def _union(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 5):
            print "El uso del programa debe ser: %s %s <archivo de datos 1> <archivo de datos 2> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        dataFileUnion = args[3]
        resultFile = args[4]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

         # Instanciamos el segundo AF
        afUnion = AF()

        # Cargamos el AF desde el segundo archivo
        self._loadFromFile(afUnion, dataFileUnion)

        # Unimos los AFDs
        af.union(afUnion)

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Proceso de union de AFs terminado correctamente. Resultado guardado en: %s" % (resultFile)

    # Metodo que lanza el proceso de concatenacion de 2 AFs
    def _concatenacion(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 5):
            print "El uso del programa debe ser: %s %s <archivo de datos 1> <archivo de datos 2> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        dataFileConcatenacion = args[3]
        resultFile = args[4]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

         # Instanciamos el segundo AF
        afConcatenacion = AF()

        # Cargamos el AF desde el segundo archivo
        self._loadFromFile(afConcatenacion, dataFileConcatenacion)

        # Unimos los AFDs
        af.concat(afConcatenacion)

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Proceso de concatenacion de AFs terminado correctamente. Resultado guardado en: %s" % (resultFile)

    # Metodo que lanza el proceso de interseccion de 2 AFs
    def _interseccion(self, args):
        # Verificamos que tenemos todos los parametros necesarios
        if (len(args) < 5):
            print "El uso del programa debe ser: %s %s <archivo de datos 1> <archivo de datos 2> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        dataFileInterseccion = args[3]
        resultFile = args[4]

        # Instanciamos un AF
        af = AF()

        # Cargamos el AF desde un archivo
        self._loadFromFile(af, dataFile)

         # Instanciamos el segundo AF
        afInterseccion = AF()

        # Cargamos el AF desde el segundo archivo
        self._loadFromFile(afInterseccion, dataFileInterseccion)

        # La interseccion de M1 y M2 se define como:
        # (M1c U M2c)c

        # 1.- Complementamos cada AF
        af.complement()
        afInterseccion.complement()

        # 2.- Unimos el segundo AF al primero
        af.union(afInterseccion)

        # 3.- Complementamos el af de la union
        af.complement()

        # Escribimos el AFD en un archivo
        self._writeOnFile(af, resultFile)

        print "Proceso de interseccion de AFs terminado correctamente. Resultado guardado en: %s" % (resultFile)

# Iniciamos la ejecucion del software
PLF()
