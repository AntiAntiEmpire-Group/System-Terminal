""" Модуль, содержащий функции для форматирования текста """

import typing
import os
import sys

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeyEvent, QTextCharFormat, QColor
from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QLayout
)


from settings import *
from style import STYLES
from main_text import (
    MAIN_TEXT, 
    SYS_TERM_VER,
    CURSOR_TEXT
)

from db_work import (
    connect_to_data_base,
    get_theme_index,
    update_theme_index,
    close_connection_with_data_base,
)


def set_theme(index: int, text_box: QPlainTextEdit) -> None:
    """ Устанавливаем цветовую тему"""

    if 0 <= index < len(THEMES):
        """ Подключаемся к БД """
        db = connect_to_data_base()

        update_theme_index(db, index)   
        theme_idx = get_theme_index(db) 
        text_box.setStyleSheet(STYLES[theme_idx])

        close_connection_with_data_base()

        # Обновляем тему
        currect_format(text_box)
        
        text_box.repaint()
        text_box.update()
        text_box.appendPlainText(CURSOR_TEXT)

    else:
        print("Неверный цветовой индекс")

def get_color(key: str) -> QColor:
    """ Возвращает индекс текущй цветовой темы """
    db = connect_to_data_base()

    theme_idx = get_theme_index(db)

    close_connection_with_data_base()

    return QColor(THEMES[theme_idx].get(key))

def currect_format(text_box: QPlainTextEdit) -> None:
    """ Изменяет вид текста на стандартный """
    format = QTextCharFormat()
    format.setForeground(get_color('DEFAULT_TEXT_COLOR'))
    text_box.setCurrentCharFormat(format)

def error_format(text_box: QPlainTextEdit) -> None:
    """ Apply the error text format """
    format = QTextCharFormat()
    format.setForeground(get_color('DEFAULT_ERROR_TEXT_COLOR'))
    text_box.setCurrentCharFormat(format)

def info_format_1(text_box: QPlainTextEdit) -> None:
    """ Apply the turquoise info text format """
    format = QTextCharFormat()
    format.setForeground(get_color('DEFAULT_INFO_TEXT_COLOR_1'))
    text_box.setCurrentCharFormat(format)

def info_format_2(text_box: QPlainTextEdit) -> None:
    """ Apply the violet info text format """
    format = QTextCharFormat()
    format.setForeground(get_color('DEFAULT_INFO_TEXT_COLOR_2'))
    text_box.setCurrentCharFormat(format)

