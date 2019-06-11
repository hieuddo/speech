from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtGui
import sys
from voice import ASR
from robot import Robot

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.run = False
        self.rb = Robot()
        self.asr = ASR()
        self.initUI()
    
    def initUI(self):
        self.terminal = QTextEdit(self)
        
        self.terminal.setFixedSize(300, 260)
        self.terminal.setReadOnly(True)
        self.terminal.setText('Pick up object!!!\n\nPress Play button to start\n\nAvailable objects:\n-Apple\n-Bread\n-Fork\n-Knife\n-Lecttuce\n-Potato\n-Spoon\n\nSpeak "drop" to drop object')

        self.startBtn = QPushButton()
        self.startBtn.setFixedSize(32,32)
        self.startBtn.setIcon(QtGui.QIcon('button/start.png'))
        self.startBtn.clicked.connect(self.start)
        
        # self.stopBtn = QPushButton()
        # self.stopBtn.setFixedSize(32,32)
        # self.stopBtn.setIcon(QtGui.QIcon('button/stop.png'))
        # self.stopBtn.clicked.connect(self.stop)

        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.terminal)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.startBtn)
        # self.hbox.addWidget(self.stopBtn)

        self.vbox.addLayout(self.hbox)

        self.wid.setLayout(self.vbox)
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Speech Final Project')    
        self.show()

    def start(self):
        self.rb.start()
        self.loop()
    
    def loop(self):
        # self.terminal.append('Recording...')
        audios = self.asr.listen()
        # self.terminal.append('Detecting...')
        for audio in audios:
            audio.export('test.wav')
            self.asr.noise_cancel()
            command = self.asr.asr()
            if command == 'drop':
                # self.terminal.append('Dropping object...')
                self.rb.dropObject()
            else:
                # self.terminal.append('Picking {} up...'.format(command))
                self.rb.pickup(command)
        self.loop()
        
    def stop(self):
        self.rb.stop()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    itf = Interface()
    sys.exit(app.exec_())