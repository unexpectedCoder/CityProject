import helperfuns as hp

from scipy.interpolate import interp2d
from typing import Union
import numpy as np


class Space:
    """
    Класс, описывающий пространство в виде пространственного параллелепипеда с учетом рельефа местности.
    """
    acc = 3                                         # Точность вывода
    units = {'km': 1000, 'm': 1, 'mm': 0.001}       # Допустимые единицы измерений (с переводом в метры)
    interp_methods = 'linear', 'cubic', 'nearest'

    def __init__(self, relief: np.ndarray, size: tuple,
                 unit='m', interp_method='linear'):
        """
        :param relief: матрица MxN сетки высот (рельефа) по ширине M и длине N (в относительном измерении)
        :param size: размеры пространственного параллепипеда (ширина x высота x длина)
        :param unit: единица измерения длины
        :param interp_method: метод интерполяции массива высот
        """
        for x in size:
            if x <= 0:
                raise ValueError(f"Ошибка в конструкторе класса '{self.__class__}': "
                                 f"каждый из размеров пространства должен быть > 0!")
        # Инициализация размеров пространства
        self.relief = relief
        self.gridSize = len(relief), len(relief[0])
        self.width, self.height, self.length = size
        # Перевод Длин в единицы СИ
        self.unit = unit if unit in self.units.keys() else 'm'
        if self.unit != 'm':
            self.width *= self.units[unit]
            self.height *= self.units[unit]
            self.length *= self.units[unit]
            self.unit = 'm'
        # Важно для метода copy
        self.interpMethod = interp_method if interp_method in self.interp_methods else self.interp_methods[0]
        # Длина одной ячейки...
        self.cellW = self.width / self.gridSize[0]      # ...по ширине
        self.cellL = self.length / self.gridSize[1]     # ...по длине
        # Функция интерполирования высоты в зависимости от координат
        x, y = self.cellW * np.arange(self.gridSize[0]), self.cellL * np.arange(self.gridSize[1])
        z = hp.meshgridMatrix(self.relief)
        self.interpHeight = interp2d(x, y, z, kind=self.interpMethod)

    def __repr__(self):
        return f"Space ({self.__class__}):" \
               f"\n - size (w x h x l), [{self.unit}]: {self.width}x{self.height}x{self.length}" \
               f"\n - relief's grid size (r x c): {self.gridSize[0]}x{self.gridSize[1]}" \
               f"\n - width cell size, [{self.unit}]: {round(self.cellW, self.acc)}" \
               f"\n - length cell size, [{self.unit}]: {round(self.cellL, self.acc)}"

    def __copy__(self):
        return Space(self.relief, (self.width, self.height, self.length), interp_method=self.interpMethod)

    def getLandHeight(self, xy: Union[list, tuple, np.ndarray]) -> float:
        """
        Функция возвращает интерполированное значение высоты для заданных координат.
        :param xy: координаты (ширина x длина)
        :return: интерполированное значение высоты рельефа
        """
        if len(xy) < 2:
            raise ValueError(f"Ошибка в функции '{self.getLandHeight.__name__}' класса '{self.__class__}': "
                             f"на плоскости необходимо 2 координаты (x и y)!")
        if 0 <= xy[0] <= self.width and 0 <= xy[1] <= self.length:
            return self.interpHeight(xy[0], xy[1])
        raise ValueError(f"Ошибка в функции '{self.getLandHeight.__name__}' класса '{self.__class__}': "
                         f"переданные координаты выходят за пределы пространства!")


# Тестирование
if __name__ != '__main__':
    relief = 3 * np.random.sample((10, 10))
    relief[0, 0] = 5
    relief[1, 0] = 20
    relief[-1, -1] = 10
    width, height, length = 1000, 500, 1200
    space = Space(relief, (width, height, length), unit='km')

    print(repr(space))
    print(hp.meshgridMatrix(space.relief))
