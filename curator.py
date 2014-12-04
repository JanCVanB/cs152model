from itertools import product
import numpy
from random import randint


class Curator:
    """Database curator that creates and queries databases for analysts

    :param float epsilon: privacy parameter
    :ivar float epsilon: privacy parameter
    """

    def __init__(self, epsilon):
        self.epsilon = epsilon

    @staticmethod
    def exponential_mechanism(epsilon, utilities):
        weights = numpy.exp(0.5 * epsilon * numpy.array(utilities))
        return weights / sum(weights)

    @staticmethod
    def make_random_preferences(network):
        return [randint(0, 1) for _ in network.nodes]

    @staticmethod
    def sequence_probabilities(nodes, preferences, epsilon, sequence_length):
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
