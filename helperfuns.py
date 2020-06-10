from numpy import array, ndarray
from typing import Union


def meshgridMatrix(mat: Union[list, tuple, ndarray]) -> ndarray:
    """
    На основании переданной прямоугольной матрицы создает новую матрицу в том виде, как если бы она была получена
    в результате вызова функции mat = f(x, y), где x, y - результат numpy.meshgrid(...).
    :param mat: прямоугольная матрица
    :return: матрица, удовлетворяющая индексации от numpy.meshgrid
    """
    res = []
    for x in mat.transpose():   # Необходимо транспонировать из-за особенности работы numpy.meshgrid
        res.append(x.copy())
    return array(res)
