import sys
from PyQt5.QtWidgets import *
import MyComponents.MyWidget_exo1 as exo1
import os
from PyQt5.QtGui import QPixmap
class MyImageViewerWidget(QFrame):

    def __init__(self, *args):

        super(MyImageViewerWidget, self).__init__(*args)
        self.setGeometry(0, 0, 800, 600)
        
        self.ui = exo1.Ui_Form() 
        
        self.ui.setupUi(self)
        
        self.images=[]
        self.image_index=0
        # self.ui.mLabel.setScaledContents(True)
 
    def LoadFiles(self):
        print("Loading files...")
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path:
            self.ui.mLineEdit.setText(path)
            liste_fichier = os.listdir(path)
            types_fichier = ['.png', '.jpg']
            self.images = []
            for i in liste_fichier:
                _, extension = os.path.splitext(i)
                if extension in types_fichier:
                    self.images.append(i)
            if len(self.images) > 0:
                self.image_index = 0
                self.AfficherImage()

    def Next(self):
        if not self.images:
            return
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.AfficherImage()
        print("Next image")

    def Previous(self):
        if not self.images:
            return
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.images) - 1
        self.AfficherImage()
        print("Previous image")

    def AfficherImage(self, ):
        image = self.images[self.image_index]
        self.path_complet = os.path.join(self.ui.mLineEdit.text(), image)
        self.px = QPixmap(self.path_complet)
        self.ui.mLabel.setPixmap(self.px)



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