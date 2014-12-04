from itertools import product
from random import random


class Network:
    """Network of Nodes connected by weighted Links

    :param int size: number of Nodes
    :param float density: fraction of defined Links over all Links
    :param float interactivity: number of user inputs possible at every Node
    :param float skew_power: Link utility distribution power (u~x^SP on (0, 1))
    :ivar int size: number of nodes
    :ivar float density: fraction of defined Links over all links
    :ivar float interactivity: number of user inputs possible at every Node
    :ivar float skew_power: Link utility distribution power (u~x^SP on (0, 1))
    :ivar list nodes: all Nodes
    """

    def __init__(self, size=10, density=0.1, interactivity=2, skew_power=1):
        self.size = size
        self.density = density
        self.interactivity = interactivity
        self.skew_power = skew_power
        self.nodes = []
        self.make_nodes()
        self.make_random_links()

    def make_nodes(self):
        """Make list of self.size Nodes
        """
        self.nodes = [Node(name='Node' + str(n + 1)) for n in range(self.size)]

    def make_random_links(self):
        """Make random-utility Links for self.density fraction of self.nodes

        Links are defined for a specific combination of source, destination, and
        response, where the response is the user input at the source Node
        """
        for source, destination in product(self.nodes, self.nodes):
            # Do not link a node to itself
            if source == destination:
                continue
            for response in range(self.interactivity):
                # Skip some pairs, according to ``self.density``
                if random() > self.density:
                    continue
                # Draw utility from x^skew_power on (0, 1)
                utility = random() ** self.skew_power
                link = Link(source, destination, response, utility)
                try:
                    source.links[destination][response] = link
                except KeyError:
                    source.links[destination] = {response: link}


class Link:
    """Link in a Network, connecting two source and destination Nodes

    :param source: source Node
    :param destination: destination Node
    :param int response: user input at source Node
    :param float utility: utility of use
    :ivar source: source Node
    :ivar destination: destination Node
    :ivar int response: user input at source Node
    :ivar float utility: utility of use
    """

    def __init__(self, source, destination, response, utility):
        self.source = source
        self.destination = destination
        self.response = response
        self.utility = utility

    def __repr__(self):
        return ('Link ' + str(self.source) + ' to ' + str(self.destination) +
                ' \t if %d \t utility %.3g' % (self.response, self.utility))

    def __str__(self):
        return ('Link ' + str(self.source) + ' to ' + str(self.destination) +
                ' \t if %d \t utility %.3g' % (self.response, self.utility))


class Node:
    """Node in a Network, connected to other nodes by weighted Links

    :param str name: node ID or descriptor
    :ivar str name: node ID or descriptor
    :ivar dict links: neighbor Nodes keying to Links
    """

    def __init__(self, name):
        self.name = name
        self.links = {}

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name