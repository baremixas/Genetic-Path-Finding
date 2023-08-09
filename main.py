import sys

from visualisation import visualise, plotBest


if __name__ == "__main__":
    if len(sys.argv) == 1: populationNumber, populationSize, maxChromosomeLength = 1500, 150, 75
    elif len(sys.argv) == 2: populationNumber, populationSize, maxChromosomeLength = int(sys.argv[1]), 150, 75
    elif len(sys.argv) == 3: populationNumber, populationSize, maxChromosomeLength = int(sys.argv[1]), int(sys.argv[2]), 75
    else: populationNumber, populationSize, maxChromosomeLength = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

    best = visualise(populationNumber, populationSize, maxChromosomeLength)
