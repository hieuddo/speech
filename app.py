from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtGui
import sys
from voice import ASR
from robot import Robot
from pydub import AudioSegment, silence

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.run = False
        self.initUI()
    
    def initUI(self):
        self.terminal = QTextEdit(self)
        
        self.terminal.setFixedSize(300, 260)
        self.terminal.setReadOnly(True)
        self.terminal.setText('Test')

        self.startBtn = QPushButton()
        self.startBtn.setFixedSize(32,32)
        self.startBtn.setIcon(QtGui.QIcon('button/start.png'))
        # self.startBtn.clicked.connect(self.start)
        
        self.stopBtn = QPushButton()
        self.stopBtn.setFixedSize(32,32)
        self.stopBtn.setIcon(QtGui.QIcon('button/stop.png'))
        # self.stopBtn.clicked.connect(self.stop)

        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.terminal)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.startBtn)
        self.hbox.addWidget(self.stopBtn)

        self.vbox.addLayout(self.hbox)

        self.wid.setLayout(self.vbox)
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Speech Final Project')    
        self.show()

    def start(self, rb, asr):
        while 1:
            asr.record_sound('record.wav', duration=5)
            myaudio = AudioSegment.from_wav('record.wav')
            audios = silence.split_on_silence(myaudio, min_silence_len=300, silence_thresh=-32, keep_silence=400)
            for audio in audios:
                # print('Detecting...')
                self.terminal.append('Detecting...')
                # itf.terminal.append('Detecting...')
                audio.export('test.wav')
                asr.noise_cancel()
                command = asr.asr()
                if command == 'drop':
                    # print('Dropping object...')
                    self.terminal.append('Dropping object...')
                    rb.dropObject()
                else:
                    # print('Picking {} up...'.format(command))
                    self.terminal.append('Picking {} up...'.format(command))
                    rb.pickup(command)

    def stop(self):
        self.terminal.append('Stop')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    itf = Interface()
    rb = Robot()
    asr = ASR()
    itf.startBtn.clicked.connect(itf.start(rb, asr))
    # itf.startBtn.clicked.connect(itf.start)
    sys.exit(app.exec_())