from operator import mul
from random import randrange


# Parameters and debug
DEBUG = 1
INPUT_FILE_NAME = 'inputs'

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

# How much each intended verse is worth, a song can have a max weight of the
# number of verses * WEIGHT_BONUS
WEIGHT_BONUS = 0.1

# Differential privacy parameter
EPSILON = 1.0

class DPMusic:
    '''Differentially private song generation, using strings for music.'''

    def __init__(self):
        '''Initializes member variables.'''
        if DEBUG:
            print
            print 'Initializing'
            print

        self.numPossibleHighlyWeightedSongs = reduce(mul, INTENDED_VERSES, 1)

        if DEBUG:
            print 'Total songs: ' + str(NUM_SONGS)
            print

    def writeInputFile1(self):
        '''Creates a database file with high and low weighted songs, where the
        non-intended songs all have weight 0'''
        if DEBUG:
            print 'Writing input file...'
            print

        f = open(INPUT_FILE_NAME, 'w')

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
                f.write(str(WEIGHT_BONUS * songLength) + ' ' + str(song) + '\n')

        for i in range(NUM_SONGS - NUM_INTENDED_SONGS):
            song = songLength * [0]

            # Generate the song and its weight
            weight = 0
            for verseNum in range(songLength):
                # Randomly generate a song space
                verse = randrange(TOTAL_VERSES[verseNum] - \
                    INTENDED_VERSES[verseNum]) + INTENDED_VERSES[verseNum]
                song[verseNum] = verse

                # If the this verse is intended, raise its weight
                if verse <= INTENDED_VERSES[verseNum]:
                    weight += WEIGHT_BONUS

            # Write the song to the file
            f.write(str(weight) + ' ' + str(song) + '\n')

        f.close()

        if DEBUG:
            print str(NUM_INTENDED_SONGS) + ' intended songs'
            print str(NUM_SONGS - NUM_INTENDED_SONGS) + ' unintended songs'
            print str(NUM_SONGS) + ' total songs'

    def writeInputFile2(self):
        '''Creates a database file with high and low weighted songs'''
        if DEBUG:
            print 'Writing input file...'
            print

        f = open(INPUT_FILE_NAME, 'w')

        songLength = len(INTENDED_VERSES)

        numNonZeroWeight = 0
        numHighWeight = 0

        for i in range(NUM_SONGS):
            song = songLength * [0]

            # Generate the song and its weight
            weight = 0
            for verseNum in range(songLength):
                # Randomly generate a song space
                verse = randrange(TOTAL_VERSES[verseNum])
                song[verseNum] = verse

                # If the this verse is intended, raise its weight
                if verse <= INTENDED_VERSES[verseNum]:
                    weight += WEIGHT_BONUS

            # Write the song to the file
            f.write(str(weight) + ' ' + str(song) + '\n')

            if weight > 0.1:
                numHighWeight += 1
                numNonZeroWeight += 1

            elif weight > 0.0:
                numNonZeroWeight += 1

        f.close()

        if DEBUG:
            print str(numNonZeroWeight) + ' songs with weight > 0.0'
            print str(numHighWeight) + ' songs with weight > 0.1'


if __name__ == '__main__':
    testclass = DPMusic()
    testclass.writeInputFile()