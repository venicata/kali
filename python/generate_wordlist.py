import itertools
import os

# Вземане на абсолютния път до папката, в която се намира ТОЗИ скрипт
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file_lines(filename):
    """Прочита файл и връща списък от думи, изчистени от празни пространства."""
    full_path = os.path.join(SCRIPT_DIR, filename)
    
    if not os.path.exists(full_path):
        print(f"Предупреждение: Файлът '{filename}' не е намерен на път: {full_path}")
        return []
        
    with open(full_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# 1. Зареждане на базовите думи от същата папка, в която е скриптът
names = read_file_lines("names.txt")
places = read_file_lines("places.txt")
brands = read_file_lines("brands.txt")
kvartali = read_file_lines("kvartali.txt")
patterns = read_file_lines("patterns.txt")

all_base_words = names + places + brands + kvartali + patterns

if not all_base_words:
    print("\nГрешка: Не бяха заредени никакви думи. Проверете къде се намират .txt файловете.")
    exit(1)

# 2. Дефиниране на хронологичните набори (Години)
years = [str(year) for year in range(1980, 2027)]

# 3. ЗНАЧИТЕЛНО РАЗШИРЕН НАБОР ОТ ЦИФРОВИ ПАТЕРНИ (common_digits)
common_digits = []

# А. Стандартни последователности и броения
common_digits += ["1", "12", "123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "0", "01", "012"]

# Б. Еднакви и повтарящи се цифри (често използвани за лесно писане)
for i in range(10):
    s = str(i)
    common_digits += [s*2, s*3, s*4, s*5, s*6] # напр. 00, 000, 1111, 99999

# В. Огледални, редуващи се и специфични повторения
common_digits += [
    "1212", "123123", "1122", "1221", "2112", "4321", "9876", "0987", 
    "1010", "2020", "5050", "7070", "8080", "9090", "1314", "6969", "777", "888", "999"
]

# Г. Популярни съкращения, телефонни кодове за БГ и "тийнейджърски" цифри
common_digits += [
    "007", "420", "666", "777", "911", "1312", "1488",
    "359", "088", "087", "089", "3598" # мобилни префикси
]

# Д. Популярни кратки комбинации от рождени дни (Ден/Месец без годината)
# Хората често пишат нещо като "ivan2512" (25 декември) или "maria0101"
birth_dates = ["0101", "1010", "0202", "0303", "0404", "0505", "0606", "0707", "0808", "0909", "1111", "1212", "2512"]

all_suffixes = list(set(years + common_digits + birth_dates)) # Премахва дубликати, ако има такива

# Изходният файл
output_file = os.path.join(SCRIPT_DIR, "bg_university_wordlist.txt")
print(f"Стартиране на генерирането в '{output_file}'...")
print(f"Заредени базови думи: {len(all_base_words)}")
print(f"Заредени цифрови суфикси: {len(all_suffixes)}")

# 4. Генериране и записване в общия файл
with open(output_file, "w", encoding="utf-8") as f:
    count = 0
    
    # Фаза 1: Комбинации от Базова дума + Суфикс
    for word, suffix in itertools.product(all_base_words, all_suffixes):
        f.write(f"{word}{suffix}\n")
        f.write(f"{word.capitalize()}\n") # Добавяме и вариант с главна дума, но без цифра
        f.write(f"{word.capitalize()}{suffix}\n")
        count += 3

    # Фаза 2: Само чистите базови думи (изцяло малки)
    for word in all_base_words:
        f.write(f"{word}\n")
        count += 1

print(f"Успешно генерирани {count} уникални комбинации в академичния речник.")