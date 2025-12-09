import random
import sys
import time
from PyQt5.QtWidgets import *
import MyComponents.MyWidget_exo1 as exo1
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime


os.environ["QT_QPA_PLATFORM"] = "xcb" 


class MyImageViewerWidget(QFrame):

    def __init__(self, *args):

        super(MyImageViewerWidget, self).__init__(*args)
        self.setGeometry(0, 0, 1000, 600)
        
        self.ui1 = exo1.Ui_Form() 
        self.ui1.setupUi(self)
        self.ui1.mLabel.move(0,50)

        self.ui2 = exo1.Ui_Form() 
        self.ui2.setupUi(self)
        self.ui2.mLabel.move(300,50)

        self.ui3 = exo1.Ui_Form() 
        self.ui3.setupUi(self)
        self.setFocus()
        self.ui3.mLabel.move(600,50)
        
        self.images= []
        self.image_index=0

        self.path = "./slot_machine_symbols.png"
        self.bigimage = QPixmap(self.path)
        for col in range(3):
            for row in range(3):
                rect = QRect(col * 300, row * 300, 300, 300)
                cropped = self.bigimage.copy(rect)
                self.images.append(cropped)

    def machineStart(self):
        a = self.ui1.mLabel
        b = self.ui2.mLabel
        c = self.ui3.mLabel

        final_a_idx = 0
        final_b_idx = 0
        final_c_idx = 0
                    
        for i in range(0, 20):
            time.sleep((50 + 25 * i) / 1000) 
            c_index = random.randint(0, 3)
            c.setPixmap(self.images[c_index])
            final_c_idx = c_index

            if i < 10:
                a_index = random.randint(0, 3)
                a.setPixmap(self.images[a_index])
                final_a_idx = a_index
            
            if i < 15:
                b_index = random.randint(0, 3)
                b.setPixmap(self.images[b_index])
                final_b_idx = b_index
            QApplication.processEvents()


        jackpot = (final_a_idx == final_b_idx == final_c_idx)
        
      
        if jackpot:
            print("You win the jackpot!")
        else:
            print("You lose.") 
        

    def keyPressEvent(self, event):
        self.timer = QTimer()
        if event.key() == Qt.Key_S:
            self.machineStart()
        if event.key() == Qt.Key_Escape:
            self.close()
class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # attributs de la fenetre principale
        self.setGeometry(100, 100, 1300, 600)
        self.titleInfo = "Henry"
        self.titleMainWindow = self.titleInfo + datetime.now().strftime("  %H:%M:%S") + ' | Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow) 
        self.mDisplay = MyImageViewerWidget(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()

