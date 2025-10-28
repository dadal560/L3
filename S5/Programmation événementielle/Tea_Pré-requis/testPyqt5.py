import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QSlider, QVBoxLayout

class Principale(QWidget):
    def _init__(self):
        super().__init__()
        self.initUI()
    def setUI(self):
        lcd = QLCDNumber(self)
        lcd.move(50, 50)

        sld = QSlider(Qt.Horizontal, self)
        sld.valueChanged.connect(lcd.display)
        sld.move(50, 150)

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Fenetre principale')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Principale()
    sys.exit(app.exec_())