import sqlite3

bd = sqlite3.connect('2048.sqlite')  # создаем базу даных
cur = bd.cursor()  # открываем

# создание бд
cur.execute('''
create table if not exists RECORDS (
name text,
score integer
)
''')


def insert_result(name, score):  # Вставляем результат в таблицу базы данных
    cur.execute("""
        insert into RECORDS values(?,?)
    """, (name, score))
    bd.commit()  # # сохраняем результат в таблицу базы данных


# выборка по бд
def get_best():
    cur.execute("""
    SELECT name gamer, max(score) score from RECORDS
    GROUP by name
    ORDER by score DESC
    LIMIT 3
    """)
    return cur.fetchall()

# cur.close()                         # закрываем
