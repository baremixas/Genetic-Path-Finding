from copy import deepcopy
import numpy as np
import operator

from utilities import Gene, Obstacle, Angles
from constants import SCREEN_RESOLUTION


def initializePopulation(screenRes: tuple, populationSize: int, maxChromosomeLength: int, startPos: list, goalPos: list, obstacles: list):
    population = []
    fitness = []
    estimatedPosition = []

    for i in range(populationSize):
        population.append([])
        estimatedPosition.append([startPos])

        #Checking whether it's possible to finish path with only 2 points
        if (startPos[0] == goalPos[0] and startPos[1] == goalPos[1]):
            return []
        elif (startPos[0] == goalPos[0] or startPos[1] == goalPos[1]):
            length = np.random.randint(4, maxChromosomeLength)
        else:
            length = np.random.randint(5, maxChromosomeLength)

        cost = 0
        tempPosition = deepcopy(startPos)

        while (len(population[i]) + 2 < length):
            angle = np.random.choice(Angles)

            match angle:
                case Angles.UP:
                    maxDistance = tempPosition[1]
                    distance = np.random.randint(maxDistance)
                    tempPosition[1] -= distance
                case Angles.DOWN:
                    maxDistance = screenRes[1] - tempPosition[1]
                    distance = np.random.randint(maxDistance)
                    tempPosition[1] += distance
                case Angles.RIGHT:
                    maxDistance = screenRes[0] - tempPosition[0]
                    distance = np.random.randint(maxDistance)
                    tempPosition[0] += distance
                case Angles.LEFT:
                    maxDistance = tempPosition[0]
                    distance = np.random.randint(maxDistance)
                    tempPosition[0] -= distance
                case _: pass

            if (not tempPosition == estimatedPosition[i][-1]):
                if (CheckForObstacles(obstacles, estimatedPosition[i], tempPosition, angle)):
                    population[i].append(Gene(angle, distance))
                    estimatedPosition[i].append(deepcopy(tempPosition))
                else: tempPosition = deepcopy(estimatedPosition[i][-1])
        
        fitness.append(calculateFitness(population[i], estimatedPosition[i], goalPos, obstacles))

    return population, fitness, estimatedPosition


def CheckForObstacles(obstacles: list, chromosome: list, tempPoint: list, direction: Angles) -> bool:
    for obstacle in obstacles:
        #Checking if point is in obstacle
        if (obstacle.rect.collidepoint(tempPoint)): return False

        #Checking if there is an obstacle between points
        match direction:
            case Angles.UP:
                if ((obstacle.position[0] <= tempPoint[0] and obstacle.position[0] + obstacle.size[0] >= tempPoint[0]) and 
                (obstacle.position[1] >= tempPoint[1] and obstacle.position[1] + obstacle.size[1] <= chromosome[-1][1])): return False
            case Angles.DOWN:
                if ((obstacle.position[0] <= tempPoint[0] and obstacle.position[0] + obstacle.size[0] >= tempPoint[0]) and 
                (obstacle.position[1] >= chromosome[-1][1] and obstacle.position[1] + obstacle.size[1] <= tempPoint[1])): return False
            case Angles.LEFT:
                if ((obstacle.position[1] <= tempPoint[0] and obstacle.position[1] + obstacle.size[1] >= tempPoint[1]) and 
                (obstacle.position[0] >= tempPoint[0] and obstacle.position[0] + obstacle.size[0] <= chromosome[-1][0])): return False
            case Angles.RIGHT:
                if ((obstacle.position[1] <= tempPoint[0] and obstacle.position[1] + obstacle.size[1] >= tempPoint[1]) and 
                (obstacle.position[0] >= chromosome[-1][0] and obstacle.position[0] + obstacle.size[0] <= tempPoint[0])): return False

    return True


