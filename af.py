import collections
from node import Node
import sys


class AF:
    def __init__(self):
        self.nodes = collections.OrderedDict()
        self.symbols = []

    def getNodes(self):
        return self.nodes

    def addNode(self, node):
        self.nodes[node.getName()] = node
        self.updateSymbols();

    def updateSymbols(self):
        for nodeName, node in self.nodes.iteritems():
            transitions = node.getTransitions()

            for symbol, transition in transitions.iteritems():
                if (not symbol in self.symbols) and symbol != "E":
                    self.symbols.append(symbol)
                    self.symbols.sort()

    def isAFD(self):
        for nodeName, node in self.nodes.iteritems():
            transitions = node.getTransitions()
            if len(transitions) < len(self.symbols):
                return False

            for symbol, destinations in transitions.iteritems():
                if len(str(symbol)) > 1:
                    return False
                if len(destinations) > 1:
                    return False

        return True

    def _getClausura(self, nodes):
        newNodes = nodes[:]

        for nodeName in nodes:
            newNodes += self.nodes[nodeName].getTransition("E")

        newNodes = list(set(newNodes))

        if sorted(nodes) != sorted(newNodes):
            return self._getClausura(sorted(newNodes))
        else:
            return newNodes

    def _getTransitions(self, nodes, symbol):
        transitions = []
        for nodeName in nodes:
            transitions += self.nodes[nodeName].getTransition(symbol)

        transitions = list(set(transitions))

        return self._getClausura(transitions)

    def _newNodeIsFinal(self, nodes):
        for nodeName in nodes:
            if self.nodes[nodeName].isFinal():
                return True

        return False

    def toAFD(self):
        if self.isAFD():
            return self

        tempNodeID = 1

        invalidSymbols = []

        for nodeName, node in self.nodes.iteritems():
            for symbol, transition in node.getTransitions().iteritems():
                if len(symbol) > 1:
                    invalidSymbols.append(symbol)

                    reverseSymbol = symbol[::-1]

                    lastNode = transition
                    tempNodeName = None
                    for i in range(0, (len(reverseSymbol) - 1)):
                        singleSymbol = reverseSymbol[i]

                        tempNodeName = "temp%s" % (tempNodeID)
                        tempNode = Node(tempNodeName, False)

                        for nextNode in lastNode:
                            tempNode.addTransition(singleSymbol, nextNode)

                        self.addNode(tempNode)

                        lastNode = [tempNodeName]

                        tempNodeID += 1

                    node.removeTransition(symbol)
                    node.addTransition(symbol[0], tempNodeName)

        for symbol in invalidSymbols:
            self.symbols.remove(symbol)

        newAF = AF()
        nodesCounter = 0
        nodeNameByTransitions = {}  # Get nodeName using the group of nodes
        transitionsByNodeName = {}  # Get group of Nodes using the nodeName
        nodes = {}
        nodesToIterate = []

        firstNode = self.nodes.itervalues().next()

        transitions = self._getClausura([firstNode.getName()])
        transitionString = '|'.join(str(v) for v in transitions)

        nodeName = "Q" + str(nodesCounter)
        nodeNameByTransitions[transitionString] = nodeName
        transitionsByNodeName[nodeName] = transitions
        nodesToIterate.append(nodeName)
        isFinal = self._newNodeIsFinal(transitions)

        node = Node(nodeName, isFinal)
        newAF.addNode(node)

        nodes[nodeName] = node

        nodesCounter += 1

        for nodeToIterate in nodesToIterate:
            for symbol in self.symbols:
                transitions = self._getTransitions(transitionsByNodeName[nodeToIterate], symbol)
                transitionString = '|'.join(str(v) for v in transitions)

                if transitionString in nodeNameByTransitions:
                    nodes[nodeToIterate].addTransition(symbol, nodeNameByTransitions[transitionString])
                else:
                    nodeName = "Q" + str(nodesCounter)
                    nodeNameByTransitions[transitionString] = nodeName
                    transitionsByNodeName[nodeName] = transitions
                    nodesToIterate.append(nodeName)
                    isFinal = self._newNodeIsFinal(transitions)

                    node = Node(nodeName, isFinal)
                    newAF.addNode(node)

                    nodes[nodeName] = node

                    nodesCounter += 1

                    nodes[nodeToIterate].addTransition(symbol, nodeName)

        newAF.updateSymbols()

        return newAF

    def minimize(self):
        if self.isAFD():
            groups = {}
            groupByName = {}

            for nodeName, node in self.nodes.iteritems():
                groupID = 1

                if node.isFinal():
                    groupID = 2

                if not groupID in groups:
                    groups[groupID] = []

                groups[groupID].append(node)
                groupByName[node.getName()] = groupID

            self._minimize(groups, groupByName)
        else:
            print "No se puede minimizar un AFND, para esto debe ejecutar %s afd %s %s minimo" % (sys.argv[0], sys.argv[2], sys.argv[3])
            sys.exit()

    def _minimize(self, groups, groupByName):
        nextGroupID = 1

        newGroups = {}
        newGroupByName = {}

        for gID, group in groups.iteritems():

            groupByTransitions = {}

            for node in group:
                transitions = node.getTransitions()
                sortedTransitions = []
                transitionGroups = []

                for symbol in self.symbols:
                    sortedTransitions.append(transitions[symbol][0])

                for transition in sortedTransitions:
                    transitionGroups.append(groupByName[transition])

                transitionString = '|'.join(str(v) for v in transitionGroups)

                if transitionString in groupByTransitions:
                    groupID = groupByTransitions[transitionString]
                else:
                    groupID = nextGroupID
                    groupByTransitions[transitionString] = groupID
                    newGroups[groupID] = []

                    nextGroupID += 1

                newGroups[groupID].append(node)
                newGroupByName[node.getName()] = groupID

        if groups == newGroups:
            self._deleteDuplicates(newGroups)
        else:
            self._minimize(newGroups, newGroupByName)

    def _deleteDuplicates(self, groups):

        for groupId, group in groups.iteritems():
            if len(group) > 1:
                validNode = None

                for duplicatedNode in group:
                    if validNode is None:
                        validNode = duplicatedNode
                    else:
                        del self.nodes[duplicatedNode.getName()]

                    for nodeName, node in self.nodes.iteritems():
                        node.replaceTransition(validNode.getName(), duplicatedNode.getName())

    def __repr__(self):
        return "<AF symbols: '%s', nodes: '\n%s'>" % (self.symbols, self.nodes)
