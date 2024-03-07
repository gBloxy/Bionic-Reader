
from sys import argv, exit
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QDesktopWidget, QLabel, QScrollArea, QAction, QWidget,
                             QSizePolicy, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QPushButton )
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


WIN_SIZE = (900, 800)
FONT = 'verdana'
FONT_SIZE = 15

p = 'asset\\'
default_text = 'This is a bionic reader tool. Enter text with the command shell to make the first letters of each words bolds and speed up your reading time.'


class AboutPanel(QDialog):
    def __init__(self):
        super().__init__(window)
        self.setWindowTitle('About')
        layout = QVBoxLayout()
        
        label = QLabel('test', self)
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()
        button_layout.addSpacing(QSizePolicy.Expanding)
        button = QPushButton('close', self)
        button.clicked.connect(self.close)
        button_layout.addWidget(button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bionic Reader')
        self.setGeometry(SCREEN_SIZE[0]//2 - WIN_SIZE[0]//2, SCREEN_SIZE[1]//2 - WIN_SIZE[1]//2, *WIN_SIZE)
        
        self.createActions()
        self.linkActions()
        self.createToolbar()
        
        label = QLabel(self)
        label.setAlignment(Qt.AlignTop)
        label.setMargin(30)
        label.setFont(QFont(FONT, FONT_SIZE))
        label.setWordWrap(True)
        self.label = label
        
        scrollarea = QScrollArea(self)
        scrollarea.setWidgetResizable(True)
        scrollarea.setWidget(label)
        
        self.setCentralWidget(scrollarea)
    
    def createActions(self):
        self.Ac_write = QAction(QIcon(p+'write.png'), '&Write', shortcut='Ctrl+w')
        self.Ac_open = QAction(QIcon(p+'open.png'), '&Open', shortcut='Ctrl+o')
        self.Ac_remove = QAction(QIcon(p+'delete.png'), '&Remove', shortcut='Ctrl+d')
        self.Ac_about = QAction(QIcon(p+'about.png'), 'A&bout', shortcut='Ctrl+h')
        self.Ac_quit = QAction(QIcon(p+'exit.png'), '&Quit', shortcut='Alt+q')
    
    def linkActions(self):
        self.Ac_write.triggered.connect(self.write)
        self.Ac_open.triggered.connect(self.from_file)
        self.Ac_remove.triggered.connect(lambda: self.set_text(default_text))
        self.Ac_about.triggered.connect(self.about)
        self.Ac_quit.triggered.connect(self.close)
    
    def createToolbar(self):
        toolbar = self.addToolBar('toolbar')
        toolbar.setMovable(False)
        toolbar.addAction(self.Ac_write)
        toolbar.addAction(self.Ac_open)
        toolbar.addAction(self.Ac_remove)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, 0)
        toolbar.addWidget(spacer)
        
        toolbar.addAction(self.Ac_about)
        toolbar.addAction(self.Ac_quit)
        
        self.addToolBar(toolbar)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def set_text(self, text: str):
        # text = text.replace('\n', '<br>')
        words = text.split()
        formatted = '<html>'
        
        for w in words:
            # if w.isalpha():
                size = len(w)
                
                if size <= 3:
                    bold_nb = 1
                elif size == 4:
                    bold_nb = 2
                else:
                    bold_nb = round(size * 0.4)
                
                formatted += '<b>'
                for l in range(bold_nb):
                    formatted += w[l]
                formatted += '</b>'
                
                for l in range(bold_nb, size):
                    formatted += w[l]
            # else:
            #     formatted += w
            
                formatted += ' '
        
        formatted += '</html>'
        self.label.setText(formatted)
    
    def write(self):
        text = str(input('enter text : '))
        if text.isspace() or text == '':
            text = default_text
        self.set_text(text)
    
    def from_file(self):
        path = QFileDialog().getOpenFileName()[0]
        if not (path.isspace() or path == ''):
            with open(path, 'r') as file:
                text = file.read()
            if text.isspace() or text == '':
                text = default_text
        else:
            text = default_text
        self.set_text(text)
    
    def about(self):
        panel = AboutPanel()
        panel.show()


if __name__ == '__main__':
    app = QApplication(argv)
    
    screen = QDesktopWidget().screenGeometry()
    SCREEN_SIZE = (screen.width(), screen.height())
    
    try:
        text = argv[1]
    except:
        text = default_text
    
    if text.isspace() or text == '':
        text = default_text * 5
    
    window = Window()
    window.set_text(text)
    window.show()
        
    exit(app.exec())
