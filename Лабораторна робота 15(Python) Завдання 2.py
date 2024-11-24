import pandas as pd
import csv
import os

#Назва файлу
file_name = 'comptagevelo2009.csv'

try:
    # Перевірка, чи існує файл у поточній директорії
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Файл '{file_name}' не знайдено в поточній директорії.")

    # Зчитування файлу за допомогою csv.DictReader для попередньої перевірки
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)  # Завантаження усіх рядків у список
        if not rows:
            raise ValueError("Файл порожній або має неправильний формат.")
        
        # Перевірка наявності необхідних стовпців
        required_columns = {'Date', 'Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Файл не містить усіх необхідних стовпців: {required_columns}")

    # Завантаження CSV-файлу у DataFrame
    data = pd.DataFrame(rows)

    # Перетворення стовпця "Date" у формат datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')
    if data['Date'].isna().any():
        raise ValueError("Помилка у форматі дат у файлі.")

    # Перетворення числових стовпців у тип float
    for col in ['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf']:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Обчислення загальної кількості велосипедистів за день
    data['Total'] = data[['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brebeuf']].sum(axis=1, skipna=True)

    # Додавання стовпця "Month" для групування за місяцями
    data['Month'] = data['Date'].dt.month

    # Групування даних за місяцями та обчислення загальної кількості велосипедистів
    monthly_data = data.groupby('Month')['Total'].sum().reset_index()

    # Знаходження місяця з найбільшою кількістю велосипедистів
    most_popular_month = monthly_data.loc[monthly_data['Total'].idxmax()]

    # Виведення результатів
    print("Загальна кількість велосипедистів за місяцями:")
    print(monthly_data)

    print("\nНайпопулярніший місяць:")
    print(f"Місяць: {int(most_popular_month['Month'])}, Кількість велосипедистів: {int(most_popular_month['Total'])}")

except FileNotFoundError as e:
    print(f"Помилка: {e}")
except pd.errors.EmptyDataError:
    print("Помилка: Файл порожній або має неправильний формат.")
except ValueError as e:
    print(f"Помилка: {e}")

