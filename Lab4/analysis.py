import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_dataframe(path: str) -> pd.DataFrame:
    """
    Получение датафрейма
    :param path: Путь к аннотации
    :return:
    """
    return pd.read_csv(path, delimiter='\t', usecols=(0, 2), names=('AbsPath', 'Name'))


def add_mark_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки с метками
    """
    names = df['Name'].unique()
    new_df = df.copy()
    new_df["Mark"] = new_df["Name"].apply(lambda x: 0 if x == names[0] else 1)
    return new_df


def add_size_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонок с высотой, шириной и грубиной изображений
    """
    new_df = df.copy()
    new_df["Height"] = new_df["AbsPath"].apply(lambda path: plt.imread(path).shape[0])
    new_df["Width"] = new_df["AbsPath"].apply(lambda path: plt.imread(path).shape[1])
    new_df["Channels"] = new_df["AbsPath"].apply(lambda path: plt.imread(path).shape[2])
    return new_df


def statistic(df: pd.DataFrame):
    """
    Получение статистики
    """
    for col in ['Height', 'Width', 'Channels']:
        print(df[df['Mark'] == 0][col].describe(), '\n')
        print(df[df['Mark'] == 1][col].describe(), '\n')


def filter_by_class(df: pd.DataFrame, class_mark: int):
    """
    Фильтр по классу
    :param df: Датафрейм
    :param class_mark: Метка класса
    :return:
    """
    return df[df['Mark'] == class_mark]


def filter_by_size(df: pd.DataFrame, class_mark: int, max_height: int, max_width: int):
    """
    Фильтр по размеру изображения
    :param df: Датафрейм
    :param class_mark: Метка класса
    :param max_height: Максимальная высота изображения
    :param max_width: Максимальная ширина изображения
    :return:
    """
    return df[(df['Mark'] == class_mark) & (df['Height'] <= max_height) & (df['Width'] <= max_width)]


def add_pixels_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки с количеством пикселей
    """
    new_df = df.copy()
    new_df['Pixels'] = df['Height'] * df['Width'] * df['Channels']
    return new_df


def df_group(df: pd.DataFrame):
    """
    Статистика по количеству пикселей
    """
    for class_name, sub_df in df.groupby("Name"):
        print(f'Name: {class_name}')
        print(f'Max: {sub_df.Pixels.max()}')
        print(f'Min: {sub_df.Pixels.min()}')
        print(f'Mean: {sub_df.Pixels.mean()}')
        print()


def create_histogram(df: pd.DataFrame, class_mark: int) -> list[np.ndarray]:
    """
    Создание гистограммы
    :param df: Датафрейм
    :param class_mark: Метка класса
    :return: Список гистограмм по трём каналам изображения
    """
    new_df = filter_by_class(df, class_mark)
    img = cv2.imread(new_df.iloc[random.randint(0, len(new_df) - 1)]['AbsPath'])
    return [cv2.calcHist([img], [i], None, [256], [0, 256]) for i in range(3)]


def histogram(df: pd.DataFrame, class_mark: int):
    """
    Отображение гистограммы
    :param df: Датафрейм
    :param class_mark: Метка класса
    :return:
    """
    hist = create_histogram(df, class_mark)
    plt.plot(hist[0], color='b')
    plt.plot(hist[1], color='g')
    plt.plot(hist[2], color='r')
    plt.xlabel("Intensity")
    plt.ylabel("Pixels")
    plt.show()


if __name__ == '__main__':
    df = get_dataframe('annotation.csv')
    print(df.tail(5))
    df = add_mark_col(df)
    print(df.head(5))
    df = add_size_col(df)
    print(df.head(5))
    statistic(df)
    print(filter_by_class(df, 1))
    print(filter_by_size(df, 0, 300, 300))
    df = add_pixels_col(df)
    df_group(df)
    histogram(df, 0)
