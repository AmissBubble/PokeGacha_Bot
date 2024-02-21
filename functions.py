import random
import sqlite3

from datetime import datetime, timedelta
misha_bot_api = '5629818025:AAE3CAZFs6uhMcWZodFUdpKhSJu5awmGK_o'
poke_bot_api = "6831587612:AAEUQ4m30-Pajetdnw0AwZ4omaNmzVkc-4o"

pokemon_list = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'NidoranF', 'Nidorina', 'Nidoqueen', 'NidoranM', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetchd', 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mr_Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew']
rarity = {
          "E": ['Bellsprout', 'Caterpie', 'Diglett', 'Ekans', 'Exeggcute', 'Gastly', 'Goldeen', 'Horsea', 'Krabby', 'Magikarp', 'NidoranF', 'NidoranM', 'Oddish', 'Omanyte', 'Paras', 'Pidgey', 'Poliwag', 'Rattata', 'Shellder', 'Spearow', 'Weedle', 'Zubat'],
          "D": ['Abra', 'Clefairy', 'Dewgong', 'Doduo', 'Drowzee', 'Dugtrio', 'Geodude', 'Grimer', 'Growlithe', 'Kakuna', 'Koffing', 'Machop', 'Magnemite', 'Mankey', 'Meowth', 'Metapod', 'Pidgeotto', 'Psyduck', 'Sandshrew', 'Seel', 'Staryu', 'Tentacool', 'Venonat', 'Voltorb', 'Weepinbell'],
          "C": ['Beedrill', 'Bulbasaur', 'Chansey', 'Charmander', 'Cubone', 'Eevee', 'Electrode', 'Fearow', 'Gloom', 'Golbat', 'Graveler', 'Haunter', 'Jigglypuff', 'Jynx', 'Kadabra', 'Kingler', 'Nidorina', 'Nidorino', 'Omastar', 'Parasect', 'Persian', 'Pikachu', 'Pinsir', 'Poliwhirl', 'Ponyta', 'Raticate', 'Rhyhorn', 'Seaking', 'Slowpoke', 'Squirtle', 'Tangela', 'Venomoth', 'Vulpix'],
          "B": ['Arbok', 'Butterfree', 'Charmeleon', 'Clefable', 'Cloyster', 'Dodrio', 'Dratini', 'Electabuzz', 'Exeggutor', 'Golduck', 'Hitmonchan', 'Hitmonlee', 'Hypno', 'Ivysaur', 'Kabuto', 'Kangaskhan', 'Lapras', 'Lickitung', 'Machoke', 'Magmar', 'Magneton', 'Mr_Mime', 'Onix', 'Pidgeot', 'Poliwrath', 'Porygon', 'Primeape', 'Rapidash', 'Sandslash', 'Scyther', 'Seadra', 'Slowbro', 'Starmie', 'Tauros', 'Tentacruel', 'Victreebel', 'Vileplume', 'Wartortle', 'Weezing', 'Wigglytuff'],
          "A": ['Aerodactyl', 'Alakazam', 'Arcanine', 'Blastoise', 'Charizard', 'Dragonair', 'Farfetchd', 'Flareon', 'Gengar', 'Golem', 'Gyarados', 'Jolteon', 'Kabutops', 'Machamp', 'Marowak', 'Muk', 'Nidoking', 'Nidoqueen', 'Ninetales', 'Raichu', 'Rhydon', 'Snorlax', 'Vaporeon', 'Venusaur'],
          "S": ['Zapdos', 'Moltres', 'Mewtwo', 'Mew', 'Dragonite', 'Ditto', 'Articuno']
}

