import random
import sqlite3

import time

misha_bot_api = '5629818025:AAE3CAZFs6uhMcWZodFUdpKhSJu5awmGK_o'
poke_bot_api = "6831587612:AAEUQ4m30-Pajetdnw0AwZ4omaNmzVkc-4o"


def pokemon_catch():  # возвращает рандомное имя покемона в зависимости от их вероятности выпадения
    dictio = {'0': ['Хуйлуша'],  # key - веротность выпаения покемона, value -  list с именами покемонов
              '10': ['Pikachu'],
              '0': ['Лох'],        # вероятности должны в сумме давать 100
              '40': ['Squirtle', 'Bulbasaur'],
              '50': ['Charmander'], }
    rand_num = random.randint(1, 100)
    counter = 0
    for key in dictio:
        counter += int(key)
        if counter >= rand_num:
            pokemon_name = random.choice(dictio[key])
            return pokemon_name

def create_users_table():
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(50))')
    conn.commit()
    conn.close()

# def update_number_of_pokemons_table():
#     conn = sqlite3.connect('pokedex.sql')
#     cur = conn.cursor()
#     try:
#         cur.execute('ALTER TABLE number_of_pokemons ADD COLUMN pokebol INTEGER DEFAULT 5')
#     except sqlite3.OperationalError:
#         pass  # Столбец уже существует
#     conn.commit()
#     conn.close()
    
def create_captured_pokemons_table():
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS captured_pokemons (
        user_id INTEGER,
        found_pokemon VARCHAR(20),
        captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    conn.commit()
    conn.close()

def create_number_of_pokemons(): #таблица для учета количества покемонов у каждого юзера
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    pokemon_list = ['pikachu', 'squirtle', 'bulbasaur', 'charmander'] #создает таблицу с покемонами из этого листа
    text = "CREATE TABLE IF NOT EXISTS number_of_pokemons (user_id INTEGER, last_access_date VARCHAR(12) DEFAULT '10/12/15', pokebols INTEGER DEFAULT 5, "
    for item in pokemon_list:
        text += f'{item} INTEGER DEFAULT 0,'
    text = text.rstrip(',') + ")"
    cur.execute(text)
    conn.commit()
    conn.close()

def add_user_to_number_of_pokemons(user_id):  #добавляет только новых юзеров
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    check = cur.execute(f'SELECT * FROM number_of_pokemons WHERE user_id = {user_id}')
    if check.fetchone() is None:
        cur.execute(f"INSERT INTO number_of_pokemons (user_id) VALUES ({user_id})")

    conn.commit()
    conn.close()

def capture_pokemon(user_id, found_pokemon): #добавляет название покемона в таблицу с временами когда словил покемона и таблицу с количеством словленных покемонов
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    # Проверяем количество pokebols у пользователя
    cur.execute(f'SELECT pokebols FROM number_of_pokemons WHERE user_id = {user_id}')
    pokebol_count = cur.fetchone()[0]

    if pokebol_count > 0:
        found_pokemon = found_pokemon.lower()
        # Выполняем логику захвата
        cur.execute("INSERT INTO captured_pokemons (user_id, found_pokemon) VALUES (?, ?)", (user_id, found_pokemon))
        cur.execute(f"UPDATE number_of_pokemons SET {found_pokemon} = {found_pokemon} + 1, pokebols = pokebols - 1 WHERE user_id = {user_id}")
        conn.commit()
        success = True
    else:
        success = False

    conn.close()
    return success


def show_capture_time(user_id): #показывает время когда словил каждого покемона
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM captured_pokemons WHERE user_id = {user_id}')
    info = cur.fetchall()
    pokedex = ''
    for el in info:
    # Убедитесь, что здесь правильно форматируете строку, например:
        pokedex += f"Pokemon: {el[1]}, Captured At: {el[2]}\n"
    cur.close()
    conn.close()
    return pokedex

def show_pokedex(user_id): #показывает количество всех покемонов
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM number_of_pokemons WHERE user_id = {user_id}')
    pokemons = cur.fetchone()
    text = f"""You have:
Pokebols: {pokemons[2]}
Pikachu: {pokemons[3]}
Squirtle: {pokemons[4]}
Bulbasaur: {pokemons[5]}
Charmander: {pokemons[6]}
"""
    cur.close()
    conn.close()
    return text

def add_pokebols(user_id, amount):
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute(f"UPDATE number_of_pokemons SET pokebols = pokebols + {amount} WHERE user_id ={user_id}")
    conn.commit()
    conn.close()

def pokebols_number(user_id):
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT pokebols from number_of_pokemons where user_id ={user_id}')
    number = int(cur.fetchone()[0])
    cur.close()
    conn.close()
    return number


#проверяет последнюю дату запроса юзера на получение покеболов, и если это новый день, дает разрешение и перезаписывает дату
def check_pokebols_elegibility(user_id):
    conn = sqlite3.connect('pokedex.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT last_access_date from number_of_pokemons where user_id ={user_id}')
    date = cur.fetchone()[0]
    current_date = time.strftime("%d/%m/%y")
    if date == current_date:
        can_get_pokemons = False
    else:
        can_get_pokemons = True
        cur.execute(f"UPDATE number_of_pokemons SET last_access_date = '{current_date}' WHERE user_id ={user_id}")
        conn.commit()

    conn.close()
    return can_get_pokemons


if __name__ == "__main__":
    add_pokebols(668210174, 5)

    print(show_pokedex(668210174))



