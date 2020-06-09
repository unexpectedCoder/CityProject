import numpy as np


class Space:
    """
    Класс, описывающий пространство в виде пространственного параллелепипеда с учетом рельефа местности.
    """
    acc = 3                             # Точность вывода
    units = {'km': 1000, 'm': 1}        # Допустимые единицы измерений (с переводом в метры)

    def __init__(self, relief: np.ndarray, size: tuple, unit: str = 'm'):
        """
        :param relief: матрица MxN сетки высот (рельефа) по ширине M и длине N (в относительном измерении)
        :param size: размеры пространственного параллепипеда (ширина x высота x длина)
        :param unit: единица измерения длины
        """
        for x in size:
            if x <= 0:
                raise ValueError(f"Ошибка в <{self.__class__}>: каждый из размеров пространства должен быть > 0!")

        self.relief = relief
        self.gridSize = len(relief), len(relief[0])     # TODO: предусмотреть интерполирование карты высот
        self.width, self.height, self.length = size

        self.unit = unit if unit in self.units.keys() else 'm'
        if self.unit != 'm':
            self.width *= self.units[unit]
            self.height *= self.units[unit]
            self.length *= self.units[unit]
            self.unit = 'm'

        self.cellW = self.width / self.gridSize[0]      # Длина одной ячейки по ширине
        self.cellL = self.length / self.gridSize[1]     # и по длине
        # Зная индекс узла сетки, можно восстановить координату в пространстве

    def __repr__(self):
        return f"Space ({self.__class__}):" \
               f"\n - size (w x h x l), [{self.unit}]: {self.width}x{self.height}x{self.length}" \
               f"\n - relief's grid size (r x c): {self.gridSize[0]}x{self.gridSize[1]}" \
               f"\n - width cell size, [{self.unit}]: {round(self.cellW, self.acc)}" \
               f"\n - length cell size, [{self.unit}]: {round(self.cellL, self.acc)}"

    def __copy__(self):
        return Space(self.relief, (self.width, self.height, self.length))

    def getLandHeight(self, xy: tuple):
        pass


# Тестирование
if __name__ != '__main__':
    relief = 3 * np.random.sample((50, 60))
    width, height, length = 1000, 500, 1200
    space = Space(relief, (width, height, length), unit='km')
    print(repr(space))
