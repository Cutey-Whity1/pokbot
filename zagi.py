import requests
from typing import Dict, List, Optional

class PokemonAPI:
    """
    Класс для получения информации о покемонах через PokeAPI.
    
    Основные методы:
        get_pokemon_info - получает полную информацию о покемоне
        get_image_url - получает URL изображения покемона
        get_abilities - получает список способностей
        get_stats - получает характеристики покемона
    """
    
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon/"
    
    def _make_request(self, pokemon_identifier: str) -> Optional[Dict]:
        """
        Внутренний метод для выполнения HTTP-запроса к API.
        
        Args:
            pokemon_identifier: Имя или номер покемона
            
        Returns:
            Словарь с данными покемона или None при ошибке
        """
        try:
            response = requests.get(f"{self.base_url}{pokemon_identifier.lower()}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: Покемон '{pokemon_identifier}' не найден (код {response.status_code})")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None
    
    def get_pokemon_info(self, pokemon_identifier: str) -> Optional[Dict]:
        """
        Получает полную информацию о покемоне.
        
        Args:
            pokemon_identifier: Имя или номер покемона (например, 'pikachu' или '25')
            
        Returns:
            Словарь с информацией о покемоне в формате:
            {
                'id': номер покемона,
                'name': имя,
                'image_url': URL изображения,
                'abilities': список способностей,
                'stats': словарь характеристик,
                'height': рост,
                'weight': вес,
                'types': список типов
            }
            или None, если покемон не найден
        """
        data = self._make_request(pokemon_identifier)
        if not data:
            return None
        
        # Формируем информацию о покемоне
        pokemon_info = {
            'id': data['id'],
            'name': data['name'].capitalize(),
            'image_url': data['sprites']['other']['official-artwork']['front_default'],
            'abilities': [ability['ability']['name'] for ability in data['abilities']],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'height': data['height'] / 10,  # Переводим в метры
            'weight': data['weight'] / 10,  # Переводим в кг
            'types': [t['type']['name'] for t in data['types']]
        }
        
        return pokemon_info
    
    def get_image_url(self, pokemon_identifier: str) -> Optional[str]:
        """
        Получает URL официального изображения покемона.
        
        Args:
            pokemon_identifier: Имя или номер покемона
            
        Returns:
            URL изображения или None, если покемон не найден
        """
        data = self._make_request(pokemon_identifier)
        if not data:
            return None
        return data['sprites']['other']['official-artwork']['front_default']
    
    def get_abilities(self, pokemon_identifier: str) -> Optional[List[str]]:
        """
        Получает список способностей покемона.
        
        Args:
            pokemon_identifier: Имя или номер покемона
            
        Returns:
            Список способностей или None, если покемон не найден
        """
        data = self._make_request(pokemon_identifier)
        if not data:
            return None
        return [ability['ability']['name'] for ability in data['abilities']]
    
    def get_stats(self, pokemon_identifier: str) -> Optional[Dict[str, int]]:
        """
        Получает характеристики покемона.
        
        Args:
            pokemon_identifier: Имя или номер покемона
            
        Returns:
            Словарь с характеристиками в формате {'hp': 45, 'attack': 49, ...}
            или None, если покемон не найден
        """
        data = self._make_request(pokemon_identifier)
        if not data:
            return None
        return {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    
    def print_pokemon_info(self, pokemon_identifier: str):
        """
        Выводит основную информацию о покемоне в читаемом формате.
        """
        info = self.get_pokemon_info(pokemon_identifier)
        if not info:
            print(f"Не удалось получить информацию о покемоне '{pokemon_identifier}'")
            return
        
        print(f"\n=== Информация о покемоне ===")
        print(f"ID: {info['id']}")
        print(f"Имя: {info['name']}")
        print(f"Тип(ы): {', '.join(info['types'])}")
        print(f"Рост: {info['height']} м")
        print(f"Вес: {info['weight']} кг")
        print("\nСпособности:")
        for ability in info['abilities']:
            print(f"- {ability}")
        
        print("\nХарактеристики:")
        for stat, value in info['stats'].items():
            print(f"- {stat}: {value}")
        
        print(f"\nИзображение: {info['image_url']}")