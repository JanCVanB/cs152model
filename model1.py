import numpy as np
import numpy.random as random
import matplotlib.pyplot as pl
import sys
import plot_defaults

##################
### Parameters ###

num_songs = 1e2 # number of songs in songspace
frac = 1e-1 # fraction of songs in songspace that are intended
power = 1e0 # for skewing the utilities toward 0 (power > 1) or 1 (power < 1)

##################

def pick_song(probs_all):
    # songs indicies are 0 to num_songs - 1, with intended songs occupying lower indices
    return random.choice(int(num_songs), p=probs_all)

def KL_divergence(distribution, approx_distribution):
    return np.sum(distribution * np.log(distribution / approx_distribution))

def pirate(N, eta, probs_all):
    '''
    Pirate by listening `N` times. `eta` is the multiplicative weights update parameter.
    ''' 
    weights = np.ones(num_songs)
    probs = weights / np.sum(weights)
    for _ in range(int(N)):
        song = pick_song(probs_all)
        weights[song] *= np.exp(eta)
        probs = weights / np.sum(weights)
    return KL_divergence(probs_all, probs)

################
### Plotting ###

num_Ns = 50
upper_N_exponent = 4
ntrials = 10 # trials at each N, epsilon value
eta = 1e-3

fig = pl.figure(figsize=(10,8))
fig.subplots_adjust(left=0.2)
fig.subplots_adjust(bottom=0.16)
fig.subplots_adjust(top=0.85)
fig.subplots_adjust(right=0.85)

for epsilon in (0.1, 1, 10, 100):

    num_intended = frac * num_songs
    num_unintended = num_songs - num_intended
    utilities = (random.random(size=num_intended))**power # sensitivity assumed 1

    intended_weights = np.exp(0.5 * epsilon * utilities)
    intended_weight = np.sum(intended_weights)
    unintended_weight = num_unintended

    # probabilities we pick X
    prob_intended = intended_weight / (intended_weight + unintended_weight)
    probs_intended = intended_weights / (intended_weight + unintended_weight)
    probs_unintended = np.ones(num_unintended) / (intended_weight + unintended_weight)
    probs_all = np.concatenate((probs_intended, probs_unintended))

    print "Probability a given picked song is intended: ", prob_intended

    # setup toolbar
    toolbar_width = num_Ns
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    Ns = np.logspace(-1, upper_N_exponent, num=num_Ns)
    div_means = []
    div_stds = []

    for N in Ns:
        divs = []
        for _ in range(ntrials):
            divs.append(pirate(N, eta, probs_all))
        div_means.append(np.mean(divs))
        div_stds.append(np.std(divs))
        sys.stdout.write("-")
        sys.stdout.flush()


    pl.plot(Ns, div_means, lw=8, label=r"\(\varepsilon = {}\)".format(epsilon))

pl.xlabel('Number of queries')
pl.ylabel('KL-divergence')
pl.xscale('log')
pl.yscale('log')
pl.legend(loc="center left")
pl.show()