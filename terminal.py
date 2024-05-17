import os
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
 
from dark_pallete import darkPalette    # Импорт тёмной темы
from terminal_box import Terminal_Box   # Импорт класса Terminal_Box

from style import STYLES


# Текущая директория
basedir = os.path.dirname(__file__)

class Terminal(QMainWindow):
    """ Класс для Главного Окна """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Terminal")
        self.setMaximumSize(920, 650)
        self.setMinimumSize(920, 650)

        # Вертикальный лэйаут
        self.layout = QVBoxLayout()

        # Создвём экземпляр Terminal_Box, который является QPlainETextEdit для ввода команд
        self.terminal_box = None

        self.create_text_box()
        

        # Выравнивание виджетов по центру
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.layout.addWidget(self.terminal_box)

    def create_text_box(self) -> None:
        """ Функция для создания основного виджета для ввода команд """
        if self.terminal_box is not None:
            self.layout.removeWidget(self.terminal_box)
            self.terminal_box.deleteLater()  # Удаление старого виджета

        self.terminal_box = Terminal_Box(self)
        self.layout.addWidget(self.terminal_box)  # Добавление нового виджета в layout


# Вызов Основного цикла
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Установка стиля Fushion и тёмноы темы
    app.setStyle("Fusion")
    app.setPalette(darkPalette)

    terminal = Terminal()
    terminal.show()

    sys.exit(app.exec())
