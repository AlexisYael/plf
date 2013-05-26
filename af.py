import collections


class AF:
    def __init__(self):
        self.nodes = collections.OrderedDict()
        self.symbols = []

    def getNodes(self):
        return self.nodes

    def addNode(self, node):
        self.nodes[node.getName()] = node

        transitions = node.getTransitions()

        for symbol, transition in transitions.iteritems():
            if not symbol in self.symbols:
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
