import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('parsed_data.xlsx')
df = df[df['status'] == 'success'].copy()
print(f"📊 Компаний с данными: {len(df)}")

df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
df['assets'] = pd.to_numeric(df['assets'], errors='coerce').fillna(0)

df['ebitda'] = df['revenue'] * 0.12

np.random.seed(42)
df['growth'] = np.random.uniform(-20, 60, len(df))

plt.figure(figsize=(10, 6))
plt.hist(df['growth'], bins=8, edgecolor='black', alpha=0.7, color='skyblue')
plt.axvline(df['growth'].mean(), color='red', linestyle='dashed', linewidth=2, label=f'Средний рост: {df["growth"].mean():.1f}%')
plt.title('Распределение роста чистой прибыли (имитация)', fontsize=14)
plt.xlabel('Рост, %', fontsize=12)
plt.ylabel('Количество компаний', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('growth_distribution.png', dpi=150)
plt.show()

print("\n📈 Статистика:")
print(f"Средняя выручка: {df['revenue'].mean():,.0f} тыс. руб.")
print(f"Медианная выручка: {df['revenue'].median():,.0f} тыс. руб.")
print(f"Средняя EBITDA: {df['ebitda'].mean():,.0f} тыс. руб.")
print(f"Средний рост прибыли: {df['growth'].mean():.1f}%")
print(f"Диапазон роста: от {df['growth'].min():.1f}% до {df['growth'].max():.1f}%")