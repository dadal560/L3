from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Main vertical layout
        self.verticalLayout = QVBoxLayout(Form)
        # Top: label and side buttons
        self.horizontalLayout = QHBoxLayout()

        self.mLabel = QLabel(Form)
        self.mLabel.setObjectName("mLabel")
        self.mLabel.setFixedSize(640, 480)
        self.mLabel.setStyleSheet("background-color: green;")
        self.mLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.mLabel)

        self.sideLayout = QVBoxLayout()
        self.mButtonN = QPushButton("Next", Form)
        self.mButtonN.setObjectName("mButtonN")
        self.mButtonP = QPushButton("Previous", Form)
        self.mButtonP.setObjectName("mButtonP")
        self.sideLayout.addWidget(self.mButtonN)
        self.sideLayout.addWidget(self.mButtonP)
        self.sideLayout.addStretch()

        self.horizontalLayout.addLayout(self.sideLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Bottom: browse line (lineedit + spacer + button)
        self.browseLayout = QHBoxLayout()
        self.mLineEdit = QLineEdit(Form)
        self.mLineEdit.setObjectName("mLineEdit")
        self.mLineEdit.setReadOnly(True)
        self.mButtonBrowse = QPushButton("...", Form)
        self.mButtonBrowse.setObjectName("mButtonBrowse")

        self.browseLayout.addWidget(self.mLineEdit)
        self.browseLayout.addStretch()
        self.browseLayout.addWidget(self.mButtonBrowse)

        self.verticalLayout.addLayout(self.browseLayout)

        # Try to connect buttons to Form slots if they exist
        try:
            if hasattr(Form, "LoadFiles"):
                self.mButtonBrowse.clicked.connect(Form.LoadFiles)
        except Exception:
            pass
        try:
            if hasattr(Form, "Next"):
                self.mButtonN.clicked.connect(Form.Next)
        except Exception:
            pass
        try:
            if hasattr(Form, "Previous"):
                self.mButtonP.clicked.connect(Form.Previous)
        except Exception:
            pass

# Convenience QWidget wrapper
class MyWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
