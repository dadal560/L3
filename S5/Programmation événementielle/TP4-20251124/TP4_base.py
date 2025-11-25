import sys
from PyQt5.QtWidgets import *
import MyComponents.MyWidget_exo1 as exo1
import os
class MyImageViewerWidget(QFrame):

    def __init__(self, *args):

        super(MyImageViewerWidget, self).__init__(*args)
        self.setGeometry(0, 0, 800, 600)
        
        self.ui = exo1.Ui_Form() 
        
        self.ui.setupUi(self)
 
    def LoadFiles(self):
        print("Loading files...")
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path:
            self.ui.mLineEdit.setText(path)
            liste_fichier = os.listdir(path)
            types_fichier = ['.png', '.jpg']
            self.images=[]
            for i in liste_fichier:
                _, extension = os.path.splitext(i)
                if extension in types_fichier:
                    self.images.append(i)
            print(self.images)

    def Next(self):
        print("Next image")

    def Previous(self):
        print("Previous image")




class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # attributs de la fenetre principale
        self.setGeometry(100, 100, 900, 600)
        self.setWindowTitle('Simple diaporama application')

        # donnée membre qui contiendra la frame associée à la widget crée par QtDesigner
        self.mDisplay = MyImageViewerWidget(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()