generations = {'Bellsprout': '', 'Caterpie': '', 'Diglett': '', 'Ekans': '', 'Exeggcute': '', 'Gastly': '', 'Goldeen': '', 'Horsea': '', 'Krabby': '', 'Magikarp': '', 'NidoranF': '', 'NidoranM': '', 'Oddish': '', 'Omanyte': '', 'Paras': '', 'Pidgey': '', 'Poliwag': '', 'Rattata': '', 'Shellder': '', 'Spearow': '', 'Weedle': '', 'Zubat': '', 'Abra': '', 'Clefairy': '', 'Dewgong': "Seel's evolution", 'Doduo': '', 'Drowzee': '', 'Dugtrio': "Diglett's evolution", 'Geodude': '', 'Grimer': '', 'Growlithe': '', 'Kakuna': "Weedle's 1'st evolution", 'Koffing': '', 'Machop': '', 'Magnemite': '', 'Mankey': '', 'Meowth': '', 'Metapod': "Caterpie's 1'st evolution", 'Pidgeotto': "Pidgey's 1'st evolution", 'Psyduck': '', 'Sandshrew': '', 'Seel': '', 'Staryu': '', 'Tentacool': '', 'Venonat': '', 'Voltorb': '', 'Weepinbell': "Bellsprout's 1'st evolution", 'Beedrill': "Weedle's 2'nd evolution", 'Bulbasaur': '', 'Chansey': '', 'Charmander': '', 'Cubone': '', 'Eevee': '', 'Electrode': "Voltorb's evolution", 'Fearow': "Spearow's evolution", 'Gloom': "Oddish's 1'st evolution", 'Golbat': "Zubat's evolution", 'Graveler': "Geodude's 1'st evolution", 'Haunter': "Gastly's 1'st evolution", 'Jigglypuff': '', 'Jynx': '', 'Kadabra': "Abra's 1'st evolution", 'Kingler': "Krabby's evolution", 'Nidorina': "NidoranF's 1'st evolution", 'Nidorino': "NidoranM's evolution", 'Omastar': "Omanyte's evolution", 'Parasect': "Paras's evolution", 'Persian': "Meowth's evolution", 'Pikachu': '', 'Pinsir': '', 'Poliwhirl': "Poliwag's 1'st evolution", 'Ponyta': '', 'Raticate': "Rattata's evolution", 'Rhyhorn': '', 'Seaking': "Goldeen's evolution", 'Slowpoke': '', 'Squirtle': '', 'Tangela': '', 'Venomoth': "Venonat's evolution", 'Vulpix': '', 'Arbok': "Ekan's evolution", 'Butterfree': "Caterpie's 2'nd evolution", 'Charmeleon': "Charmander's 1'st evolution", 'Clefable': "Clefairy's evolution", 'Cloyster': "Shellder's evolution", 'Dodrio': "Doduo's evolution", 'Dratini': '', 'Electabuzz': '', 'Exeggutor': "Exeggcute's evolution", 'Golduck': "Psyduck's evolution", 'Hitmonchan': '', 'Hitmonlee': '', 'Hypno': "Drowzee's evolution", 'Ivysaur': "Bulbasaur's 1'st evolution", 'Kabuto': '', 'Kangaskhan': '', 'Lapras': '', 'Lickitung': '', 'Machoke': "Machop's 1'st evolution", 'Magmar': '', 'Magneton': "Magnemite's evolution", 'Mr_Mime': '', 'Onix': '', 'Pidgeot': "Pidgey's 2'st evolution", 'Poliwrath': "Poliwag's 2'nd evolution", 'Porygon': '', 'Primeape': "Mankey's evolution", 'Rapidash': "Ponyta's evolution", 'Sandslash': "Sandshrew's evolution", 'Scyther': '', 'Seadra': "Horsea's evolution", 'Slowbro': "Slowpoke's evolution", 'Starmie': "Staryu's evolution", 'Tauros': '', 'Tentacruel': "Tentacool's evolution", 'Victreebel': "Bellsprout's 2'nd evolution", 'Vileplume': "Oddish's 2'nd evolution", 'Wartortle': "Squirtle's 1'st evolution", 'Weezing': "Koffing's evolution", 'Wigglytuff': "Jigglypuff's evolution", 'Aerodactyl': '', 'Alakazam': "Abra's 2'nd evolution", 'Arcanine': "Growlithe's evolution", 'Blastoise': "Squirtle's 2'nd evolution", 'Charizard': "Charmander's 2'nd evolution", 'Dragonair': "Dratini's 1'st evolution", 'Farfetchd': '', 'Flareon': "Eevee's evolution", 'Gengar': "Gastly's 2'nd evolution", 'Golem': "Geodude's 2'nd evolution", 'Gyarados': "Magikarp's evolution", 'Jolteon': "Eevee's evolution", 'Kabutops': "Kabuto's evolution", 'Machamp': "Machop's 2'nd evolution", 'Marowak': "Cubone's evolution", 'Muk': "Grimer's evolution", 'Nidoking': "NidoranM's evolution", 'Nidoqueen': "Nidorina's evolution", 'Ninetales': "Vulpix's evolution", 'Raichu': "Pikachu's evolution", 'Rhydon': "Rhyhorn's evolution", 'Snorlax': '', 'Vaporeon': "Eevee's evolution", 'Venusaur': "Bulbasaur's 2'nd evolution", 'Zapdos': '', 'Moltres': '', 'Mewtwo': '', 'Mew': '', 'Dragonite': "Dratini's 2'nd evolution", 'Ditto': '', 'Articuno': ''}

def pokemon_catch():  # возвращает рандомное имя покемона в зависимости от их вероятности выпадения
    dictio = {"E":'600',
              "D":'230',
              "C":'120',       # key - веротность выпаения покемона, value -  list с именами покемонов
              "B":'30',
              "A":'19',   # вероятности должны быть написаны целыми числами
              "S":'1'}



    rand_num = random.randint(1, 1000) # вероятности должны в сумме давать 1000
    counter = 0
    for key in dictio:
        counter += int(dictio[key])
        if counter >= rand_num:
            pokemon_name = random.choice(rarity[key])
            return pokemon_name, key

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

    text = "CREATE TABLE IF NOT EXISTS number_of_pokemons (user_id INTEGER, last_access_date VARCHAR(12) DEFAULT '10/12/15', pokebols INTEGER DEFAULT 5, "
    for item in pokemon_list:     #создаем таблицу с покемонами из этого листа, который был идентифицирован ранее
        text += f'{item.lower()} INTEGER DEFAULT 0,'
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
    text = f'You have:\nPokebols: {pokemons[2]}\n'
    for poke_count, pokemon_name in zip(pokemons[3:], pokemon_list):
        if poke_count > 0:
            text += f'{pokemon_name}: {poke_count}\n'

    #     text = f"""You have:
    # Pokebols: {pokemons[2]}
    # Pikachu: {pokemons[3]}
    # Squirtle: {pokemons[4]}
    # Bulbasaur: {pokemons[5]}
    # Charmander: {pokemons[6]}
    # """
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
    now = datetime.now()
    current_date = now.strftime("%d/%m/%y")
    if date == current_date:
        can_get_pokemons = False
    else:
        can_get_pokemons = True
        cur.execute(f"UPDATE number_of_pokemons SET last_access_date = '{current_date}' WHERE user_id ={user_id}")
        conn.commit()

    conn.close()
    return can_get_pokemons

def time_until_next_midnight():
    current_time = datetime.now()

    next_midnight = datetime(current_time.year, current_time.month, current_time.day) + timedelta(days=1)
    time_remaining = next_midnight - current_time

    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes = remainder // 60
    text = f'{hours} часов, {minutes+1} минут'

    return text


if __name__ == "__main__":
    print(show_pokedex(668210174))
    print(time_until_next_midnight())