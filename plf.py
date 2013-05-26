from af import AF
from node import Node
import sys
import os.path


class PLF:
    def __init__(self):

        args = sys.argv

        validActions = ['minimizar']

        if (len(args) < 2) or (args[1] not in validActions):
            print "Tienes que ingresar una accion valida."
            sys.exit()

        action = args[1]

        if action == "minimizar":
            return self.minimizar(args)

    def _loadFromFile(self, af, filename):
        if not os.path.isfile(filename):
            print "El archivo indicado no existe."
            sys.exit()

        f = open(filename)

        for line in f:
            line = line.rstrip()
            data = line.split()

            if len(data) > 2:
                nodeName = data[0]
                final = True if data[1] == "S" else False

                node = Node(nodeName, final)

                del data[:1]

                for transition in data:
                    transition = transition.split(":")
                    if len(transition) == 2:
                        node.addTransition(transition[0], transition[1])

                af.addNode(node)

    def _writeOnFile(self, af, filename):
        f = open(filename, "w")

        for nodeName, node in af.getNodes().iteritems():
            line = "%s %s" % (node.getName(), "S" if node.isFinal() else "N")

            for symbol, transition in node.getTransitions().iteritems():
                for destinationNode in transition:
                    line += " %s:%s" % (symbol, destinationNode)

            line += "\n"
            f.write(line)

        f.close()

    def minimizar(self, args):
        if (len(args) < 4):
            print "El uso del programa debe ser: %s %s <archivo de datos> <archivo de resultado>" % (args[0], args[1])
            sys.exit()

        dataFile = args[2]
        resultFile = args[3]

        af = AF()

        self._loadFromFile(af, dataFile)

        af.minimize()

        self._writeOnFile(af, resultFile)

        print "Minimizacion terminada correctamente, el AFD de resultado esta en: %s" % (resultFile)

PLF()
