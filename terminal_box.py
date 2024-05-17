import os
import sys
import typing

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QFontDatabase, QFont
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import (
    QPlainTextEdit
)

from db_work import (
    connect_to_data_base,
    get_theme_index,
    close_connection_with_data_base,
)

from style import STYLES # Импорт строки стиля

from terminal_commands import ( # ИМпорт методов исполнения терминальных команд
    terminal_echo, 
    terminal_clear,
    terminal_help,
    terminal_color,
)

from text_formats import ( # Импорт метод изменения вида текста
    error_format, 
    currect_format,
    info_format_1,
    info_format_2,
) 

from terminal_command_list import ( # Импорт списка команд терминала и методы на поиск совпадений в списке команд
    TERMINAL_COMMAND_LIST, 
    find_right_command
)

from main_text import (
    MAIN_TEXT, 
    SYS_TERM_VER,
    CURSOR_TEXT
)


basedir = os.path.dirname(__file__) # Текущая директория



class Terminal_Box(QPlainTextEdit):
    """ Класс, описывающий поведение ввода текста в терминале """
    def __init__(self, parent=None):
        super().__init__()

        """ Установка соединения с БД и получение текущий индекс цветовой темы """
        db = connect_to_data_base()    

        self.model = QSqlTableModel(db=db)
        self.model.setTable("theme_index")
        self.model.select()
        self.theme_index = get_theme_index(db)
        close_connection_with_data_base()
 
        """ Загрузка шрифта """
        font_id = QFontDatabase.addApplicationFont(os.path.join(basedir, "src/fonts/Better VCR 6.1.TTF"))
        if font_id < 0: print("Error to load font")
        families = QFontDatabase.applicationFontFamilies(font_id) # Список семейства шрифта

        self.setFont(QFont(families[0])) # Установка шрифта

        self.setObjectName("terminal_box") # Установка имени для класса, для стилизования
        self.setStyleSheet(STYLES[int(self.theme_index)]) # Установка стиля
        self.setOverwriteMode(True) # Это свойство определяет, будет ли текст, введенный пользователем, перезаписывать существующий текст
        self.appendPlainText(MAIN_TEXT)
        self.appendPlainText(f"{CURSOR_TEXT}{SYS_TERM_VER}") # Вставка абзаца с текстом в конец
        self.appendPlainText(CURSOR_TEXT) # Вставка абзаца с курсором обычного пользователя в конец

        self.number_of_last_line = self.blockCount()


    def get_last_line(self) -> str:
        """ Функция, возвращающая самую крайнюю(последнюю) строку """

        text = self.toPlainText()  
        lines = text.splitlines()       
        if lines:   # Если текст есть                   
            return lines[-1]            
        return ""                       
    

    def dragMoveEvent(self, e):
        """ Запрещает пользователю перемещать выделенный текст """
        e.ignore()


    def keyPressEvent(self, e: QKeyEvent) -> None:
        """ Метод, вызывающийся при нажатии клавиш """
        cursor = self.textCursor() # Курсор

        cursor_position = self.textCursor().position() # Текущая позиция курсора
        text = self.toPlainText() # ВЕСЬ текст в Terminal_Box

        last_prompt_index = text.rfind(CURSOR_TEXT) + len(CURSOR_TEXT) # Нахождение самого БОЛЬШОГО индекса вхождения обычного курсора
        
        """ Если позиция курсора это '*> {position}' 
            Например:
            *> 
               ^
               |
                ----- Здесь курсор"""
        if cursor_position < last_prompt_index:
            """ Если позиция курсора меньше последнего приглашения по ввод, и если нажата любая клавиша, то НИЧЕГО не происходит """
            if e.key():
                return
        
        """ Если позиция курсора РАВНА последнему приглашению на ввод И нажаты клавиши Backspace, Delete, то ничего не происходит. """
        if cursor_position == last_prompt_index and e.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            return

        """ Если пользователь выделил текст, то он не может его удалить """
        if cursor.hasSelection():
            if e.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
                return
        
        """ При нажатии на Return(Enter) """
        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            last_line = self.get_last_line() # Получаем последнюю строку

            """ Если ничего не введено, то происходит переход на новую строку с добавлением символа обычного курсора """
            if last_line == CURSOR_TEXT:
                self.appendPlainText(CURSOR_TEXT)
            else:
                """ Иначе, если что-то введено, то мы вводим переменную command и список args
                    Пояснения:

                    command = строка введённой команды
                    >> last_line.strip().split() = ['> ', 'echo', 'hello']
                    >> command = last_line.strip().split()[1] = 'echo'

                    args = список аргументов
                    >> last_line.strip().split() = ['> ', 'echo', 'hello,', 'world!']
                    >> args = last_line.strip().split()[2:] = ['hello,', 'world!']
                 """
                command = last_line.strip().split()[1]
                args = last_line.strip().split()[2:] if len(last_line.strip().split()) > 1 else []

                """ Выполнение команды echo """
                if command == list(TERMINAL_COMMAND_LIST.keys())[0]:
                    terminal_echo(self, " ".join(args))

                """ Выполнение команды clear """
                if command == list(TERMINAL_COMMAND_LIST.keys())[1]:
                    terminal_clear(self)

                """ Выполнение команды help """
                if command == list(TERMINAL_COMMAND_LIST.keys())[2]:
                    terminal_help(self, TERMINAL_COMMAND_LIST)

                """ Для команды color """
                if command == list(TERMINAL_COMMAND_LIST.keys())[3]:
                    if len(args) == 0:
                        error_format(self)
                        self.appendPlainText("'color' должен принимать флаг!\nНапример: color 2")
                        currect_format(self)
                        self.appendPlainText(CURSOR_TEXT)
                    else:
                        terminal_color(self, args[0])

                """ Если команда нет в списке, то выводится ошибка """
                if command not in list(TERMINAL_COMMAND_LIST.keys()):
                    info_format_1(self)
                    self.appendPlainText(find_right_command(command))
                    currect_format(self)
                    self.appendPlainText(CURSOR_TEXT)        

            """ В других случаях, просто продолжается ввод текста """
        else:
            super().keyPressEvent(e)

            
