class Adversary:
    """Adversarial analyst that reconstructs the database from repeated queries

    :param float eta: multiplicative weights update power (w <-- w * e^eta)
    :param curator: curator of the target network
    :ivar float eta: multiplicative weights update power (w <-- w * e^eta)
    :ivar float network: the approximation network
    :ivar float eta: multiplicative weights update power (w <-- w * e^eta)
    """

    def __init__(self, curator, eta=1e-4):
        self.curator = curator
        self.eta = eta
        self.network = Network(size=self.curator.network.size)
        self.preference_combinations = self.network.get_all_preferences()

    @staticmethod
    def normalized(utilities):
        utility_sum = sum(utilities)
        return [utility / utility_sum for utility in utilities]

    def pirate(self, number_of_queries=1):
        """Return a network that approximates curator's network probabilities

        This network's link utilities are normalized to probabilities, rather
        than fed through the exponential mechanism to obtain probabilities.

        :param curator: curator of the target network
        :param int number_of_queries: number of times to query the curator
        """
        network = Network()
        for query_number in range(number_of_queries):
            sequence = curator.query()
            # TODO: reconstruct network
        return network
