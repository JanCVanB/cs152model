from adversary import Adversary
from curator import Curator
from database import Network
from matplotlib import pyplot


def test_adversary():
    cutoff_fractions = (0.1, 0.5)
    preference_count = 5
    query_counts = (1, 10, 100, 1000)
    sequence_length = 4

    adversary = Adversary()
    curator = Curator()
    curator.network = Network()
    curator.network.make_random_links()
    preferences = tuple(curator.network.get_random_preferences() for _ in range(preference_count))

    errors = {cutoff_fraction: {preference: [] for preference in preferences}
              for cutoff_fraction in cutoff_fractions}
    for query_count in query_counts:
        adversary.pirate(curator, query_count)
        for preference in preferences:
            adversary_probabilities = sorted(adversary.network.sequence_probabilities(preferences,
                                                                                      sequence_length,
                                                                                      Adversary.normalize),
                                             reverse=True)
            curator_probabilities = sorted(curator.network.sequence_probabilities(preferences,
                                                                                  sequence_length,
                                                                                  curator.exponential_mechanism),
                                           reverse=True)
            for cutoff_fraction in cutoff_fractions:
                cutoff_sequence = cutoff_fraction * len(curator_probabilities)
                adversary_subset = adversary_probabilities[:cutoff_sequence]
                curator_subset = curator_probabilities[:cutoff_sequence]
                error_count = sum(x not in adversary_subset for x in curator_subset)
                errors[cutoff_fraction][preference] = error_count / cutoff_sequence

    for cutoff_fraction in cutoff_fractions:
        for preference in preferences:
            pyplot.plot(range(len(errors[cutoff_fraction][preference])),
                        errors[cutoff_fraction][preference])
    pyplot.show()


def test_network():
    epsilons = [100]
    fractions_of_links_defined = [0.2, 0.4, 0.6, 0.8]
    numbers_of_nodes = [10]
    numbers_of_responses = [2]
    sequence_lengths = [4]
    utility_skew_powers = [1]
    variables = fractions_of_links_defined
    variable_name = 'Fraction of Links Defined'
    number_of_repeat_runs = 5
    print 'Testing model by varying ' + variable_name

    figure, (link_axes, sequence_axes) = pyplot.subplots(2, 1)
    figure.canvas.set_window_title('Content Network with Varying ' + variable_name)
    figure.suptitle(('%.2g Epsilon, %.2g Fraction of Links Defined, %.2g Nodes, ' +
                     '%.2g Responses, %.2g Sequence Length, %.2g Utility Skew Power') %
                    (epsilons[0], fractions_of_links_defined[0], numbers_of_nodes[0],
                     numbers_of_responses[0], sequence_lengths[0], utility_skew_powers[0]),
                    size='large')
    link_axes.set_title('Link Utilities')
    link_axes.set_xlabel('Link Index (Sorted)')
    link_axes.set_ylabel('Link Utility')
    link_colors = [next(link_axes._get_lines.color_cycle) for _ in range(len(variables))]
    sequence_axes.set_title('Sequence Probabilities')
    sequence_axes.set_xlabel('Sequence Index (Sorted)')
    sequence_axes.set_xscale('log')
    sequence_axes.set_ylabel('Sequence Probability')
    sequence_axes.set_yscale('log')
    sequence_colors = [next(sequence_axes._get_lines.color_cycle) for _ in range(len(variables))]

    for run_number in range(len(variables)):
        variable = variables[run_number]
        epsilon = variable if epsilons == variables else epsilons[0]
        fraction_of_links_defined = variable if fractions_of_links_defined == variables else fractions_of_links_defined[0]
        number_of_nodes = variable if numbers_of_nodes == variables else numbers_of_nodes[0]
        number_of_responses = variable if numbers_of_responses == variables else numbers_of_responses[0]
        sequence_length = variable if sequence_lengths == variables else sequence_lengths[0]
        utility_skew_power = variable if utility_skew_powers == variables else utility_skew_powers[0]

        for repeat_run_number in range(number_of_repeat_runs):
            curator = Curator()
            curator.network = Network(size=number_of_nodes,
                                      density=fraction_of_links_defined,
                                      interactivity=number_of_responses,
                                      skew_power=utility_skew_power)
            preferences = curator.network.get_random_preferences()
            print('%d Nodes, %d Responses, Sequences of %d, Density=%.3g, Epsilon=%.3g, Skew=%.3g, Run %d' %
                  (number_of_nodes, number_of_responses, sequence_length, fraction_of_links_defined, epsilon, utility_skew_power, repeat_run_number))
            sequence_probabilities = sorted([probability for probability in
                                             curator.network.sequence_probabilities(preferences, sequence_length, curator.exponential_mechanism)
                                             if probability > 10 ** (- sequence_length)], reverse=True)
            link_utilities = sorted([link.utility for node in curator.network.nodes for links in node.links.values() for link in links.values()], reverse=True)
            assert all(probability for probability in sequence_probabilities)

            label = str(variable) + ' ' + variable_name
            link_color = link_colors[run_number]
            sequence_color = sequence_colors[run_number]
            link_graph, = link_axes.plot(range(len(link_utilities)), link_utilities, c=link_color, lw=3)
            sequence_graph, = sequence_axes.plot(range(len(sequence_probabilities)), sequence_probabilities, c=sequence_color, lw=3)
            if not repeat_run_number:
                link_graph.set_label(label)
                sequence_graph.set_label(label)

    link_axes.legend()
    sequence_axes.legend()
    pyplot.show()


if __name__ == '__main__':
    test_adversary()
    test_network()
