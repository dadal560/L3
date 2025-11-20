import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime


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

        self.createActions()
        self.createMenus()

    def resizeEvent(self,event):
        self.titleMainWindow = self.titleInfo + datetime.now().strftime("  %H:%M:%S") + '| Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow) 

    def createActions(self):
        """ Créer ici les actions d'item de menu ainsi que connexions signal/slot, à compléter"""
        self.exitAct = QAction(" &Quit", self)
        self.exitAct.setShortcut("Ctrl+X")
        
        self.open = QAction(" &Open", self)
        self.open.setShortcut("Ctrl+O")
        self.open.triggered.connect(self.myOpen)
        
        self.save = QAction(" &Save", self)
        self.save.setShortcut("Ctrl+S")
        self.save.triggered.connect(self.mySave)
        
        self.restore = QAction(" &Restore", self)
        self.restore.setShortcut("Ctrl+R")
        self.restore.triggered.connect(self.myRestore)
        
        self.bye = QAction(" &Bye", self)
        self.bye.setShortcut("Ctrl+B")
        self.bye.triggered.connect(self.myExit)
        
        self.clear = QAction("&Clear", self)
        
        self.color = QAction("C&olor", self)

    def createMenus(self):
        """ Créer ici les menu et les items de menu, à compléter"""
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.exitAct)
        fileMenu.addAction(self.open)
        fileMenu.addAction(self.save)
        fileMenu.addAction(self.restore)
        fileMenu.addSeparator()
        fileMenu.addAction(self.bye)
        
        dislpayMenu =self.menuBar().addMenu("&Display")
        dislpayMenu.addAction(self.clear)
        dislpayMenu.addAction(self.color)
        
    

    def myExit(self):
        """ Slot associé à exitAct, instance de QAction, à compléter """
        self.statusBar.showMessage("Quit ...")
        QApplication.quit()
    
    def myOpen(self):
        self.statusBar.showMessage("Histo-gram opened !")
        fileName, ext = QFileDialog.getOpenFileName(self,"Open File", ".", "*.dat")
        print(fileName)
        if fileName:
            file = QFile(fileName)
            file.open(QIODevice.ReadOnly|QIODevice.Text)
            while not file.atEnd():
                line = file.readLine()
                self.mHisto.m_list.append(int(line))
                self.mHisto.m_size += 1
                self.mHisto.m_max = max(self.mHisto.m_max, int(line))
            print(self.mHisto.m_list)
            print(self.mHisto.m_size)
            print(self.mHisto.m_max)
            file.close()
            self.update()

    def mySave(self):
        self.statusBar.showMessage("Histogram saved !")
        fileName, ext = QFileDialog.getSaveFileName(self,"Save File", ".", "*.dat")
        print(fileName)
        if fileName:
            file = QFile(fileName)
            file.open(QIODevice.WriteOnly|QIODevice.Text)
            for value in self.mHisto.m_list:
                line = str(value) + '\n'
                file.write(line.encode())
            file.close()

    def myRestore(self):
        self.statusBar.showMessage("Histogram restored !")
        self.mHisto.m_list = []
        self.mHisto.m_size = 0
        self.mHisto.m_max = 0
        self.update()
        
    def myBye(self):
        self.statusBar.showMessage("Bye")
        QApplication.quit()

    def paintEvent(self, event):
        if self.mHisto.m_size == 0:
            return

        painter = QPainter(self)
        painter.begin(self)
        
        painter.setBrush(QColor(Qt.red))
        painter.setPen(Qt.black)             

        w_fenetre = self.width()
        h_fenetre = self.height()
        

        largeur_barre = int(w_fenetre / self.mHisto.m_size)

        for i in range(self.mHisto.m_size):
            valeur = self.mHisto.m_list[i]
            
            hauteur_barre = int((valeur / self.mHisto.m_max) * h_fenetre * 0.9)
            
            x = i * largeur_barre
            
            y = h_fenetre - hauteur_barre
            
            painter.drawRect(x, y, largeur_barre, hauteur_barre)

        painter.end()        

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()
