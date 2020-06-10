from space import Space

import numpy as np


#######################################################################################################################
relief = 3 * np.random.sample((50, 60))
width, height, length = 1000, 500, 1200
space1 = Space(relief, (width, height, length))
#######################################################################################################################


def test_grid_size():
    # Совпадает ли размер сетки рельефа
    assert space1.gridSize == (50, 60)


def test_size():
    # Правильно ли инициализируется размер пространства
    assert space1.width == 1000 and space1.height == 500 and space1.length == 1200


#######################################################################################################################
space2 = Space(relief, (width * 1e-3, height * 1e-3, length * 1e-3), unit='km')
#######################################################################################################################


def test_size_km():
    # Правильно ли инициализируется размер пространства при инициализации в км
    assert space2.width == 1000. and space2.height == 500. and space2.length == 1200.


def test_init():
    try:
        res1 = False
        Space(relief, (1, 2, 0))    # Нельзя передавать 0...
    except ValueError:
        res1 = True
    try:
        res2 = False
        Space(relief, (1, -2, 3))   # ...или отрицательные значения
    except ValueError:
        res2 = True
    assert res1 and res2


#######################################################################################################################
relief = 3 * np.random.sample((10, 10))
relief[0, 0] = 5.
relief[1, 0] = 20.
relief[-1, -1] = 10.
width, height, length = 1000, 500, 1200
space = Space(relief, (width, height, length))
#######################################################################################################################


def test_interp():
    # Совпадает ли значение в узлах при интерполяции
    res1 = space.getLandHeight((0, 0))
    res2 = space.getLandHeight((width, length))
    assert res1 == relief[0, 0] and res2 == relief[-1, -1]


def test_interp_raise():
    # Вызывается ли исключение при передачи координат вне границ и при передаче неполного массива (len < 2)
    try:
        res1 = False
        space.getLandHeight((-1, 12))
    except ValueError:
        res1 = True
    try:
        res2 = False
        space.getLandHeight([1])
    except ValueError:
        res2 = True
    assert res1 and res2
