from model1 import DPMusic

NUM_TRIALS = 15

def main():
    testclass = DPMusic()
    #testclass.writeInputFiles()

    for i in range(NUM_TRIALS):
        testclass.playSong()

if __name__ == '__main__':
    main()