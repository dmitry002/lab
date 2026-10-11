import csv

file_in = "gdp_per_capita.csv"
file_out = "search_result.csv"

try:
    f = open(file_in, "r", encoding="utf-8")
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
    f.close()
except FileNotFoundError:
    print("Помилка: файл", file_in, "не знайдено")
    exit()
except Exception as e:
    print("Помилка при відкритті файлу:", e)
    exit()

text = input("Введіть назви країн через кому: ")
countries = text.split(",")

result = []
for name in countries:
    name = name.strip().lower()
    found = False
    for row in rows:
        if name in [x.lower() for x in row]:
            result.append(row)
            found = True
    if not found:
        print("Країну", name, "не знайдено")

for row in result:
    print(row)

try:
    f = open(file_out, "w", encoding="utf-8", newline="")
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(result)
    f.close()
    print("Результати збережено у файл", file_out)
except Exception as e:
    print("Помилка при записі файлу:", e)