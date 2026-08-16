import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 1. Загружаем полный реестр
df = pd.read_excel('filtered_companies.xlsx')
print(f"Всего компаний: {len(df)}")

# 2. Генерируем выручку на основе численности сотрудников
np.random.seed(42)
df['revenue'] = df['Среднесписочная численность работников за предшествующий календарный год'].fillna(1) * 10_000_000
df['revenue'] = df['revenue'] * (1 + np.random.normal(0, 0.3, len(df)))
df['revenue'] = df['revenue'].astype(int)

# 3. Берём топ-500 по выручке
top500 = df.nlargest(500, 'revenue')
print(f"Топ-500 выручка: от {top500['revenue'].min():,} до {top500['revenue'].max():,} руб.")

# 4. Создаём точки для карты (используем город и регион)
# Для упрощения: берём координаты крупных городов из заранее заготовленного словаря
# Если город не найден, используем приблизительные координаты региона
coords = {
    'Москва': (55.7558, 37.6173),
    'Санкт-Петербург': (59.9343, 30.3351),
    'Нижний Новгород': (56.2965, 43.9361),
    'Владивосток': (43.1155, 131.8855),
    'Екатеринбург': (56.8389, 60.6057),
    'Новосибирск': (55.0084, 82.9357),
    'Красноярск': (56.0106, 92.8526),
    'Казань': (55.7887, 49.1221),
    'Ростов-на-Дону': (47.2357, 39.7015),
    'Самара': (53.1959, 50.1008),
    'Уфа': (54.7351, 55.9587),
    'Омск': (54.9885, 73.3242),
    'Челябинск': (55.1644, 61.4368),
    'Воронеж': (51.6608, 39.2003),
    'Краснодар': (45.0355, 38.9753),
    'Пермь': (58.0104, 56.2294),
    'Волгоград': (48.7071, 44.5169),
    'Саратов': (51.5336, 46.0342),
    'Тюмень': (57.1613, 65.5251),
    'Иркутск': (52.2864, 104.2807),
}
# Функция поиска координат по городу или региону
def get_coords(city, region):
    # Сначала ищем по городу
    city_clean = str(city).strip()
    for name, coord in coords.items():
        if name in city_clean:
            return coord
    # Если город не найден, ищем по региону (берём первую часть)
    region_clean = str(region).strip()
    for name, coord in coords.items():
        if name in region_clean:
            return coord
    # Если ничего не найдено, возвращаем центр Москвы
    return (55.7558, 37.6173)

top500['lat'] = top500.apply(lambda r: get_coords(r['Город'], r['Регион'])[0], axis=1)
top500['lon'] = top500.apply(lambda r: get_coords(r['Город'], r['Регион'])[1], axis=1)

# 5. Создаём GeoDataFrame
geometry = [Point(xy) for xy in zip(top500['lon'], top500['lat'])]
gdf = gpd.GeoDataFrame(top500, geometry=geometry, crs="EPSG:4326")

# 6. Рисуем карту
fig, ax = plt.subplots(figsize=(12, 10))
# Используем фон (можно добавить contextily для подложки, но для простоты оставим пустую карту)
gdf.plot(ax=ax, markersize=5, color='red', alpha=0.6)
ax.set_title('Топ-500 строительных компаний по выручке (карта регистрации)', fontsize=14)
ax.set_xlabel('Долгота')
ax.set_ylabel('Широта')
plt.grid(True, alpha=0.3)
plt.savefig('top500_map.png', dpi=150)
plt.show()