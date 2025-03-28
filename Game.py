import xml.etree.ElementTree as ET
import random
import time
import os

class GameData:
    def __init__(self, game_name="Без названия", author="Неизвестный автор", trolleybuses=None, routes=None):
        self.game_name = game_name
        self.author = author
        self.trolleybuses = trolleybuses if trolleybuses else []
        self.routes = routes if routes else []

    @staticmethod
    def load_from_xml(file_path):
        if not os.path.exists(file_path): raise FileNotFoundError("XML файл не найден")

        tree = ET.parse(file_path)
        root = tree.getroot()
        game_data = GameData(game_name=root.findtext("GameName", "Без названия"), author=root.findtext("Author", "Неизвестный автор"))
        
        for t in root.find("Trolleybuses") or []:
            model = t.get("model", "Неизвестная модель")
            numbers = t.get("numbers", "").split(", ")
            game_data.trolleybuses.append(Trolleybus(model, numbers))

        for r in root.find("Routes") or []:
            name = r.get("name", "Без имени")
            stops = [s.text for s in r.findall("Stop")]
            game_data.routes.append(Route(name, stops))

        return game_data

class Trolleybus:
    def __init__(self, model, numbers):
        self.model = model
        self.numbers = numbers

class Route:
    def __init__(self, name, stops):
        self.name = name
        self.stops = stops

def main():
    global game_data, trolleybus_index, number_index, route_index, stop_index
    
    game_data = GameData.load_from_xml("gamedata.xml")
    os.system("cls" if os.name == "nt" else "clear")
    main_menu()

def main_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{game_data.game_name}\n\nГлавное меню:\n1. Начать игру\n2. О проекте\n3. Выход\n")
        select = input("Ваш выбор: ")
        if select == "1": set_game_parameters()
        elif select == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print(f"{game_data.game_name}\n\nАвтор основной игры: Костян Сигаев\nАвтор адаптации: {game_data.author}\n")
            input("Нажмите любую кнопку, чтобы вернуться в главное меню...")
        elif select == "3": exit()

def set_game_parameters():
    global trolleybus_index, number_index, route_index, stop_index
    os.system("cls" if os.name == "nt" else "clear")
    print("Для начала выберите троллейбус из списка:")
    for i, t in enumerate(game_data.trolleybuses, start=1): print(f"{i}) {t.model}")
    
    trolleybus_index = get_valid_index(len(game_data.trolleybuses))
    print(f"\nВы выбрали {game_data.trolleybuses[trolleybus_index].model}, теперь выберите бортовой номер:")
    for i, num in enumerate(game_data.trolleybuses[trolleybus_index].numbers, start=1): print(f"{i}) {num}")
    number_index = get_valid_index(len(game_data.trolleybuses[trolleybus_index].numbers))

    print("\nТеперь выберите маршрут:")
    for i, r in enumerate(game_data.routes, start=1): print(f"{i}) Маршрут №{r.name}: {len(r.stops)} остановок")
    route_index = get_valid_index(len(game_data.routes))
    
    print(f"\nВыбранные параметры: Троллейбус {game_data.trolleybuses[trolleybus_index].model} номер {game_data.trolleybuses[trolleybus_index].numbers[number_index]}, маршрут №{game_data.routes[route_index].name}")
    if input("Вы согласны? [Да | Нет]: ").strip().lower() == "да": game()
    else: set_game_parameters()

def get_valid_index(limit):
    try:
        index = int(input("Ваш выбор: ")) - 1
        return max(0, min(index, limit - 1))
    except ValueError: return random.randint(0, limit - 1)

def game():
    global stop_index
    stop_index = 0
    passengers_inside = 0
    passengers_total = 0
    
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(1)
    print("Начало игры...\nТроллейбус готовится...")
    time.sleep(1)
    print("Троллейбус выехал из депо...")
    time.sleep(1)
    print("Троллейбус подъехал к первой остановке...\n")
    time.sleep(1)
    
    while stop_index < len(game_data.routes[route_index].stops):
        print(f"Остановка: {game_data.routes[route_index].stops[stop_index]}\nПассажиров внутри: {passengers_inside}")
        print("1. Впустить/выпустить пассажиров\n2. Отправиться дальше\n3. Завершить рейс")
        
        action = input("Ваш выбор: ")
        if action == "1":
            print("Двери открываются")
            time.sleep(0.5)
            print("Пассажиры выходят и заходят")
            time.sleep(3)
            print("Двери закрываются")
            time.sleep(0.5)
            to_exit = random.randint(0, passengers_inside)
            to_enter = random.randint(0, 10)
            passengers_inside = max(0, passengers_inside - to_exit) + to_enter
            passengers_total += to_enter
            print(f"\nПассажиры вышли: {to_exit}, зашли: {to_enter}\n")
            time.sleep(1)
        elif action == "2":
            print("\nТроллейбус отправился...")
            time.sleep(3)
            print("Троллейбус подъехал к следующей остановке.\n")
            time.sleep(1)
            stop_index += 1
        elif action == "3": break
        else:
            print("\nТроллейбус отправился...")
            time.sleep(3)
            print("Троллейбус подъехал к следующей остановке.\n")
            time.sleep(1)
            stop_index += 1
    
    print(f"\nРейс окончен. Всего перевезено пассажиров: {passengers_total}\n")
    input("Нажмите любую кнопку, чтобы вернуться в меню...")
    main_menu()

if __name__ == "__main__":
    main()
