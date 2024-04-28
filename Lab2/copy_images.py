import os
import csv
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
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for class_name in classes:
        class_path = os.path.join(old_path, class_name)
        images = os.listdir(os.path.join(old_path, class_name))
        for image in images:
            shutil.copyfile(os.path.join(class_path, image),
                            os.path.join(new_path, f"{class_name}_{image}"))


def create_copy_annotation(dataset_dir: str, classes: list[str], save_path: str):
    """
    Создание аннотации для датасета
    :param dataset_dir: Папка датасета
    :param classes: Классы изображений
    :param save_path: Путь к аннотации
    :return:
    """
    if os.path.exists(save_path):
        os.remove(save_path)
    paths = get_paths(dataset_dir)
    abs_paths = get_abs_paths(dataset_dir)
    for class_name in classes:
        with open(save_path, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter='\t', lineterminator='\n')
            for path, abs_path in zip(paths, abs_paths):
                if class_name in path:
                    writer.writerow([abs_path, path, class_name])


if __name__ == "__main__":
    create_dataset_copy("dataset", "dataset_copy", ["cat", "dog"])
    create_copy_annotation("dataset_copy", ["cat", "dog"], "annotation_copy.csv")
