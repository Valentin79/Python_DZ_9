# Напишите следующие функции:
# ○ Нахождение корней квадратного уравнения
# ○ Генерация csv файла с тремя случайными числами в каждой строке.
# 100-1000 строк.
# ○ Декоратор, запускающий функцию нахождения корней квадратного
# уравнения с каждой тройкой чисел из csv файла.
# ○ Декоратор, сохраняющий переданные параметры и результаты работы
# функции в json файл.

import csv
import json
import random


def decorator(func): # переопределяем фуенкцию по поиску корней
    result_dict = {}

    def wrapper(*args): # исходные аргументы нам уже не нужны, но без них все ломается
        with(
            open("csv_file.csv", "r", encoding='utf-8', newline='') as csv_file,
            open("json_file.json", "w", encoding='utf-8') as j_file
        ):
            csv_file = csv.reader(csv_file) # считываем файл
            for line in csv_file: # построчно присваеваем значения
                a, b, c = int(line[0]), int(line[1]), int(line[2])
                result = func(a, b, c) # запускаем функцию со считанными значениями
                result_dict.update(result) # добавляем результат в общий словарь
            # сперва записывал полученный словарь тут, потом сделал отдельную функцию. Но пусть остается.
            json.dump(result_dict, j_file, ensure_ascii=False, indent=4)
        return result_dict
    return wrapper


def right_write(func): # переопределяем функцию записи в json
    def wrapper(*args):
        file = "json_file1.json"  # другое название файла
        # data = find_roots(1, 2, 3) # можно и так сделать, если изначально данные из другого источника
        data = args[1]
        func(file, data)
    return wrapper

@decorator
def find_roots(a, b, c): # Поиск корней
    result = {}
    if a != 0:
        d = b * b - 4 * a * c
        if d > 0:
            x1 = (-b + d ** 0.5) / (2 * a)
            x2 = (-b - d ** 0.5) / (2 * a)
            result[f"{a}, {b}, {c}"] = (str(x1), str(x2))

        elif d == 0:
            x = (-b / (2 * a))
            result[f"{a}, {b}, {c}"] = str(x)

        else:
            d: complex = complex(d, 0)
            x1 = (- b - d ** 0.5) / (2 * a)
            x2 = (- b + d ** 0.5) / (2 * a)
            result[f"{a}, {b}, {c}"] = (str(x1), str(x2))

    # else: # непонятно, надо ли что-то записывать, если первый аргумент равен 0.
    #     print("a = 0")
    return result


@right_write
def write_json(file_name, data): # запись в json
    with open(file_name, "w", encoding='utf-8') as j_file:
        json.dump(data, j_file, ensure_ascii=False, indent=4)


def create_csv(row_count: int): # сщздание csv
    with open("csv_file.csv", 'w', encoding='utf-8') as f:
        for i in range(row_count):
            a = random.randint(0, 10)
            b = random.randint(0, 10)
            c = random.randint(0, 10)
            csv_writer = csv.writer(f, dialect='excel', delimiter=',', lineterminator="\r")
            csv_writer.writerow([str(a), str(b), str(c)])


create_csv(5)
result = find_roots(1, 2, 3)
write_json("json_file2.json", result)
