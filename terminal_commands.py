""" Модуль содержащий команды для терминала """

import typing
import os
import sys

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget
)

from text_formats import ( # Импорт метод изменения вида текста
    error_format, 
    currect_format,
    info_format_1,
    info_format_2,
    set_theme,
) 

from main_text import (
    MAIN_TEXT, 
    SYS_TERM_VER,
    CURSOR_TEXT
)

from db_work import (
    connect_to_data_base,
    get_theme_index,
    close_connection_with_data_base,
)

from style import INFO_ABOUT_THEMES

# Курсор обычного пользователя
from main_text import CURSOR_TEXT

def terminal_echo(text_box: QPlainTextEdit, string: str) -> None:
    """ Команда на вывод string в терминал
        Например:
    >>  echo hello, world!
    >>  hello, world!
       """
    if string:
        text_box.appendPlainText(string)
        text_box.appendPlainText(CURSOR_TEXT)
    else:
        error_format(text_box) # Изменение йвета текста на красный
        text_box.appendPlainText("'echo' должна принимать строку как параметр!\nНапример: echo привет, мир!")
        currect_format(text_box)
        text_box.appendPlainText(CURSOR_TEXT) # Изменение йвета текста на стандартный


def terminal_clear(text_box: QPlainTextEdit) -> None:
    """ Команда на очистку терминала """
    text_box.clear()
    text_box.appendPlainText(MAIN_TEXT)
    text_box.appendPlainText(f"{CURSOR_TEXT}{SYS_TERM_VER}")
    text_box.appendPlainText(CURSOR_TEXT)


def terminal_help(text_box: QPlainTextEdit, term_com_list: list) -> None:
    """ Команда для отображение всех команд """
    for command in term_com_list:

        info_format_1(text_box) # Изменение цвета текста на голубой
        text_box.appendPlainText(f"{command}: ")
        currect_format(text_box) # Изменение цвета текста на стандартный

        info_format_2(text_box) # Изменение йвета текста на другой голубой
        text_box.insertPlainText(f"{term_com_list.get(command)}")
        currect_format(text_box)

    text_box.appendPlainText(CURSOR_TEXT)


def terminal_color(text_box: QPlainTextEdit, flag: str) -> None:
    """ Команда на смену цветовой темы терминала """
    allow_flags = ['0', '1', '2', '-i']
    
    # Получение информации и о текущем стиле
    if flag == '-i':
        """ Подключаемся к БД и получаем текущий индекс """
        db = connect_to_data_base()

        theme_idx = get_theme_index(db)
        text_box.appendPlainText(f"Текущая цветовая тема: {INFO_ABOUT_THEMES[theme_idx]}")
        text_box.appendPlainText(CURSOR_TEXT)

        close_connection_with_data_base()
        return

    # Если флага не существует, то говорим об этом
    if flag not in allow_flags:
        error_format(text_box)
        text_box.appendPlainText("Неизвестный флаг")
        currect_format(text_box)
        text_box.appendPlainText(CURSOR_TEXT)

    # Устанавливаем тему
    else:
        set_theme(int(flag), text_box)
        
        
