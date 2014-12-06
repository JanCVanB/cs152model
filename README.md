cs152model
==========

Authors: Jan Van Bruggen, Cutter Coryell, James Chang

Model for the privacy of streamed content with respect to complexity,
interactivity, and noisiness

Formulation
-----------

We have structured our model as the canonical privacy problem, with a curator
that protects a database from an adversary capable of making repeated query
attacks in attempt to reconstruct the database.

The Database
------------

The only database model we are
analyzing is an interactive content network of nodes connected by links with
various utilities. At each node, user input (or a user response to a question)
can change the link utilities, so link utility depends on both the nodes and
the user input.

The Curator
-----------

The curator processes all analyst queries to the database and adds noise by
calculating link probabilities according to the exponential mechanism, instead
of simply normalizing the link utilities to obtain link probabilities.

The Adversary
-------------

The adversary reconstructs the database by analyzing the sequence obtained by
querying through the curator. We implement a simple reconstruction algorithm
where the adversary uses multiplicative weights to increase the utility of each
link seen in the sequence. We evaluate the adversary's success with the
KL-Divergence of the probability distributions (over sequences) that represent
the curator's database and the adversary's database.
