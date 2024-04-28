import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from annotation import create_annotation
from copy_images import create_dataset_copy, create_copy_annotation
from random_dataset import create_dataset_random, create_random_annotation
from iterator import Iterator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dataset_path = None
        self.annotation_path = None

        self.__init_ui()
        self.__create_action()
        self.__create_menu_bar()

        self.cat_iter = None
        self.dog_iter = None

    def __init_ui(self):
        self.resize(1000, 800)
        self.center()
        self.setWindowTitle('Cat and Dog')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        cat_btn = QPushButton('Next cat', self)
        dog_btn = QPushButton('Next dog', self)
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
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText(message)
        mb.exec()

    def next_cat(self):
        if self.dataset_path is None:
            self.get_message_box("Please, select dataset")
            return
        if self.annotation_path is None:
            self.get_message_box("Please, create annotation")
            return
        lbl_size = self.lbl.size()

        try:
            next_image = next(self.cat_iter)
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        except:
            self.cat_iter = Iterator("cat", self.annotation_path)
            self.next_cat()

    def next_dog(self):
        if self.dataset_path is None:
            self.get_message_box("Please, select dataset")
            return
        if self.annotation_path is None:
            self.get_message_box("Please, create annotation")
            return

        lbl_size = self.lbl.size()
        try:
            next_image = next(self.dog_iter)
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        except:
            self.dog_iter = Iterator("dog", self.annotation_path)
            self.next_dog()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __create_menu_bar(self):
        menu_bar = self.menuBar()
        self.fileMenu = menu_bar.addMenu('&File')
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.changeAction)

        self.annotMenu = menu_bar.addMenu('&Annotation')
        self.annotMenu.addAction(self.createAnnotAction)

        self.dataMenu = menu_bar.addMenu('&Datasets')
        self.dataMenu.addAction(self.createData2Action)

    def __create_action(self):
        self.exitAction = QAction('&Exit')
        self.exitAction.triggered.connect(qApp.quit)

        self.changeAction = QAction('&Select dataset')
        self.changeAction.triggered.connect(self.select_dataset)

        self.createAnnotAction = QAction('&Create annotation for current dataset')
        self.createAnnotAction.triggered.connect(self.__create_annotation)

        self.createData2Action = QAction('&Create copy dataset')
        self.createData2Action.triggered.connect(self.create_copy_dataset)

        self.createData3Action = QAction('&Create random dataset')
        self.createData3Action.triggered.connect(self.create_random_dataset)

    def __create_annotation(self):
        if self.dataset_path is None:
            self.get_message_box("Please, select dataset")
            return
        self.annotation_path = QFileDialog.getSaveFileName(self, 'Create file', filter="(*.csv)")[0]
        create_annotation(self.dataset_path, ["cat", "dog"], self.annotation_path)
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText("Task completed")
        mb.exec()

    def create_copy_dataset(self):
        if self.dataset_path is None:
            self.get_message_box("Please, select base dataset")
            return
        self.dataset_copy_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.dataset_copy_path = os.path.relpath(self.dataset_copy_path)
        create_dataset_copy(self.dataset_path, self.dataset_copy_path, ["cat", "dog"])
        create_copy_annotation(self.dataset_copy_path, ["cat", "dog"],
                               os.path.join(self.dataset_copy_path, "annotation.csv"))

        self.dataMenu.addAction(self.createData3Action)
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText("Task completed")
        mb.exec()

    def create_random_dataset(self):
        if self.dataset_path is None:
            self.get_message_box("Please, select base dataset")
            return

        dataset_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        dataset_path = os.path.relpath(dataset_path)
        classes_dict = create_dataset_random(self.dataset_copy_path, dataset_path, ["cat", "dog"])
        create_random_annotation(dataset_path, classes_dict,
                                 os.path.join(dataset_path, "annotation.csv"))
        mb = QMessageBox()
        mb.setWindowTitle("Message")
        mb.setText("Task completed")
        mb.exec()

    def select_dataset(self):
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.dataset_path = os.path.relpath(self.dataset_path)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
