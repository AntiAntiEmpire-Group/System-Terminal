""" Список команд для терминала """

import typing


def number_of_matches(entered_command:str, command:str) -> int:
    """ Метод на нахождения кол-во соответствий между введённой командой и имеющими командами """
    if len(entered_command) < len(command):
        return 0
    else:
        matches = 0
        
        for l1, l2 in zip(entered_command, command):
            if l1 == l2:
                matches += 1
        return matches

def find_right_command(entered_command: str) -> str:
    """ Метод, который предлгает пользователю верную команду, если он ошибся в её написание """
    idx = 0 # индекс команды в текущей итерации
    max_cmd_idx = len(TERMINAL_COMMAND_LIST.keys()) # максимально возможный индекс в словаре команд

    """ Начинаем с перебора ключей словаря команд """
    for command in TERMINAL_COMMAND_LIST.keys():
        
        if entered_command == command:
            return 
        
        # Вызываем метод на подсчёт совпадений
        mathes = number_of_matches(entered_command, command)
        
        idx += 1 

        if mathes + 1 == len(command) and len(entered_command) == len(command):
            """ Если колв-во (минимальное кол-во возможный совпадений) + 1 
                РАВНО длине команде на текущей итерации И длина введённой команды РАВНА длине команды на текущнй итерации,
                выдаём исключение о НЕИЗВЕСТНОЙ команды и предлагаем нужную команду"""
            return f"команда '{entered_command}' не найдена, вы имели ввиду:\n\команда '{command}.'"
        
        if mathes < len(command) and idx == max_cmd_idx:
            """ Если совпадений нет И все команды перебраны,
                то выдаём исключение о ПОЛНОСТЬЮ НЕИЗВЕСТНОЙ команды """
            return f"команда '{entered_command}' не найдена."
        
        if entered_command.startswith(command) or entered_command.endswith(command):
            """ Если в начале ИЛИ в конце введённой команды есть подстрока команды на текущеё итерации, 
                то выдаём исключение о НЕИЗВЕСТНОЙ команды и предлагаем нужную команду"""
            return f"команда '{entered_command}' не найдена, вы имели ввиду:\n\команда '{command}.'"
        
        elif mathes == 0:
            continue


TERMINAL_COMMAND_LIST = {
    "echo": "Отображает строку текста",
    "clear": "Очищает терминал",
    "help": "Вывод всех команд",
    "color": "Изменяет цветовую тему терминала",
}