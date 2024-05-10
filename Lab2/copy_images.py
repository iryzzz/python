import csv
import logging
import os
import shutil

from annotation import get_paths, get_abs_paths


def create_dataset_copy(old_path: str, new_path: str, classes: list[str]):
    """
    Создание копии датасета
    :param old_path: Путь к старому датасеты
    :param new_path: Путь к новому датасету
    :param classes: Классы изображений
    :return:
    """
    try:
        logging.info("Start copying images")
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        for class_name in classes:
            logging.info(f"Handled class: {class_name}")
            class_path = os.path.join(old_path, class_name)
            images = os.listdir(os.path.join(old_path, class_name))
            for image in images:
                shutil.copyfile(os.path.join(class_path, image),
                                os.path.join(new_path, f"{class_name}_{image}"))
        logging.info("Copying of images is completed")
    except Exception as exc:
        logging.error(f"Error: {exc}")


def create_copy_annotation(dataset_dir: str, classes: list[str], save_path: str):
    """
    Создание аннотации для датасета
    :param dataset_dir: Папка датасета
    :param classes: Классы изображений
    :param save_path: Путь к аннотации
    :return:
    """
    try:
        logging.info("Start of annotation creation")
        if os.path.exists(save_path):
            os.remove(save_path)
        paths = get_paths(dataset_dir)
        abs_paths = get_abs_paths(dataset_dir)
        for class_name in classes:
            logging.info(f"Handled class: {class_name}")
            with open(save_path, 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter='\t', lineterminator='\n')
                for path, abs_path in zip(paths, abs_paths):
                    if class_name in path:
                        writer.writerow([abs_path, path, class_name])
        logging.info("Annotation creation is completed")
    except Exception as exc:
        logging.error(f"Error: {exc}")
