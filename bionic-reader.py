
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QDesktopWidget, QLabel, QScrollArea, QAction, QWidget,
                              QSizePolicy, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit )
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from sys import argv, exit
from re import split


WIN_SIZE = (600, 650)
FONT = 'verdana'
FONT_SIZE = 14


p = 'asset\\'
separators_str = r'([,:\s\n;.\-(){}\[\]])'
separators = [':', ',', ';', '.', '-', '{', '}', '(', ')', '[', ']', '<br>']

default_text = ('This is a bionic reader tool.\n'
                'Enter text with the command shell or open a file '
                'to make the first letters of each words bolds and speed up your reading time.')


class AboutPanel(QDialog):
    def __init__(self):
        super().__init__(window)
        self.setWindowTitle('About')
        self.setWindowIcon(QIcon(p+'about.png'))
        self.setFixedSize(470, 260)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(
            'This is a bionic reader tool python implementation made by g_Bloxy.\n'
            ))
        layout.addWidget(QLabel((
            'To make text bionic readable, click on the write button and input you text\nwith the console '
            'or click on the open file button to import a basic .txt file.\n'
            'Click on the remove button to reset the text.\n'
            )))
        layout.addWidget(QLabel((
            'Licence : This software is open source and licensed under the MIT licence, '
            'so\nyou can make anything with it. See the licence file for details.'
            )))
        layout.addWidget(QLabel(
            'Credits : icons from Carbon Design System by IBM under Apache Licence 2.0\n'
            ))
        github_link = QLabel(
            'Github link : <a href=\"https://github.com/gBloxy/Bionic-Reader">gBloxy/Bionic-Reader</a>'
            )
        github_link.setOpenExternalLinks(True)
        layout.addWidget(github_link)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button = QPushButton('close', self)
        button.clicked.connect(self.close)
        button_layout.addWidget(button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


class InputPanel(QDialog):
    def __init__(self):
        super().__init__(window)
        self.setWindowTitle('Text input')
        self.setWindowIcon(QIcon(p+'write.png'))
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        
        self.editor = QTextEdit(self)
        self.editor.setAcceptRichText(False)
        
        layout.addWidget(self.editor)
        
        yes_button = QPushButton('ok', self)
        yes_button.clicked.connect(self.accept)
        cancel_button = QPushButton('cancel', self)
        cancel_button.clicked.connect(self.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_text(self):
        return self.editor.toPlainText()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bionic Reader')
        self.setGeometry(SCREEN_SIZE[0]//2 - WIN_SIZE[0]//2, SCREEN_SIZE[1]//2 - WIN_SIZE[1]//2, *WIN_SIZE)
        self.setWindowIcon(QIcon(p+'book.png'))
        
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
        self.Ac_remove = QAction(QIcon(p+'delete.png'), '&Remove', shortcut='Ctrl+r')
        self.Ac_about = QAction(QIcon(p+'about.png'), 'A&bout', shortcut='Alt+a')
        self.Ac_quit = QAction(QIcon(p+'exit.png'), '&Quit', shortcut='Alt+q')
    
    def linkActions(self):
        self.Ac_write.triggered.connect(self.write)
        self.Ac_open.triggered.connect(self.from_file)
        self.Ac_remove.triggered.connect(lambda: self.set_text(default_text))
        self.Ac_about.triggered.connect(lambda: AboutPanel().show())
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
        words = split(separators_str, text)
        words = [w.replace('\n', '<br>') for w in words]
        formatted = ''
        
        for w in words:
            if w in separators or w.isspace() or w == '':
                formatted += w
            
            else:
                size = len(w)
                
                if size <= 3:
                    bold_nb = 1
                elif size == 4:
                    bold_nb = 2
                else:
                    bold_nb = round(size * 0.4)
                
                formatted += '<b>' + w[:bold_nb] + '</b>' + w[bold_nb:]
        
        self.label.setText(formatted)
    
    def write(self):
        dialog = InputPanel()
        
        if dialog.exec():
            text = dialog.get_text()
            
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


if __name__ == '__main__':
    app = QApplication(argv)
    
    screen = QDesktopWidget().screenGeometry()
    SCREEN_SIZE = (screen.width(), screen.height())
    
    window = Window()
    window.set_text(default_text)
    window.show()
    
    exit(app.exec())
