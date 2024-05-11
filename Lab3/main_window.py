import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, \
    QLabel, QHBoxLayout, QVBoxLayout, QMessageBox, QDesktopWidget, \
    QAction, qApp, QFileDialog

from annotation import create_annotation
from copy_images import create_dataset_copy, create_copy_annotation
from iterator import Iterator
from random_dataset import create_dataset_random, create_random_annotation


class MainWindow(QMainWindow):
    """
    Окно приложения
    """
    def __init__(self, settings: str):
        """
        Конструктор
        :param settings: путь к json файлу с параметрами программы
        """
        super().__init__()

        self.dataset_path = None
        self.annotation_path = None

        self.__init_ui()
        self.__create_action()
        self.__create_menu_bar()

        self.cat_iter = None
        self.dog_iter = None
        self.classes = None
        self.annotation_name = None
        self.__set_settings(settings)

    def __set_settings(self, settings: str):
        """
        Установка параметров программы
        :param settings: путь к json файлу с параметрами программы
        :return:
        """
        try:
            with open(settings, "r") as read_file:
                data = json.load(read_file)
                self.annotation_name = data["annotation_path"]
                self.classes = data["classes"]
                if len(self.classes) != 2:
                    raise ValueError("Неверное количество классов")
        except:
            self.get_message_box("Ошибка закрузки параметров программы")
            sys.exit()

    def __init_ui(self):
        """
        Создание основных компонентов окна
        :return:
        """
        self.resize(1000, 800)
        self.center()
        self.setWindowTitle('Viewer')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        cat_btn = QPushButton(f'Next {self.classes[0]}', self)
        dog_btn = QPushButton(f'Next {self.classes[1]}', self)
        cat_btn.clicked.connect(self.next_cat)
        dog_btn.clicked.connect(self.next_dog)

        self.lbl = QLabel(self)

        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        hbox.addWidget(cat_btn)
        hbox.addWidget(dog_btn)

        vbox = QVBoxLayout()
        vbox.addSpacing(1)
        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)

        self.centralWidget.setLayout(vbox)
        self.show()

    @staticmethod
    def get_message_box(message: str):
        """
        Создание QMessageBox
        :param message: Сообщение
        :return:
        """
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText(message)
        mb.exec()

    def check_dataset(self) -> bool:
        """
        Проверка наличия выбранного датасета
        :return: True - датасет выбран, False - иначе
        """
        if self.dataset_path is None:
            self.get_message_box("Please, select dataset")
            return False
        return True

    def check_annotation(self) -> bool:
        """
        Проверка наличия выбранной аннотации
        :return: True - аннотация выбрана, False - иначе
        """
        if self.annotation_path is None:
            self.get_message_box("Please, create annotation")
            return False
        return True

    def next_cat(self):
        """
        Получение следующего изображения кота
        :return:
        """
        if not self.check_dataset() and not self.check_annotation():
            return
        lbl_size = self.lbl.size()

        try:
            next_image = next(self.cat_iter)
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        except:
            self.cat_iter = Iterator(self.classes[0], self.annotation_path)
            self.next_cat()

    def next_dog(self):
        """
        Получение следующего изображения собаки
        :return:
        """
        if not self.check_dataset() and not self.check_annotation():
            return

        lbl_size = self.lbl.size()
        try:
            next_image = next(self.dog_iter)
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        except:
            self.dog_iter = Iterator(self.classes[1], self.annotation_path)
            self.next_dog()

    def center(self):
        """
        Выравнивание по центру
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __create_menu_bar(self):
        """
        Создание панели меню
        :return:
        """
        menu_bar = self.menuBar()
        self.fileMenu = menu_bar.addMenu('File')
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.changeAction)

        self.annotMenu = menu_bar.addMenu('Annotation')
        self.annotMenu.addAction(self.createAnnotAction)

        self.dataMenu = menu_bar.addMenu('Datasets')
        self.dataMenu.addAction(self.createData2Action)

    def __create_action(self):
        """
        Создание и подключение событий окна
        :return:
        """
        self.exitAction = QAction('Exit')
        self.exitAction.triggered.connect(qApp.quit)

        self.changeAction = QAction('Select dataset')
        self.changeAction.triggered.connect(self.select_dataset)

        self.createAnnotAction = QAction('Create annotation for current dataset')
        self.createAnnotAction.triggered.connect(self.__create_annotation)

        self.createData2Action = QAction('Create copy dataset')
        self.createData2Action.triggered.connect(self.create_copy_dataset)

        self.createData3Action = QAction('Create random dataset')
        self.createData3Action.triggered.connect(self.create_random_dataset)

    def __create_annotation(self):
        """
        Создание аннотации к датасету
        :return:
        """
        if not self.check_dataset():
            return
        self.annotation_path = QFileDialog.getSaveFileName(self, 'Create file', filter="(*.csv)")[0]
        create_annotation(self.dataset_path, self.classes, self.annotation_path)
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText("Task completed")
        mb.exec()

    def create_copy_dataset(self):
        """
        Создание копии датасета и его аннотации
        :return:
        """
        if not self.check_dataset():
            return
        self.dataset_copy_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.dataset_copy_path = os.path.relpath(self.dataset_copy_path)
        create_dataset_copy(self.dataset_path, self.dataset_copy_path, self.classes)
        create_copy_annotation(self.dataset_copy_path, self.classes,
                               os.path.join(self.dataset_copy_path, self.annotation_name))

        self.dataMenu.addAction(self.createData3Action)
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText("Task completed")
        mb.exec()

    def create_random_dataset(self):
        """
        Создание датасета с перемешанными изображениями
        :return:
        """
        if not self.check_dataset():
            return

        dataset_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        dataset_path = os.path.relpath(dataset_path)
        classes_dict = create_dataset_random(self.dataset_copy_path, dataset_path, self.classes)
        create_random_annotation(dataset_path, classes_dict,
                                 os.path.join(dataset_path, self.annotation_name))
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText("Task completed")
        mb.exec()

    def select_dataset(self):
        """
        Выбор датасета
        :return:
        """
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.dataset_path = os.path.relpath(self.dataset_path)

    def closeEvent(self, event):
        """
        Событие закрытия окна
        :param event:
        :return:
        """
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow("settings.json")
    sys.exit(app.exec_())
