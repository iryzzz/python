import os

from bs4 import BeautifulSoup
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def download_images(path: str, key: str, page: int, count: int = 1000) -> int:
    """
    Парсинг изображений
    :param path: Путь к папке с изображениями
    :param key: Класс изображения
    :param page: Страница старта
    :param count: Количество скачиваемых изображений
    :return: Страница окончания
    """
    index = len(os.listdir(path))
    if index >= count:
        return page
    while True:
        url = f'https://yandex.ru/images/search?p={page}&text={key}'
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        images = soup.find_all('img', 'ContentImage-Image_clickable')
        for image in images:
            if index >= count:
                return page
            image_url = image.get("src")
            if image_url and not image_url.startswith("data:"):
                picture = requests.get(f"https:{image_url}", HEADERS)

                with open(os.path.join(f"{path}/{str(index).zfill(4)}.jpg"), "wb") as f:
                    f.write(picture.content)

                index += 1
        page += 1


if __name__ == "__main__":
    if not os.path.exists("dataset/cat"):
        os.makedirs("dataset/cat")
    if not os.path.exists("dataset/dog"):
        os.makedirs("dataset/dog")
    print(download_images("dataset/cat", 'cat', 1, 1000))
    print(download_images("dataset/dog", 'dog', 1, 1000))
