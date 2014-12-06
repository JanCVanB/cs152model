from operator import mul
from random import randrange, random
from math import exp


# Parameters and debug
DEBUG = 1
INTENDED_FILE_NAME = 'intended.data'
UNINTENDED_FILE_NAME = 'unintended.data'
PLAYED_FILE_NAME = 'played.data'

# Variations per feature for the exponential mechanism. Each song has a certain
# amount of intended verses. These are part of a larger set of total verses that
# may or may not appear. Each output's weight is calculated by whether or not
# an intended piece exists within the song. The exponential mechanism outputs
# intended outputs with a higher chance than unintended outputs, but protects
# intended outputs with the possibility of outputting unintended outputs.
# Intended outputs will have high weights while unintended outputs won't.
INTENDED_VERSES = [2,3,3,4,1,5,6,1,7,9]
TOTAL_VERSES = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
NUM_SONGS = 1000000
NUM_INTENDED_SONGS = 15
NUM_UNINTENDED_SONGS = NUM_SONGS - NUM_INTENDED_SONGS
UNINTENDED_WEIGHT = 0.01
INTENDED_WEIGHT = 1

# How much each intended verse is worth, a song can have a max weight of the
# number of verses * WEIGHT_BONUS
WEIGHT_BONUS = 0.1

# Differential privacy parameter
EPSILON = 1.0

class DPMusic:
    '''Differentially private song generation, using strings for music.'''

    def __init__(self):
        '''Initializes member variables.'''
        if DEBUG: print 'Initializing'

        # Destroy outputs
        f = open(PLAYED_FILE_NAME, 'w')
        f.close()

        # Global sensitivity
        self.sensitivity = WEIGHT_BONUS * len(INTENDED_VERSES)

        # Chance of the intended song playing vs unintended song playing
        propIntended = exp(EPSILON * INTENDED_WEIGHT / (2 * self.sensitivity))
        propUnintended = exp(EPSILON * UNINTENDED_WEIGHT / \
            (2 * self.sensitivity))
        self.pIntended = propIntended / (propIntended + propUnintended)
        self.pUnintended = propUnintended / (propIntended + propUnintended)

        # Songs we have played
        self.songsPlayed = []

        if DEBUG:
            print 'Total songs: ' + str(NUM_SONGS)
            print 'PIntended: ' + str(self.pIntended)

    def writeInputFiles(self):
        '''Creates a database file with high and low weighted songs, where the
        non-intended songs all have weight 0'''
        if DEBUG: print 'Writing input file...'

        f = open(INTENDED_FILE_NAME, 'w')

        intendedSongsCount = 0
        intendedSongs = []
        songLength = len(INTENDED_VERSES)

        # Get all the combinations of intended songs first
        while intendedSongsCount < NUM_INTENDED_SONGS:
            song = songLength * [0]

            for j in range(songLength):
                song[j] = randrange(INTENDED_VERSES[j])

            if song not in intendedSongs:
                intendedSongs.append(song)
                intendedSongsCount += 1
                f.write(str(INTENDED_WEIGHT) + ' ' + str(song) + '\n')

        f.close()
        f = open(UNINTENDED_FILE_NAME, 'w')

        # Randomly generate unintended songs until our space is filled
        for i in range(NUM_UNINTENDED_SONGS):
            song = songLength * [0]

            # Generate the song
            for verseNum in range(songLength):
                # Randomly generate a song space
                verse = randrange(TOTAL_VERSES[verseNum] - \
                    INTENDED_VERSES[verseNum]) + INTENDED_VERSES[verseNum]
                song[verseNum] = verse

            # Write the song to the file
            f.write(str(UNINTENDED_WEIGHT) + ' ' + str(song) + '\n')

        f.close()

        if DEBUG:
            print str(NUM_INTENDED_SONGS) + ' intended songs'
            print str(NUM_UNINTENDED_SONGS) + ' unintended songs'
            print str(NUM_SONGS) + ' total songs'

    def playSong(self):
        '''Plays a song from the database'''
        selector = random()

        # Which song category does the selector fall under?
        if selector <= self.pIntended:
            f = open(INTENDED_FILE_NAME, 'r')
            songs = f.readlines()
            song = songs[randrange(NUM_INTENDED_SONGS)]
            f.close()
        else:
            f = open(UNINTENDED_FILE_NAME, 'r')
            songs = f.readlines()
            song = songs[randrange(NUM_UNINTENDED_SONGS)]
            f.close()

        # Append this song
        with open(PLAYED_FILE_NAME, 'r+') as f:
            old = f.read()
            f.seek(0)
            f.write(old + str(song))
            f.close()

        self.songsPlayed.append(song)
        
        print 'Played: ' + str(song)