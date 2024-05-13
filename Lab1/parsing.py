import logging
import os
import requests

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from fake_headers import Headers

def create_dir(path: str):
    """
    Создание директории
    :param path: Путь к директории
    :return:
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f"Creating dir: {path}")
    except Exception as exc:
        logging.error(f"Error: {exc}")


def download_images(path: str, key: str, page: int, count: int = 1000,
                    url: str = "https://yandex.ru/images/"):
    """
    Парсинг изображений
    :param path: Путь к папке с изображениями
    :param key: Класс изображения
    :param page: Страница старта
    :param count: Количество скачиваемых изображений
    :param url: url
    :return:
    """
    try:
        logging.info("Start downloading images")
        index = len(os.listdir(path))
        if index >= count:
            logging.info("Image download completed")
            return
        while True:
            header = Headers(headers=False).generate()
            url = url + f'search?p={page}&text={key}'
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.text, 'lxml')
            images = soup.find_all('img', 'ContentImage-Image_clickable')
            for image in images:
                if index >= count:
                    logging.info("Image download completed")
                    return
                image_url = image.get("src")
                if image_url and not image_url.startswith("data:"):
                    picture = requests.get(f"https:{image_url}", header)

                    with open(os.path.join(path, f"{str(index).zfill(4)}.jpg"), "wb") as f:
                        f.write(picture.content)

                    index += 1
            logging.info(f"Page: {page}, saved images: {index}")
            page += 1
    except Exception as exc:
        logging.error(f"Error: {exc}")


if __name__ == "__main__":
    logging.basicConfig(filename='lab1.log', level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('data_dir', type=str, help='Directory for dataset')
    parser.add_argument('-c', '--classes', nargs='+', help='List of classes', required=True)
    args = parser.parse_args()

    for cls in args.classes:
        logging.info(f"Handled class: {cls}")
        dir_path = os.path.join(args.data_dir, cls)
        create_dir(dir_path)
        download_images(dir_path, cls, 1, 1000)
