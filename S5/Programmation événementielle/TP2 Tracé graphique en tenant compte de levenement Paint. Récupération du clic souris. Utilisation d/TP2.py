import sys
import urllib.request
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtWebEngineWidgets import QWebEngineView

BASE_URL = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_name'

os.environ["QT_QPA_PLATFORM"] = "xcb"  # force le mode X11 avant d'importer PyQt5
class myBrowserWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        
        self.setWindowTitle("Pokémon Browser (Piloté par la Grille)")
        
        # Le widget de navigateur occupant tout l'espace
        self.myBrowserWidget = QWebEngineView(self)
        
        # Consigne: donner une taille fixe
        self.setFixedSize(800, 600) 
        
        # Chargement de la page de base
        self.myBrowserWidget.load(QUrl(BASE_URL))
        
        # Layout pour s'assurer que le navigateur prend toute la fenêtre
        layout = QVBoxLayout(self)
        layout.addWidget(self.myBrowserWidget)
        self.setLayout(layout)

    def changeLetter(self, letter):
        """
        Méthode appelée par le signal de la grille.
        Modifie l'URL en ajoutant le fragment (#A, #B, etc.) et recharge la page.
        """
        print(f"Browser: Réception du signal pour la lettre '{letter}'.")
        
        # Construction de la nouvelle URL avec l'ancre (#A, #B...)
        new_url = BASE_URL + '#' + letter
        
        # Chargement de la nouvelle URL
        self.myBrowserWidget.load(QUrl(new_url))
        
        self.setWindowTitle(f"Pokémon Browser - Lettre: {letter}")

class myMainWindow(QWidget): 
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # attributs de la fenetre principale
        self.setGeometry(300,300,800,400)
        self.setMinimumSize(QSize(400,200))
        self.titlestart = "HENRY" + datetime.now().strftime("  %H:%M:%S")
        self.setWindowTitle(self.titlestart) 
        self.rectUtil = self.rect()

        self.initUI()   # appel d'une methode dédiée à la création de l'IHM
        
        self.paint_count = 0

        self.x = 0
        self.y = 0


        self.doPaint = False


    def initUI(self):
        w = self.width()
        h = self.height()
        print(str(w)+","+str(h))
        # self.bu1 = QPushButton("Dessine", self)
        # self.bu2 = QPushButton("Efface", self)
        # self.bu1.move(10,10)
        # self.bu2.move(10,50)
        # self.bu1.clicked.connect(self.actionDessine)
        # self.bu2.clicked.connect(self.actionEfface)

    def actionDessine(self):
        self.resize(400, 200)
        self.doPaint = True
        self.update()

    def actionEfface(self):
        self.resize(800, 400)
        self.doPaint = False
        self.update()
    
    def afficheLettre(self,qp, w, h):
        for i in range(26):
            char_code = ord("A") + i
            x = (i%13)*w//13 + w//26
            y = (i//13)*h//2 + h//4
            qp.drawText(x, y, chr(char_code))
    
    def paintEvent(self, event):
        self.paint_count += 1
        print(f"Paint event N°: {self.paint_count}")

        qp = QPainter()
        
        qp.begin(self)

        # qp.drawText(self.rect(), Qt.AlignCenter, f"Paint event N°: {self.paint_count} Mouse dc at:{self.x},{self.y}")

        if self.doPaint:
            qp.setPen(QPen(Qt.black, 4))
            w = self.width()
            h = self.height()
            qp.drawLine(0,h/2,w,h/2)
            for i in range(13):
                qp.drawLine(i*(w/13),0,i*(w/13),h)
            self.afficheLettre(qp, w, h)
        qp.end()

    def mouseReleaseEvent(self, event):
        self.x = event.x()
        self.y = event.y()

        h=self.height()
        w=self.width()

        col=w//13
        row=h//2

        index=(self.y//row)*13 + (self.x//col)
        if index<26:
            char_code = ord("A") + index
            print(f"lettre: {chr(char_code)}")

        
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.actionDessine()
        elif event.key() == Qt.Key_E:
            self.actionEfface()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myMainWindow()
    v = myBrowserWindow()
    v.show() 
    w.show() 
    app.exec_()    # ou de préférence sys.exit(app.exec_()) si vous êtes sous linux
