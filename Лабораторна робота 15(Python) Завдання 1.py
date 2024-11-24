import pandas as pd

# Початковий словник
train_schedule = {
    16: {"destination": "Київ - Харків", "arrival": (10, 30), "departure": (10, 45)},
    102: {"destination": "Львів - Одеса", "arrival": (12, 0), "departure": (12, 15)},
    123: {"destination": "Київ - Дніпро", "arrival": (14, 45), "departure": (15, 0)},
    104: {"destination": "Одеса - Львів", "arrival": (16, 10), "departure": (16, 25)},
    105: {"destination": "Харків - Київ", "arrival": (18, 50), "departure": (19, 5)},
    116: {"destination": "Ужгород - Київ", "arrival": (7, 20), "departure": (7, 35)},
    107: {"destination": "Чернівці - Львів", "arrival": (9, 40), "departure": (9, 55)},
    18: {"destination": "Київ - Запоріжжя", "arrival": (13, 10), "departure": (13, 25)},
    109: {"destination": "Харків - Одеса", "arrival": (17, 5), "departure": (17, 20)},
    110: {"destination": "Львів - Київ", "arrival": (20, 0), "departure": (20, 15)},
}

# Перетворення словника на датафрейм
df = pd.DataFrame.from_dict(train_schedule, orient="index").reset_index()
df.rename(columns={"index": "train_number"}, inplace=True)

# Додавання тривалості зупинки (в хвилинах)
df["arrival_minutes"] = df["arrival"].apply(lambda x: x[0] * 60 + x[1])
df["departure_minutes"] = df["departure"].apply(lambda x: x[0] * 60 + x[1])
df["stop_duration"] = df["departure_minutes"] - df["arrival_minutes"]

# Розділення напрямку на початкове і кінцеве міста
df[["start_city", "end_city"]] = df["destination"].str.split(" - ", expand=True)

# Агрегація: кількість потягів за містом призначення
grouped = df.groupby("end_city").size().reset_index(name="train_count")

# Виведення результатів
print("Датафрейм потягів:")
print(df[["train_number", "destination", "arrival", "departure", "stop_duration", "start_city", "end_city"]])

print("\nКількість потягів за містами призначення:")
print(grouped)
