import csv


class Iterator:
    def __init__(self, class_name: str, annotation: str):
        """
        Инициализация
        :param class_name: Класс изображения
        :param annotation: Путь к аннотации датасета
        """
        self.dataset = []
        with open(annotation, mode='r') as file:
            reader = csv.reader(file, delimiter='\t', lineterminator='\n')
            for lines in reader:
                self.dataset.append(lines)
        self.class_name = class_name
        self.counter = 0
        self.limit = len(self.dataset)

    def __iter__(self):
        return self

    def __next__(self):
        while self.counter < self.limit and self.dataset[self.counter][2] != self.class_name:
            self.counter += 1
        if self.counter < self.limit:
            path = self.dataset[self.counter][0]
            self.counter += 1
            return path
        else:
            raise StopIteration


if __name__ == "__main__":
    cat = Iterator("cat", "annotation.csv")
    print(next(cat))
    for cat in Iterator("cat", "annotation.csv"):
        print(cat)
