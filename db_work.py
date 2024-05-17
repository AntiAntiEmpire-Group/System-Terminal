""" Модуль для работы с базой данных """
import os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel


basedir = os.path.dirname(__file__) # директория в которой находится этот модуль


def connect_to_data_base() -> QSqlDatabase:
    """ Функция для установления подлючения с БД """
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(os.path.join(basedir, "src/main_db.sqlite"))
    if not db.open():
        raise Exception("Failed to open database")
    return db

def close_connection_with_data_base() -> None:
    """ Функция для закрытия подлючения с БД """
    db = QSqlDatabase.database("QSQLITE")
    db.close()
    QSqlDatabase.removeDatabase(os.path.join(basedir, "src/main_db.sqlite"))

def get_theme_index(db) -> int:
    """ Функция для получения текущего индекса темы """
    query = QSqlQuery(db=db)
    query.prepare("SELECT \"index\" FROM theme_index") # Запрос на получение индекса

    if not query.exec():
        raise Exception("Query failed: " + query.lastError().text())
    
    """ Если первая запись найдена """
    if query.first(): 
        # Получаем значение поля по индексу 0 (то есть, единственный столбец index)
        index_value = query.value(0)
        return index_value
    else:
        raise Exception("Data not found.")


def update_theme_index(db, index: int) -> None:
    """ Функция для обновления индекса цветовой темы """

    query = QSqlQuery(db=db)
    query.prepare("UPDATE theme_index SET \"index\" = :index")
    query.bindValue(":index", index)
    
    if not query.exec():
        raise Exception(f"Query failed: {query.lastError().text()}")
    print("Index updated successfully")

