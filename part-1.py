import requests
import json
import csv

indicator = "NY.GDP.PCAP.CD"
year = "2019"
url = (
    f"https://api.worldbank.org/v2/country/all/"
    f"indicator/{indicator}?date={year}&format=json&per_page=500"
)
json_file = "gdp_per_capita.json"
csv_file = "gdp_per_capita.csv"


def get_data(url):
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Помилка виконання HTTP-запиту:", e)
        return None

    if response.status_code != 200:
        print("Помилка отримання даних:", response.status_code)
        return None

    print("Дані успішно отримано")
    try:
        data = response.json()
    except ValueError:
        print("Відповідь не є коректним JSON")
        return None
    return data


def check_data(data):
    if data is None:
        print("Дані відсутні")
        return False
    if not isinstance(data, list) or len(data) < 2:
        print("Неправильна структура даних")
        return False
    if data[1] is None or len(data[1]) == 0:
        print("Немає записів за вказаний рік")
        return False
    return True


def save_json(data, file_name):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Створено файл", file_name)
        return True
    except OSError as e:
        print("Помилка запису файлу", file_name, ":", e)
        return False


def save_csv(data, file_name):
    csv_data = []
    for item in data[1]:
        if item["value"] is not None:
            csv_data.append([
                item["country"]["value"],
                item["date"],
                item["value"]
            ])

    try:
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Year", "GDP per capita (current US$)"])
            writer.writerows(csv_data)
        print("Створено файл", file_name)
    except OSError as e:
        print("Помилка запису файлу", file_name, ":", e)
        return None
    return csv_data


def print_results(json_name, csv_name):
    print("\nЗміст JSON:")
    print("-" * 50)
    try:
        with open(json_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data[1][:5]:
            print(json.dumps(item, ensure_ascii=False, indent=4))
            print()
    except (OSError, json.JSONDecodeError) as e:
        print("Помилка відкриття файлу", json_name, ":", e)

    print("Зміст CSV:")
    print("-" * 50)
    try:
        with open(csv_name, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i > 5:
                    break
                print(", ".join(row))
    except OSError as e:
        print("Помилка відкриття файлу", csv_name, ":", e)


data = get_data(url)
if check_data(data):
    if save_json(data, json_file):
        if save_csv(data, csv_file) is not None:
            print_results(json_file, csv_file)