def CheckBetweenPoints(point1: list, point2: list, obstacles: list) -> bool:
    penalty = 0
    safeDistance = 20

    if (point1[0] < 0 or point1[0] > SCREEN_RESOLUTION[0] or point1[1] < 0 or point1[1] > SCREEN_RESOLUTION[1]):
        penalty += 0.6
    if (point2[0] < 0 or point2[0] > SCREEN_RESOLUTION[0] or point2[1] < 0 or point2[1] > SCREEN_RESOLUTION[1]):
        penalty += 0.6

    for obstacle in obstacles:
        if (obstacle.rect.collidepoint(point1) or obstacle.rect.collidepoint(point2)): penalty += 1

        if(point1 == point2):
            print(point1, point2)
        if (point1[0] == point2[0]):
            if (point1[1] > point2[1]): angle = Angles.UP
            if (point1[1] < point2[1]): angle = Angles.DOWN
        elif (point1[1] == point2[1]):
            if (point1[0] > point2[0]): angle = Angles.LEFT
            if (point1[0] < point2[0]): angle = Angles.RIGHT

        if (angle == Angles.UP):
            if (obstacle.position[1] + obstacle.size[1] >= point2[1] and obstacle.position[1] <= point1[1]):
                if (point1[0] >= obstacle.position[0] and point1[0] <= obstacle.position[0] + obstacle.size[0]): penalty += 1
        elif (angle == Angles.DOWN):
            if (obstacle.position[1] + obstacle.size[1] >= point1[1] and obstacle.position[1] <= point2[1]):
                if (point1[0] >= obstacle.position[0] and point1[0] <= obstacle.position[0] + obstacle.size[0]): penalty += 1
        elif (angle == Angles.LEFT):
            if (obstacle.position[0] + obstacle.size[0] >= point2[0] and obstacle.position[0] <= point1[0]):
                if (point1[1] >= obstacle.position[1] and point1[1] <= obstacle.position[1] + obstacle.size[1]): penalty += 1
        elif (angle == Angles.RIGHT):
            if (obstacle.position[0] + obstacle.size[0] >= point1[0] and obstacle.position[0] <= point2[0]):
                if (point1[1] >= obstacle.position[1] and point1[1] <= obstacle.position[1] + obstacle.size[1]): penalty += 1

        distance = safeDistance

        match angle:
            case Angles.UP:
                if (obstacle.position[1] + obstacle.size[1] >= point2[1] and obstacle.position[1] <= point1[1]):
                    if (obstacle.position[0] - point1[0] < safeDistance and obstacle.position[0] - point1[0] > 0):
                        distance = obstacle.position[0] - point1[0]
                    elif (point1[0] - (obstacle.position[0] + obstacle.size[0]) < safeDistance and point1[0] - (obstacle.position[0] + obstacle.size[0]) > 0):
                        distance = point1[0] - (obstacle.position[0] + obstacle.size[0])
            case Angles.DOWN:
                if (obstacle.position[1] + obstacle.size[1] >= point1[1] and obstacle.position[1] <= point2[1]):
                    if (obstacle.position[0] - point1[0] < safeDistance and obstacle.position[0] - point1[0] > 0):
                        distance = obstacle.position[0] - point1[0]
                    elif (point1[0] - (obstacle.position[0] + obstacle.size[0]) < safeDistance and point1[0] - (obstacle.position[0] + obstacle.size[0]) > 0):
                        distance = point1[0] - (obstacle.position[0] + obstacle.size[0])
            case Angles.LEFT:
                if (obstacle.position[0] + obstacle.size[0] >= point2[0] and obstacle.position[0] <= point1[0]):
                    if (obstacle.position[1] - point1[1] < safeDistance and obstacle.position[1] - point1[1] > 0):
                        distance = obstacle.position[1] - point1[1]
                    elif (point1[1] - (obstacle.position[1] + obstacle.size[1]) < safeDistance and point1[1] - (obstacle.position[1] + obstacle.size[1]) > 0):
                        distance = point1[1] - (obstacle.position[1] + obstacle.size[1])
            case Angles.RIGHT:
                if (obstacle.position[0] + obstacle.size[0] >= point1[0] and obstacle.position[0] <= point2[0]):
                    if (obstacle.position[1] - point1[1] < safeDistance and obstacle.position[1] - point1[1] > 0):
                        distance = obstacle.position[1] - point1[1]
                    elif (point1[1] - (obstacle.position[1] + obstacle.size[1]) < safeDistance and point1[1] - (obstacle.position[1] + obstacle.size[1]) > 0):
                        distance = point1[1] - (obstacle.position[1] + obstacle.size[1])
        
        penalty += (safeDistance - distance) / safeDistance

    return penalty

