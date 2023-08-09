from sys import displayhook
import pygame
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

from genetic import initializePopulation, mainLoop
from constants import SCREEN_RESOLUTION, DISPLAY_RESOLUTION
from utilities import Obstacle, Angles


def visualise(populationNumber, populationSize, maxChromosomeLength):
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    font = pygame.font.SysFont('Comic Sans MS', 20)

    pygame.display.set_caption('Path Finding')

    startPosition = [150, 500]
    goalPosition = [600, 200]

    populationCount = -1

    population = []
    fitness = []
    estimatedPosition = []

    obstacles = []

    #Saving for plotting
    best = []

    run = True

    while (run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if (populationCount == -1):
                        populationCount = 0
                    else:
                        populationCount = -1
                        best = []
                
                if event.key == pygame.K_RETURN:
                    plotBest(best, populationNumber)

            if (populationCount == -1):
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    beginObstacle = pygame.mouse.get_pos()
                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    endObstacle = pygame.mouse.get_pos()
                    size = (abs(endObstacle[0] - beginObstacle[0]), abs(endObstacle[1] - beginObstacle[1]))

                    if (beginObstacle[0] >= endObstacle[0] and beginObstacle[1] >= endObstacle[1]):
                        obstacles.append(Obstacle(endObstacle, size))
                    if (beginObstacle[0] >= endObstacle[0] and beginObstacle[1] < endObstacle[1]):
                        obstacles.append(Obstacle((endObstacle[0], beginObstacle[1]), size))
                    if (beginObstacle[0] < endObstacle[0] and beginObstacle[1] >= endObstacle[1]):
                        obstacles.append(Obstacle((beginObstacle[0], endObstacle[1]), size))
                    if (beginObstacle[0] < endObstacle[0] and beginObstacle[1] < endObstacle[1]):
                        obstacles.append(Obstacle(beginObstacle, size))

                if (event.type == pygame.MOUSEBUTTONUP and event.button == 3):
                    clickPoint = pygame.mouse.get_pos()

                    for obstacle in obstacles[::-1]:
                        if obstacle.rect.collidepoint(clickPoint):
                            obstacles.remove(obstacle)
                            break

        #Drawing obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, 'Yellow', obstacle.rect)

        if (populationCount == 0):
            population, fitness, estimatedPosition = initializePopulation(SCREEN_RESOLUTION, populationSize, maxChromosomeLength, startPosition, goalPosition, obstacles)
            populationCount += 1

            #Drawing path
            for i, point in enumerate(estimatedPosition[0]):
                if (i + 1 < len(estimatedPosition[0])):
                    pygame.draw.line(screen, 'White', point, estimatedPosition[0][i+1])
                    pygame.draw.rect(screen, 'White', pygame.Rect(point[0] - 2, point[1] - 2, 4, 4))

        elif (populationCount > 0 and populationCount < populationNumber):
            population, fitness, estimatedPosition = mainLoop(population, fitness, estimatedPosition, startPosition, goalPosition, obstacles, SCREEN_RESOLUTION, maxChromosomeLength, populationCount)
            populationCount += 1

            #Saving for plotting
            best.append(fitness[0:5])

            #Drawing path
            for i, point in enumerate(estimatedPosition[0]):
                if (i + 1 < len(estimatedPosition[0])):
                    pygame.draw.line(screen, 'White', point, estimatedPosition[0][i+1])
                    pygame.draw.rect(screen, 'White', pygame.Rect(point[0] - 2, point[1] - 2, 4, 4))

        #Drawing text
        generation_text = "Generation " + str(populationCount + 1)
        generation_text_surface = font.render(generation_text, False, 'White')
        screen.blit(generation_text_surface, (745,40))

        #Drawing start and goal
        pygame.draw.rect(screen, 'Green', pygame.Rect(startPosition[0] - 4, startPosition[1] - 4, 8, 8))
        pygame.draw.rect(screen, 'Red', pygame.Rect(goalPosition[0] - 4, goalPosition[1] - 4, 8, 8))

        if (populationCount < populationNumber):
            pygame.display.update()

        screen.fill('Black')
    
    pygame.quit()

    return best


def plotBest(bestIndividuals, populationNumber):
    bestFitness = [[],[],[],[],[]]
    bestDistance = [[],[],[],[],[]]

    for generation in bestIndividuals:
        for j, element in enumerate(generation):
            bestFitness[j].append(element[0])
            bestDistance[j].append(element[1])

    size = 2
    plotSize = len(bestFitness[0]) + 1

    plt.figure()

    plt.subplot(121)
    plt.scatter(list(range(1,plotSize)), bestFitness[0], s=size)
    plt.scatter(list(range(1,plotSize)), bestFitness[1], s=size)
    plt.scatter(list(range(1,plotSize)), bestFitness[2], s=size)
    plt.scatter(list(range(1,plotSize)), bestFitness[3], s=size)
    plt.scatter(list(range(1,plotSize)), bestFitness[4], s=size)
    plt.legend(["#1", "#2", "#3", "#4", "#5"])
    plt.xlabel("Population number")
    plt.ylabel("Fitness value")
    if (plotSize >= populationNumber): plt.xticks(np.arange(0, populationNumber + 1, 300))

    plt.subplot(122)
    plt.scatter(list(range(1,plotSize)), bestDistance[0], s=size)
    plt.scatter(list(range(1,plotSize)), bestDistance[1], s=size)
    plt.scatter(list(range(1,plotSize)), bestDistance[2], s=size)
    plt.scatter(list(range(1,plotSize)), bestDistance[3], s=size)
    plt.scatter(list(range(1,plotSize)), bestDistance[4], s=size)
    plt.legend(["#1", "#2", "#3", "#4", "#5"])
    plt.xlabel("Population number")
    plt.ylabel("Distance to goal")
    if (plotSize >= populationNumber): plt.xticks(np.arange(0, populationNumber + 1, 300))

    plt.show()


if __name__ == "__main__":
    pass
    