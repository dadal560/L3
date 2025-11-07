import sys
from random import randint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QSlider, QVBoxLayout

class Principale(QWidget):
    def __init__(self):
        super().__init__()
        
        self.myValue = randint(0, 99) 
        
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout() 

        lcd = QLCDNumber(self)
        
        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(0, 99) 
        
        sld.setValue(self.myValue) 

        sld.valueChanged.connect(lcd.display)
        
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        
        self.setLayout(vbox)

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Fenetre principale')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Principale()
    sys.exit(app.exec_())