# def CheckObstaclesBetweenPoints(point1: list, point2: list, obstacles: list) -> bool:
#     for obstacle in obstacles:
#         if (obstacle.rect.collidepoint(point1) or obstacle.rect.collidepoint(point2)): return False

#         if(point1 == point2):
#             print(point1, point2)
#         if (point1[0] == point2[0]):
#             if (point1[1] > point2[1]): angle = Angles.UP
#             if (point1[1] < point2[1]): angle = Angles.DOWN
#         elif (point1[1] == point2[1]):
#             if (point1[0] > point2[0]): angle = Angles.LEFT
#             if (point1[0] < point2[0]): angle = Angles.RIGHT

#         if (angle == Angles.UP):
#             if (obstacle.position[1] + obstacle.size[1] >= point2[1] and obstacle.position[1] <= point1[1]):
#                 if (point1[0] >= obstacle.position[0] and point1[0] <= obstacle.position[0] + obstacle.size[0]): return False
#         elif (angle == Angles.DOWN):
#             if (obstacle.position[1] + obstacle.size[1] >= point1[1] and obstacle.position[1] <= point2[1]):
#                 if (point1[0] >= obstacle.position[0] and point1[0] <= obstacle.position[0] + obstacle.size[0]): return False
#         elif (angle == Angles.LEFT):
#             if (obstacle.position[0] + obstacle.size[0] >= point2[0] and obstacle.position[0] <= point1[0]):
#                 if (point1[1] >= obstacle.position[1] and point1[1] <= obstacle.position[1] + obstacle.size[1]): return False
#         elif (angle == Angles.RIGHT):
#             if (obstacle.position[0] + obstacle.size[0] >= point1[0] and obstacle.position[0] <= point2[0]):
#                 if (point1[1] >= obstacle.position[1] and point1[1] <= obstacle.position[1] + obstacle.size[1]): return False

#     return True


def calculateFitness(chromosome: list, estimatedPosition: list, goalPosition: list, obstacles: list) -> list:
    distance = 0
    for i in range(len(chromosome)):
        distance += chromosome[i].distance
    
    # #Check for obstacle colision
    # penalty = 0
    # for i in range(1, len(estimatedPosition)):
    #     if (not CheckObstaclesBetweenPoints(estimatedPosition[i - 1], estimatedPosition[i], obstacles)):
    #         penalty += 2000
    
    #Check for obstacle colision
    penalty = 0
    for i in range(1, len(estimatedPosition)):
        penalty += CheckBetweenPoints(estimatedPosition[i - 1], estimatedPosition[i], obstacles)

    distanceToGoal = 0
    distanceToGoal = np.sqrt(np.power(estimatedPosition[-1][0] - goalPosition[0], 2) + np.power(estimatedPosition[-1][1] - goalPosition[1], 2))

    reachedGoal = 0
    if (abs(estimatedPosition[-1][0] - goalPosition[0]) <= 4 and abs(estimatedPosition[-1][1] - goalPosition[1]) <= 4):
        reachedGoal = -300

    cost = 0.5 * distance + 10 * distanceToGoal + 2500 * penalty + reachedGoal

    return [cost, distanceToGoal]


def rouletteSelection(population: list, fitness: list, amount: int) -> list:
    probability = []
    parentPairs = []

    costSum = 0

    for element in fitness:
        costSum += element[0]

    probability.append(0)

    for element in fitness:
        probability.append(element[0]/costSum + probability[-1])

    while (len(parentPairs) < amount):
        parentNumbers = []

        for _ in range(2):
            rouletteRandomNumber = np.random.random()

            for i in range(1, len(probability)):
                if (rouletteRandomNumber > probability[i-1] and rouletteRandomNumber <= probability[i]):
                    parentNumbers.append(i - 1)
            
        if ((parentNumbers[0] != parentNumbers[1]) and not (parentNumbers in parentPairs)):
            parentPairs.append(parentNumbers)

    return parentPairs


