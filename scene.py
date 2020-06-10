from space import Space

from copy import copy
from typing import NoReturn
import numpy as np
import pygame


class Scene:
    """Класс, описывающий визуализацию имитационной модели."""
    winSize = 800, 800
    isRun = False

    def __init__(self, space: Space):
        """
        :param space: экземпляр области пространства
        """
        self.space = copy(space)
        # Для окна
        self.win = None
        self.bgColor = 255, 255, 255

    def run(self) -> NoReturn:
        """Основная PyGame-функция - запускает цикл обраьботки сообщений. Отвечает за отрисовку объектов."""
        self.__initWindow()

        self.isRun = True
        while self.isRun:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    self.isRun = False

            self.win.fill(self.bgColor)
            pygame.display.update()

        pygame.quit()

    def __initWindow(self) -> NoReturn:
        pygame.init()
        self.win = pygame.display.set_mode(self.winSize)
        pygame.display.set_caption("City Plan")


# Проверка
if __name__ == '__main__':
    relief = 3 * np.random.sample((10, 10))
    width, height, length = 1000, 500, 1200
    space = Space(relief, (width, height, length))
    scene = Scene(space)

    print(repr(scene.space))

    scene.run()
