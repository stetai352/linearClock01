from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from datetime import datetime
import sys


class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Set window size and position
        self.short = 3
        screen = QApplication.primaryScreen()
        #tbwidth = screen.geometry().width() - screen.availableGeometry().width()
        fullW = screen.geometry().width()
        scH = screen.availableGeometry().height()
        self.setGeometry(0, scH - 2*self.short, fullW, 2*self.short)
        #self.setGeometry(tbwidth, scH - 2*self.short, scW, 2*self.short)

        # QLabel to display the graphic
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, fullW, 2*self.short)

        # Timer to update the graphic
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graphic)
        self.timer.start(200)  # Update every 100ms

        # Custom graphic as a placeholder
        self.update_graphic()

    def update_graphic(self):
        # Create pixmap that displays the progress bar
        colour1 = QColor(255, 102, 0, 255)
        colour2 = QColor(0, 0, 0, 255)
        short = self.short

        now = datetime.now()
        total_seconds = 24 * 3600
        secD = now.hour * 3600 + now.minute * 60 + now.second
        secH = now.minute * 60 + now.second
        relD = secD / total_seconds
        relH = secH / 3600

        scW = QApplication.primaryScreen().availableGeometry().width()
        fullW = QApplication.primaryScreen().geometry().width()
        tbW = QApplication.primaryScreen().geometry().width() - scW
        tick_width = max(int(scW / 1000), 1)
        
        progD = int(relD * scW)
        progH = int(relH * scW)

        pixmap = QPixmap(fullW, 2*short)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        

        painter.setBrush(colour1)
        painter.drawRect(tbW, short, progD, short)
        painter.drawRect(tbW, 0, progH, short)

        painter.setBrush(colour2)
        for i in range(1, 24):
            tickpos = tbW + int(i * scW / 24)
            painter.drawRect(tickpos, short+1, tick_width, short)
            if (i % 6 == 0):
                painter.drawRect(tickpos, 0, tick_width+1, 2*short)

        painter.end()
        self.label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()
    sys.exit(app.exec_())
