import csv
import logging
import os


def get_paths(data_dir: str) -> list[str]:
    """
    Создание списка относительных путей
    :param data_dir: Путь к папке с изображениями
    :return: Список относительных путей к изображениям
    """
    paths = []
    for name in os.listdir(data_dir):
        paths.append(os.path.join(data_dir, name))
    return paths


def get_abs_paths(data_dir: str) -> list[str]:
    """
    Создание списка абсолютных путей
    :param data_dir: Путь к папке с изображениями
    :return: Список абсолютных путей к изображениям
    """
    class_path = os.path.abspath(data_dir)
    paths = []
    for name in os.listdir(class_path):
        paths.append(os.path.join(class_path, name))
    return paths


def create_annotation(dataset_dir: str, classes: list[str], save_path: str):
    """
    Создание аннотации к датасету
    :param dataset_dir: Папка датасета
    :param classes: Классы изображений
    :param save_path: Путь к аннотации
    :return:
    """
    try:
        logging.info("Start of annotation creation")
        if os.path.exists(save_path):
            os.remove(save_path)
        for class_name in classes:
            logging.info(f"Handled class: {class_name}")
            paths = get_paths(os.path.join(dataset_dir, class_name))
            abs_paths = get_abs_paths(os.path.join(dataset_dir, class_name))
            with open(save_path, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter='\t', lineterminator='\n')
                for path, abs_path in zip(paths, abs_paths):
                    writer.writerow([abs_path, path, class_name])
        logging.info("Annotation creation is completed")
    except Exception as exc:
        logging.error(f"Error: {exc}")
