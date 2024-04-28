import os
import shutil
import csv
import random

from annotation import get_paths, get_abs_paths


def get_class(path: str, classes: list[str]) -> str:
    """
    Оперделение класса по названию
    :param path: Путь к изображению
    :param classes: Классы изображений
    :return: Класс изображения
    """
    for class_name in classes:
        if class_name in path:
            return class_name
    return ""


def create_dataset_random(old_path: str, new_path: str,
                          classes: list[str]) -> dict[str, str]:
    """
    Создание перемешанного датасета
    :param old_path: Путь к старому датасету
    :param new_path: Путь к новому датасету
    :param classes: Классы изображений
    :return: Список путей к изображениям и их классов
    """
    new_names = [f'{num}.jpg' for num in random.sample(range(10001), 2000)]
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    paths = get_paths(old_path)
    classes_dict = {}
    for new_name, old_name in zip(new_names, paths):
        shutil.copyfile(old_name, os.path.join(new_path, new_name))
        classes_dict[new_name] = get_class(old_name, classes)
    return classes_dict


def create_random_annotation(dataset_dir: str, classes_dict: dict[str, str], save_path: str):
    """
    Создание аннотации к перемешанному датасету
    :param dataset_dir: Папка датасета
    :param classes_dict: Список путей к изображениям и их классов
    :param save_path: Путь к аннотации
    :return:
    """
    if os.path.exists(save_path):
        os.remove(save_path)
    paths = get_paths(dataset_dir)
    abs_paths = get_abs_paths(dataset_dir)
    names = os.listdir(dataset_dir)
    with open(save_path, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t', lineterminator='\n')
        for name, path, abs_path in zip(names, paths, abs_paths):
            writer.writerow([abs_path, path, classes_dict[name]])


if __name__ == "__main__":
    cls_dict = create_dataset_random("dataset_copy", "dataset_random", ["cat", "dog"])
    create_random_annotation("dataset_random", cls_dict, "annotation_random.csv")

