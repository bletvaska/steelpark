from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from sqlmodel import Session, select

from .helpers import get_db_engine
from .models.player import Player


# 📥 Načíta skóre hráčov z databázy
with Session(get_db_engine()) as session:
    scores = session.exec(select(Player.score)).all()

# ✅ Kontrola, či máme dáta
if not scores:
    print("⚠️ V databáze nie sú žiadne skóre!")
    exit()

# 📊 Prevod na numpy array
scores = np.array(scores)

# 📈 Výpočet priemeru a smerodajnej odchýlky
mean_score = np.mean(scores)
std_dev = np.std(scores)

print(f'Minimalna hodnota: {min(scores)} Maximalna hodnota: {max(scores)}')
print(f"📌 Priemer skóre: {mean_score:.2f}, Smerodajná odchýlka: {std_dev:.2f}")

# 🔢 Definovanie 9 binov (intervalov)
bins = np.linspace(min(scores), max(scores), 9)  # 10 hraníc -> 9 intervalov

import math


    
# 🟢 Vytvorenie histogramu s 9 binmi
hist_values, bin_edges = np.histogram(scores, bins=bins)
# print(type(hist_values))
# print(bin_edges)
score = 0
player_score_bin = None
intervals = []
for i in range(len(bin_edges) - 1):
    intervals.append(f"{math.ceil(bin_edges[i])} - {math.floor(bin_edges[i+1])}")
    if bin_edges[i] <= score <= bin_edges[i+1]:
        player_score_bin = i

print(intervals)
print(player_score_bin)

data = int_list = list(map(int, hist_values))
print(type(data), data)

# 🟡 Vygenerovanie Gaussovej krivky zoskalovanej podľa počtu hráčov
x = np.linspace(min(scores), max(scores), 100)
y = (len(scores) * np.diff(bins)[0]) * (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_score) / std_dev) ** 2)

# 🎨 Vykreslenie histogramu a Gaussovej krivky
plt.figure(figsize=(10, 6))
plt.bar(bin_edges[:-1], hist_values, width=np.diff(bins), alpha=0.6, color='g', edgecolor='black', label='Histogram (9 intervalov)')
plt.plot(x, y, linewidth=2, color='r', label='Gaussova krivka')
plt.title('Rozdelenie skóre hráčov do 9 intervalov a Gaussova krivka')
plt.xlabel('Skóre')
plt.ylabel('Počet hráčov')
plt.xticks(bin_edges.round(2))  # Označenie hodnôt na X osi
plt.legend()
plt.grid(True)
plt.show()
