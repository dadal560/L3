import sys
from syracuse_bad import GenerateSyracuseSequence 
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor
import socket



class MyMainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,500,300)
    

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        title = "HENRY " + datetime.now().strftime("%H:%M:%S")
        self.setWindowTitle(title)
        self.setWindowModified(True)

        self.labal=QLabel("Saisir un monbre et cliquer", self)
        self.display=QPushButton("Resultat",self)
        self.values=QLineEdit(self)        
        self.te=QTextEdit(self)
        self.sortie=QPushButton("Quitter",self)

        self.lb = QLabel()
        self.lb.setFixedWidth(500)
        self.lb.setFixedHeight(300)
        self.lb.setFrameShape(QFrame.Panel)
        self.px = QPixmap(500,300)

        layout.addWidget(self.labal)
        layout.addWidget(self.values)
        layout.addWidget(self.display)        
        layout.addWidget(self.te)
        layout.addWidget(self.lb)
        layout.addWidget(self.sortie)

        self.sortie.clicked.connect(self.close)
        self.display.clicked.connect(self.DisplayMessage)

    def DisplayMessage(self):
        value = self.values.text()
        result = GenerateSyracuseSequence(int(value))
        for i in result:
            self.te.append(str(i))
        self.te.append("Nombre d'éléments: "+str(len(result)))
        self.te.append("Valeur la plus grande: "+ str(max(result)))

        self.px.fill(QColor(200, 200, 200))
        painter = QPainter(self.px)
        painter.setPen(QColor(255,0,0))
        for i in range(len(result)):
            h = 300
            w = 500

            x = int(i * w / len(result))
            y = int(h - (result[i] * h / max(result)))

            x1 = int((i-1) * w / len(result))
            y1 = int(h - (result[i-1] * h / max(result)))

            x2 = x
            Y2 = y
            painter.drawPoint(x,y)
            painter.drawLine(x1,y1,x2,Y2)
        self.lb.setPixmap(self.px)
        painter.end()
    def closeEvent(self, event):
        rep = QMessageBox.question(self,"","Souhaitez-vous vraiment quitter ?",
                                     QMessageBox.Yes | QMessageBox.No)

        if rep == QMessageBox.Yes:
            event.accept() 
        else:
            event.ignore()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()