def randomSelection(population: list, amount: int) -> list:
    parentPairs = []

    while (len(parentPairs) < amount):
        randomIndex1 = np.random.randint(len(population))
        randomIndex2 = np.random.randint(len(population))

        if (randomIndex1 != randomIndex2):
            parentPairs.append((randomIndex1, randomIndex2))
    
    return parentPairs


def onePointCrossover(population: list, parentPairs: list) -> list:
    offspring = []

    for parents in parentPairs:
        if (min(len(population[parents[0]]), len(population[parents[1]])) <= 2):
            continue

        randomPoint = np.random.randint(1, min(len(population[parents[0]]), len(population[parents[1]])) - 1)

        offspring1 = population[parents[0]][0 : randomPoint] + population[parents[1]][randomPoint :]
        offspring2 = population[parents[1]][0 : randomPoint] + population[parents[0]][randomPoint :]
        
        offspring.append(deepcopy(offspring1))
        offspring.append(deepcopy(offspring2))

    return offspring


def multiplePointCrossover(population: list, parentPairs: list) -> list:
    offspring = []

    for parents in parentPairs:
        if (min(len(population[parents[0]]), len(population[parents[1]])) <= 2):
            continue

        randomPoint1 = np.random.randint(1, min(len(population[parents[0]]), len(population[parents[1]])) - 1)
        try:
            randomPoint2 = np.random.randint(randomPoint1 + 1, min(len(population[parents[0]]), len(population[parents[1]])) - 1)
        except:
            continue

        offspring1 = population[parents[0]][0 : randomPoint1] + population[parents[0]][randomPoint1 : randomPoint2] + population[parents[1]][randomPoint2 :]
        offspring2 = population[parents[0]][0 : randomPoint1] + population[parents[1]][randomPoint1 : randomPoint2] + population[parents[0]][randomPoint2 :]
        offspring3 = population[parents[0]][0 : randomPoint1] + population[parents[1]][randomPoint1 : randomPoint2] + population[parents[1]][randomPoint2 :]
        offspring4 = population[parents[1]][0 : randomPoint1] + population[parents[0]][randomPoint1 : randomPoint2] + population[parents[0]][randomPoint2 :]
        offspring5 = population[parents[1]][0 : randomPoint1] + population[parents[0]][randomPoint1 : randomPoint2] + population[parents[1]][randomPoint2 :]
        offspring6 = population[parents[1]][0 : randomPoint1] + population[parents[1]][randomPoint1 : randomPoint2] + population[parents[0]][randomPoint2 :]

        offspring += [deepcopy(offspring1), deepcopy(offspring2), deepcopy(offspring3), deepcopy(offspring4), deepcopy(offspring5), deepcopy(offspring6)]

    return offspring


def randomMutation(offspring: list, maxDistance: int, probability: float) -> list:
    for chromosome in offspring:
        if (np.random.random() <= probability):
            randomIndex = np.random.randint(len(chromosome))

            chromosome[randomIndex] = Gene(np.random.choice(Angles), np.random.randint(1, maxDistance))
    
    return offspring


def deletion(offspring: list, probability: float) -> list:
    for chromosome in offspring:
        if (len(chromosome) > 2):
            if (np.random.random() <= probability):
                randomIndex = np.random.randint(len(chromosome))

                chromosome.pop(randomIndex)
    
    return offspring


def insert(offspring: list, maxDistance: int, probability: float) -> list:
    for chromosome in offspring:
        if (np.random.random() <= probability):
            randomIndex = np.random.randint(len(chromosome))

            chromosome.insert(randomIndex, Gene(np.random.choice(Angles), np.random.randint(1, maxDistance)))
    
    return offspring


