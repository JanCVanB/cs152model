class Adversary:
    """Adversarial analyst that reconstructs the database from repeated queries

    :param float eta: multiplicative weights update power (w <-- w * e^eta)
    :ivar float eta: multiplicative weights update power (w <-- w * e^eta)
    """

    def __init__(self, eta=1e-4):
        self.eta = eta

    @staticmethod
    def normalized(utilities):
        utility_sum = sum(utilities)
        return [utility / utility_sum for utility in utilities]

    def pirate(self, curator, number_of_queries):
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
