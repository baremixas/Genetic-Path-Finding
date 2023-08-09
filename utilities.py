import pygame
from enum import Enum


class Angles(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Gene:
    def __init__(self, _direction: Angles, _distance: int) -> None:
        self.direction = _direction
        self.distance = _distance


class Obstacle:
    def __init__(self, _position: tuple, _size: tuple) -> None:
        self.position = _position
        self.size = _size

        self.rect = pygame.Rect(self.position, self.size)


def ConvertToGrid(rows: int, columns: int, resolution: tuple) -> list:
    width = resolution[0] / columns
    height = resolution[1] / rows

    grid = []

    for i in range(rows):
        grid.append([])

        for j in range(columns):
            grid[i].append((j * width, i * height))

    return grid, width, height


if __name__ == "__main__":
    pass
    