def calculateOffspringEstimatedAndFitness(offspring: list, startPosition: list, goalPosition: list, obstacles: list):
    offspringEstimatedPosition = []
    offspringFitness = []

    for chromosome in offspring:
        offspringEstimatedPosition.append([startPosition])

        tempPosition = deepcopy(startPosition)

        for gene in chromosome:
            match gene.direction:
                    case Angles.UP:
                        tempPosition[1] -= gene.distance
                    case Angles.DOWN:
                        tempPosition[1] += gene.distance
                    case Angles.RIGHT:
                        tempPosition[0] += gene.distance
                    case Angles.LEFT:
                        tempPosition[0] -= gene.distance
                    case _: pass

            offspringEstimatedPosition[-1].append(deepcopy(tempPosition))
        
        offspringFitness.append(calculateFitness(chromosome, offspringEstimatedPosition[-1], goalPosition, obstacles))
    
    return offspringEstimatedPosition, offspringFitness


def selectPopulation(population: list, populationFitness: list, populationEstimatedPosition: list, offspring: list, offspringFitness: list, offspringEstimatedPosition: list):
    size = len(population)
    
    populationFitness, population, populationEstimatedPosition = (list(t) for t in zip(*sorted(zip(populationFitness, population, populationEstimatedPosition), key=operator.itemgetter(0))))
    offspringFitness, offspring, offspringEstimatedPosition = (list(t) for t in zip(*sorted(zip(offspringFitness, offspring, offspringEstimatedPosition), key=operator.itemgetter(0))))

    newPopulation, newFitness, newEstimatedPosition = [], [], []

    populationCount = 0
    offspringCount = 0

    while (len(newPopulation) < size):
        if (offspringCount < len(offspring)):
            if (populationFitness[populationCount][0] <= offspringFitness[offspringCount][0]):
                newPopulation.append(population[populationCount])
                newFitness.append(populationFitness[populationCount])
                newEstimatedPosition.append(populationEstimatedPosition[populationCount])

                populationCount += 1
            else:
                newPopulation.append(offspring[offspringCount])
                newFitness.append(offspringFitness[offspringCount])
                newEstimatedPosition.append(offspringEstimatedPosition[offspringCount])

                offspringCount += 1
        else:
            newPopulation.append(population[populationCount])
            newFitness.append(populationFitness[populationCount])
            newEstimatedPosition.append(populationEstimatedPosition[populationCount])

            populationCount += 1
    
    return newPopulation, newFitness, newEstimatedPosition


def randomPopulate(amount: int, screenRes: tuple, maxChromosomeLength: int, startPos: list, goalPos: list, obstacles: list):
    newPopulation, newFitness, newEstimatedPosition = initializePopulation(screenRes, amount, maxChromosomeLength, startPos, goalPos, obstacles)

    return newPopulation, newFitness, newEstimatedPosition


def mainLoop(population: list, fitness: list, estimatedPosition: list, startPosition: list, goalPosition: list, obstacles: list, screenRes: tuple, maxChromosomeLength: int, currentGeneration: int):
    if (currentGeneration < 750): parents = rouletteSelection(population, fitness, 50)
    else:
        parents1 = randomSelection(population, 30)
        parents2 = rouletteSelection(population, fitness, 25)
        parents = parents1 + parents2
    offspringAfterCrossover = onePointCrossover(population, parents)
    offspringAfterMutation = randomMutation(offspringAfterCrossover, 450, 0.4)
    offspringAfterDeletion = deletion(offspringAfterMutation, 0.1)
    offspringAfterInsertion = insert(offspringAfterDeletion, 500, 0.1)
    offspringEstimatedPosition, offspringFitness = calculateOffspringEstimatedAndFitness(offspringAfterInsertion, startPosition, goalPosition, obstacles)
    # newPopulation, newFitness, newEstimatedPosition = selectPopulation(populationRandomized, fitnessRandomized, estimatedPositionRandomized, offspringAfterMutation, offspringFitness, offspringEstimatedPosition)
    offspringRandom, fitnessRandom, estimatedPositionRandom = randomPopulate(20, screenRes, maxChromosomeLength, startPosition, goalPosition, obstacles)
    newPopulation, newFitness, newEstimatedPosition = selectPopulation(population, fitness, estimatedPosition, offspringAfterMutation + offspringRandom, offspringFitness + fitnessRandom, offspringEstimatedPosition + estimatedPositionRandom)

    return newPopulation, newFitness, newEstimatedPosition


if __name__ == "__main__":
    pass
    