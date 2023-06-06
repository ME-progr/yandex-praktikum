"""Модуль содержит различные утилиты для построения графиков тестов хранилищ."""
from typing import Iterable

import matplotlib.pyplot as plt


def create_test_plot(file_path: str, x: Iterable, y: Iterable, title: str = 'График'):
    """
    Функция создает графики для тестов по заданному пути.

    Args:
        file_path: путь до файла
        x: последовательность, которая должна отображаться по оси координат X
        y: последовательность, которая должна отображаться по оси координат Y
        title: наименование графика.
    """
    plt.clf()
    plt.plot(x, y)
    plt.ylabel('Время выполнения операции')
    plt.xlabel('Операция')
    plt.title(title)
    plt.savefig(file_path)
