""" Файл стиля """


import os
from PyQt6.QtGui import QFontDatabase, QFont
from settings import *

basedir = os.path.dirname(__file__)

DEAFULT_STYLE = f"""
    Terminal_Box#terminal_box {{
        font-size: 15px;
        color: {THEMES[0]['DEFAULT_TEXT_COLOR']};
        background-color: #000000;
        line-height: 40px;
        line-height: 20px;
    }}
"""

FIRST_THEME_STYLE = f"""
    Terminal_Box#terminal_box {{
        font-size: 15px;
        color: {THEMES[1]['DEFAULT_TEXT_COLOR']};
        background-color: #000000;
        line-height: 40px;
        line-height: 20px;
    }}
"""

SECOND_THEME_STYLE = f"""
    Terminal_Box#terminal_box {{
        font-size: 15px;
        color: {THEMES[2]['DEFAULT_TEXT_COLOR']};
        background-color: #000000;
        line-height: 40px;
        line-height: 20px;
    }}
"""

STYLES = [DEAFULT_STYLE, FIRST_THEME_STYLE, SECOND_THEME_STYLE]