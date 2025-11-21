import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
import os
import random
import pickle
os.environ["QT_QPA_PLATFORM"] = "xcb" 


class myHisto:
    """Classe myHisto pour stocker l'histogramme"""

    def __init__(self):
        print('Méthode __init__()  de la classe myHisto')
        self.m_list = []
        self.m_size = 0
        self.m_max = 0



class MyMainWindow(QMainWindow):
    """ Classe de l'application principale"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # Attributs de la fenetre principale
        self.setGeometry(300, 300, 600, 450)
        self.titleInfo = "Henry"
        self.titleMainWindow = self.titleInfo + datetime.now().strftime("  %H:%M:%S") + ' | Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow) 
        # Barre de status pour afficher les infos
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Zone d'informations, peut toujours servir")

        # Creation d'une instance de la classe myHisto
        self.mHisto = myHisto()
    
        self.setAcceptDrops(True)

        self.histoColor= Qt.red
        self.colorIcon = QPixmap(16, 16)
        self.colorIcon.fill(QColor(self.histoColor))

        self.createActions()
        self.createMenus()



    def resizeEvent(self,event):
        self.titleMainWindow = self.titleInfo + datetime.now().strftime("  %H:%M:%S") + '| Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow) 

    def createActions(self):
        """ Créer ici les actions d'item de menu ainsi que connexions signal/slot, à compléter"""
        self.open = QAction("&Open", self)
        self.open.setShortcut("Ctrl+O")
        self.open.triggered.connect(self.myOpen)
        
        self.save = QAction("&Save", self)
        self.save.setShortcut("Ctrl+S")
        self.save.triggered.connect(self.mySave)
        
        self.restore = QAction("&Restore", self)
        self.restore.setShortcut("Ctrl+R")
        self.restore.triggered.connect(self.myRestore)
        
        self.bye = QAction("&Bye", self)
        self.bye.setShortcut("Ctrl+B")
        self.bye.triggered.connect(self.myBye)
        
        self.clear = QAction("&Clear", self)
        self.clear.setShortcut("Ctrl+C")

        self.color = QAction("&Color", self)
        self.color.setIcon(QIcon(self.colorIcon))
        self.color.triggered.connect(self.myColor)

    def createMenus(self):
        """ Créer ici les menu et les items de menu, à compléter"""
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.open)
        fileMenu.addAction(self.save)
        fileMenu.addAction(self.restore)
        fileMenu.addSeparator()
        fileMenu.addAction(self.bye)
        
        dislpayMenu =self.menuBar().addMenu("&Display")
        dislpayMenu.addAction(self.clear)
        dislpayMenu.addAction(self.color)
        
    
    def myOpen(self):
        self.statusBar.showMessage("Histo-gram opened !")
        fileName, ext = QFileDialog.getOpenFileName(self,"Open File", ".", "*.dat")
        self.lectureFichier(fileName)

    def mySave(self):
        self.statusBar.showMessage("Histogram saved !")
        with open("./saveHisto.bin","wb") as file:
            pickle.dump(self.mHisto.m_list,file)
        

    def myRestore(self):
        self.statusBar.showMessage("Histogram restored !")
        with open("./saveHisto.bin","rb") as file:
            self.mHisto.m_list = pickle.load(file)
            self.mHisto.m_size = len(self.mHisto.m_list)
            self.mHisto.m_max = max(self.mHisto.m_list)
            self.update()
    
    def myBye(self):
        self.statusBar.showMessage("Bye")
        QApplication.quit()

    def myClear(self):
        self.statusBar.showMessage("Clear")
        self.mHisto.m_list = []
        self.mHisto.m_size = 0
        self.mHisto.m_max = 0
        self.update()
        
    def myColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.statusBar.showMessage("Color changed!")
            self.histoColor= color
            self.colorIcon.fill(color)
            self.color.setIcon(QIcon(self.colorIcon))
            self.update()

    def lectureFichier(self,fileName):
        self.mHisto.m_list = []
        self.mHisto.m_size = 0
        self.mHisto.m_max = 0
        if fileName:
            file = QFile(fileName)
            file.open(QIODevice.ReadOnly|QIODevice.Text)
            while not file.atEnd():
                line = file.readLine()
                self.mHisto.m_list.append(int(line))
                self.mHisto.m_size += 1
                self.mHisto.m_max = max(self.mHisto.m_max, int(line))
            file.close()
            self.update()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            filename= url.toLocalFile()
            self.lectureFichier(filename)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.mHisto.m_list = []
            self.mHisto.m_size = 0
            self.mHisto.m_max = 0
            for i in range(9):
                self.mHisto.m_list.append(random.randint(0,99))
                self.mHisto.m_size+=1
                self.mHisto.m_max = max(self.mHisto.m_max,  self.mHisto.m_list[i])
            self.update()

    def paintEvent(self, event):
        if self.mHisto.m_list:

            painter = QPainter(self)
            painter.begin(self)

            painter.setBrush(QColor(self.histoColor))
            
            painter.setPen(Qt.black)             

            w = self.width()
            h = self.height()
            
            

            largeur_barre = int(w / self.mHisto.m_size)

            for i in range(self.mHisto.m_size):
                
                hauteur_barre = int((self.mHisto.m_list[i] / self.mHisto.m_max) * h)
                
                x = i * largeur_barre
                
                y = h - (hauteur_barre+self.statusBar.height())
                
                painter.drawRect(x, y, largeur_barre, hauteur_barre)

            painter.end()        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()
