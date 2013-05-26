import collections


class Node:
    def __init__(self, name, final):
        self.name = name
        self.final = final
        self.transitions = collections.OrderedDict()

    def addTransition(self, symbol, destination):
        if not symbol in self.transitions:
            self.transitions[symbol] = []

        if not destination in self.transitions[symbol]:
            self.transitions[symbol].append(destination)

    def getTransition(self, symbol):
        if symbol in self.transitions:
            return self.transitions[symbol]
        else:
            return []

    def removeTransition(self, symbol):
        del self.transitions[symbol]

    def getName(self):
        return self.name

    def getTransitions(self):
        return self.transitions

    def isFinal(self):
        return self.final

    def replaceTransition(self, validNode, duplicatedNode):
        for symbol, transition in self.transitions.iteritems():
            for index, nodeName in enumerate(transition):
                if nodeName == duplicatedNode:
                    transition[index] = validNode

    def __repr__(self):
        return "<Node name='%s', isFinal='%s', transitions='%s'>\n" % (self.name, self.final, self.transitions)
