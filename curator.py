from itertools import product
import numpy
import random


class Curator:
    """Database curator that creates and queries databases for analysts

    :param float epsilon: privacy parameter
    :ivar float epsilon: privacy parameter
    :ivar database: private content network
    """

    def __init__(self, epsilon=100):
        self.epsilon = epsilon
        self.database = None

    @staticmethod
    def exponential_mechanism(epsilon, utilities):
        """Return a list of probabilities generated from the utilities

        :return: list of probabilities generated from the utilities
        :rtype: list
        """
        weights = numpy.exp(0.5 * epsilon * numpy.array(utilities))
        return list(weights / sum(weights))

    def query(self, length, preferences):
        """Return a list of nodes picked with the exponential mechanism

        Each step in this sequence is picked by running the exponential
        mechanism on the utilities of links leaving the previous node.

        The utility is 0 for any undefined links, but the probability is not.

        The first node is always the first node in self.database.nodes.

        :return: list of nodes picked with the exponential mechanism
        :rtype: list
        """
        sequence = [self.database.nodes[0]]
        for sequence_step in range(length - 1):
            this_node = sequence[-1]
            utilities = [0 if (node not in this_node.links
                               or preferences[this_node] not in this_node.links[node])
                         else this_node.links[node][preferences[this_node]].utility
                         for node in self.database.nodes]
            probabilities = Curator.exponential_mechanism(self.epsilon, utilities)
            shuffled_probabilities = probabilities[:]
            random.shuffle(shuffled_probabilities)
            next_probability = numpy.random.choice(shuffled_probabilities, p=shuffled_probabilities)
            # In case of equal probabilities, eliminate earlier-in-list bias
            next_probability_indices = [i for i, x in enumerate(probabilities) if x == next_probability]
            next_node_index = random.choice(next_probability_indices)
            next_node = self.database.nodes[next_node_index]
            sequence.append(next_node)
        return sequence

    @staticmethod
    def sequence_probabilities(nodes, preferences, epsilon, sequence_length):
        """Return a list of probabilities for every possible sequence

        :return: list of probabilities for every possible sequence
        :rtype: list
        """
        sequences = list(product(nodes, repeat=sequence_length))
        sequence_probabilities = [1.0 / len(nodes)] * len(sequences)
        progress_bar_size = 50
        progress_step = 2
        print '|' + ' ' * progress_bar_size + '|',
        for sequence_index in range(len(sequences)):
            if not sequence_index % (len(sequences) * progress_step / 100) and sequence_index:
                progress_percent = int(100 * sequence_index / len(sequences))
                print('\r|' + '-' * (progress_percent * progress_bar_size / 100) +
                      ' ' * ((100 - progress_percent) * progress_bar_size / 100) + '|'),
            for sequence_step in range(sequence_length - 1):
                this_node = sequences[sequence_index][sequence_step]
                next_node = sequences[sequence_index][sequence_step + 1]
                response = preferences[nodes.index(this_node)]
                utilities = []
                for other_node in nodes:
                    try:
                        utilities.append(this_node.links[other_node][response].utility)
                    except KeyError:
                        utilities.append(0)
                probabilities = Curator.exponential_mechanism(epsilon, utilities)
                step_probability = probabilities[nodes.index(next_node)]
                sequence_probabilities[sequence_index] *= step_probability
        print '\r|' + '-' * progress_bar_size + '|'
        assert sum(sequence_probabilities) < 1.0001
        assert sum(sequence_probabilities) > 0.9999
        return sequence_probabilities
