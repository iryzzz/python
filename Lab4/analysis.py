from argparse import ArgumentParser
import logging
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_dataframe(path: str) -> pd.DataFrame:
    """
    Получение датафрейма
    :param path: Путь к аннотации
    :return: Считанный датафрейм
    """
    try:
        return pd.read_csv(path, delimiter='\t', usecols=(0, 2), names=('AbsPath', 'Name'))
    except Exception as exc:
        logging.error(exc)


def add_mark_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки с метками
    :param df: Датафрейм без колонки с метками
    :return: Датафрейм с добавленной колонкой с метками
    """
    try:
        names = df['Name'].unique()
        new_df = df.copy()
        new_df["Mark"] = new_df["Name"].apply(lambda x: 0 if x == names[0] else 1)
        return new_df
    except Exception as exc:
        logging.error(exc)


def add_size_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонок с высотой, шириной и грубиной изображений
    :param df: Датафрейм
    :return: Датафрейм с добавленными колонками с высотой, шириной и грубиной изображений
    """
    try:
        new_df = df.copy()
        new_df["Height"] = new_df["AbsPath"].apply(lambda path: plt.imread(path).shape[0])
        new_df["Width"] = new_df["AbsPath"].apply(lambda path: plt.imread(path).shape[1])
        new_df["Channels"] = new_df["AbsPath"].apply(lambda path: plt.imread(path).shape[2])
        return new_df
    except Exception as exc:
        logging.error(exc)


def statistic(df: pd.DataFrame) -> None:
    """
    Получение статистики
    :param df: Датафрейм с колонками 'Height', 'Width', 'Channels' и 'Mark'
    :return:
    """
    try:
        for col in ['Height', 'Width', 'Channels']:
            print(df[df['Mark'] == 0][col].describe(), '\n')
            print(df[df['Mark'] == 1][col].describe(), '\n')
    except Exception as exc:
        logging.error(exc)


def filter_by_class(df: pd.DataFrame, class_mark: int) -> pd.DataFrame:
    """
    Фильтр по классу
    :param df: Датафрейм
    :param class_mark: Метка класса
    :return: Отфильтрованный датафрейм
    """
    try:
        return df[df['Mark'] == class_mark]
    except Exception as exc:
        logging.error(exc)


def filter_by_size(df: pd.DataFrame, class_mark: int, max_height: int,
                   max_width: int) -> pd.DataFrame:
    """
    Фильтр по размеру изображения
    :param df: Датафрейм
    :param class_mark: Метка класса
    :param max_height: Максимальная высота изображения
    :param max_width: Максимальная ширина изображения
    :return: Отфильтрованный датафрейм
    """
    try:
        return df[(df['Mark'] == class_mark) & (df['Height'] <= max_height) & (df['Width'] <= max_width)]
    except Exception as exc:
        logging.error(exc)


def add_pixels_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавление колонки с количеством пикселей
    :param df: Датафрейм
    :return: Датафрейм с добавленной колонкой с количеством пикселей
    """
    try:
        new_df = df.copy()
        new_df['Pixels'] = df['Height'] * df['Width'] * df['Channels']
        return new_df
    except Exception as exc:
        logging.error(exc)


def df_group(df: pd.DataFrame) -> None:
    """
    Статистика по количеству пикселей
    :param df: Датафрейм
    :return:
    """
    try:
        for class_name, sub_df in df.groupby("Name"):
            print(f'Name: {class_name}')
            print(f'Max: {sub_df.Pixels.max()}')
            print(f'Min: {sub_df.Pixels.min()}')
            print(f'Mean: {sub_df.Pixels.mean()}')
            print()
    except Exception as exc:
        logging.error(exc)


def create_histogram(df: pd.DataFrame, class_mark: int) -> list[np.ndarray]:
    """
    Создание гистограммы
    :param df: Датафрейм
    :param class_mark: Метка класса
    :return: Список гистограмм по трём каналам изображения
    """
    try:
        new_df = filter_by_class(df, class_mark)
        img = cv2.imread(new_df.iloc[random.randint(0, len(new_df) - 1)]['AbsPath'])
        return [cv2.calcHist([img], [i], None, [256], [0, 256]) for i in range(3)]
    except Exception as exc:
        logging.error(exc)


def histogram(df: pd.DataFrame, class_mark: int) -> None:
    """
    Отображение гистограммы
    :param df: Датафрейм
    :param class_mark: Метка класса
    :return:
    """
    try:
        hist = create_histogram(df, class_mark)
        plt.plot(hist[0], color='b')
        plt.plot(hist[1], color='g')
        plt.plot(hist[2], color='r')
        plt.xlabel("Intensity")
        plt.ylabel("Pixels")
        plt.show()
    except Exception as exc:
        logging.error(exc)


if __name__ == '__main__':
    logging.basicConfig(filename='lab4.log', level=logging.INFO)

    parser = ArgumentParser()
    parser.add_argument('annotation', type=str, help='Path to annotation')
    parser.add_argument('-c', '--class_index', type=int, help='Class index of image', required=True)
    parser.add_argument('-he', '--height', type=int, help='Height of image', required=True)
    parser.add_argument('-w', '--width', type=int, help='Width of image', required=True)
    args = parser.parse_args()

    try:
        df = get_dataframe(args.annotation)
        print(df.tail())
        df = add_mark_col(df)
        print(df.head())
        df = add_size_col(df)
        print(df.head())
        statistic(df)
        print(filter_by_class(df, args.class_index))
        print(filter_by_size(df, args.class_index, args.height, args.width))
        df = add_pixels_col(df)
        df_group(df)
        histogram(df, args.class_index)
    except Exception as exc:
        logging.error(exc)
