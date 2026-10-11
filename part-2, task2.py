import json

teams = {
    "Динамо": 52,
    "Шахтар": 48,
    "Дніпро-1": 44,
    "Зоря": 39,
    "Ворскла": 35,
    "Олександрія": 31,
    "Колос": 27,
    "Металіст": 22,
    "Інгулець": 17
}

with open("teams.json", "w", encoding="utf-8") as f:
    json.dump(teams, f, ensure_ascii=False, indent=4)

with open("teams.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Вміст файлу teams.json:")
place = 1
for team in data:
    print(place, team, "-", data[team], "балів")
    place += 1

new_team = input("\nВведіть назву десятої команди: ")
new_points = int(input("Введіть кількість її балів: "))

points = list(data.values())

if new_points >= points[0] or new_points <= points[-1] or new_points in points:
    print("Неправильна кількість балів")
else:
    new_place = 1
    for p in points:
        if p > new_points:
            new_place += 1

    weaker = []
    for team in data:
        if data[team] < new_points:
            weaker.append(team)

    print("Команда", new_team, "зайняла", new_place, "місце")
    print("Команди, які набрали менше балів:", ", ".join(weaker))

    result = {
        "team": new_team,
        "points": new_points,
        "place": new_place,
        "weaker_teams": weaker
    }

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print("Результат збережено у файл result.json")