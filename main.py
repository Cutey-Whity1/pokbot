import requests
from random import randint
from math import floor

class Pokemon:
    pokemons = {}  # Словарь для хранения покемонов

    def __init__(self, pokemon_trainer, num, lvl=5):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = num
        self.level = lvl
        self.img = self.get_img()
        self.name = self.get_name()
        self.stats = self.update_stats()

        Pokemon.pokemons[pokemon_trainer] = self  # Сохраняем покемона в словарь

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['other']['official-artwork']['front_default']
        return "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png"

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        return "Pikachu"

    def update_stats(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        stats = {}
        
        if response.status_code != 200:
            return stats  # Возвращаем пустой словарь, если API не ответило

        data = response.json()
        for stat_data in data['stats']:
            iv = randint(1, 31)
            stat_name = stat_data['stat']['name']
            base_stat = stat_data['base_stat']
            effort = stat_data['effort']

            if stat_name == 'hp':
                power = floor(0.01 * (2 * base_stat + iv + floor(0.25 * effort)) * self.level) + self.level + 10
            else:
                power = floor(0.01 * (2 * base_stat + iv + floor(0.25 * effort)) * self.level) + 5

            stats[stat_name] = {
                'power': power,
                'effort': effort
            }
        return stats
                        

    # метод для аттаки другиз покемонов
    def attack():
        pass

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img



class Wizard(Pokemon):
    pass


class Fighter(Pokemon):
    
    #статы покемончика
    def __init__(self):
    self.stats = {"atk": 10, "def": 8, "SPatk": 10, "SPdef": 8, "spd": 12, "tch": 13, "hlt": 30}
    #жестк функция атаки покемончика
    def attack(self,atk):
        #статовая атака
        if atk.type == 0:
            #Перебираем изменения атаки
            for i in atk.changes:
                #Статы изменения статов :P
                atk_stat_type = atk.changes[i][1]
                atk_stat_change = atk.changes[i][2]
                #Проверяем кому отправлены изменения
                if atk.changes[i][0] == 0:
                    self.stats[atk_stat_type] += atk_stat_change
                else:
                    enemy.stats[atk_stat_type] += atk_stat_change                    

        else:
            if not atk.sp:
                enemy.stats["hlt"] -= (atk.pow / 10 * self.stats["atk"]) - enemy.stats.["def"] / 2
            else:
                enemy.stats["hlt"] -= (atk.pow / 10 * self.stats["atk"]) - enemy.stats["SPdef"] / 1.8
