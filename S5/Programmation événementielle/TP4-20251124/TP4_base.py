import sys
from PyQt5.QtWidgets import *


class MyImageViewerWidget(QFrame):

    def __init__(self, *args):

        super(MyImageViewerWidget, self).__init__(*args)
        self.setGeometry(0, 0, 800, 600)
 
    def LoadFiles(self):
        print("Loading files...")

    def Next(self):
        print("Next image")

    def Previous(self):
        print("Previous image")




class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # attributs de la fenetre principale
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Simple diaporama application')

        # donnée membre qui contiendra la frame associée à la widget crée par QtDesigner
        self.mDisplay = MyImageViewerWidget(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()