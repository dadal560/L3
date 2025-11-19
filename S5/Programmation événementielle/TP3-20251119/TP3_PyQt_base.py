import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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

    def mySave(self):
        self.statusBar.showMessage("Histogram saved !")

    def myRestore(self):
        self.statusBar.showMessage("Histogram restored !")
        

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()
