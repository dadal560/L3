import sys
import random
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal

class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.setWindowTitle('Tetris PyQt6')
        self.resize(300, 600)
        self.show()

class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    def start(self):
        self.isStarted = True
        self.numLinesRemoved = 0
        self.clearBoard()
        self.msg2Statusbar.emit(str(self.numLinesRemoved))
        self.newPiece()
        self.timer.start(Board.Speed, self)

    def clearBoard(self):
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(0)

    def newPiece(self):
        self.curPiece = [ [0,0], [0,1], [1,0], [1,1] ] # Simple Carré pour l'exemple
        self.curX = Board.BoardWidth // 2
        self.curY = 0

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.curY += 1
            self.update()
        else:
            super(Board, self).timerEvent(event)

    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QColor
        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
                if shape != 0:
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), QColor(0xCC6666))

        for i in range(4):
            x = self.curX + self.curPiece[i][0]
            y = self.curY + self.curPiece[i][1]
            self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                            boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(), QColor(0x66CC66))

    def drawSquare(self, painter, x, y, color):
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, self.squareHeight() - 2, color)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Left:
            self.curX -= 1
        elif key == Qt.Key.Key_Right:
            self.curX += 1
        elif key == Qt.Key.Key_Down:
            self.curY += 1
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tetris()
    sys.exit(app.exec())