import math
from collections import Counter
# import numpy as np
import matplotlib.pyplot as plt
from sqlmodel import Session, select

from .helpers import get_db_engine
from .models.player import Player

def mean(values):
    return sum(values) / len(values)

def stddev(values, mean_value):
    variance = sum((x - mean_value) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

def gaussian(x, mean, std_dev):
    coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
    exponent = math.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    return coefficient * exponent

# 📥 Načíta skóre hráčov z databázy
with Session(get_db_engine()) as session:
    scores = session.exec(select(Player.score)).all()

# ✅ Kontrola, či máme dáta
if not scores:
    print("⚠️ V databáze nie sú žiadne skóre!")
    exit()

# 📊 Prevod na numpy array
# scores = np.array(scores)

# 📈 Výpočet priemeru a smerodajnej odchýlky
mean_score = mean(scores)
std_dev = stddev(scores, mean_score)

num_bins = 9
min_score, max_score = min(scores), max(scores)
bin_width = (max_score - min_score) / num_bins

print(f'Minimalna hodnota: {min(scores)} Maximalna hodnota: {max(scores)}')
print(f"📌 Priemer skóre: {mean_score:.2f}, Smerodajná odchýlka: {std_dev:.2f}")

# Vytvorenie binov ako intervalov
bins = [min_score + i * bin_width for i in range(num_bins + 1)]
histogram = {i: 0 for i in range(num_bins)}


# Priradenie skóre hráčov do binov
for score in scores:
    for i in range(num_bins):
        if bins[i] <= score < bins[i + 1]:  # Posledný interval zahŕňa max_score
            histogram[i] += 1
            break

# Prevod histogramu na zoznam hodnôt
hist_values = list(histogram.values())

# 🟡 Vygenerovanie Gaussovej krivky zoskalovanej podľa počtu hráčov
x = [min_score + i * (max_score - min_score) / 100 for i in range(101)]
y = [len(scores) * bin_width * gaussian(x, mean_score, std_dev) for x in x]

print(bins)

# 🎨 Vykreslenie histogramu a Gaussovej krivky
plt.figure(figsize=(10, 6))
plt.bar(bins[:-1], hist_values, width=bin_width, alpha=0.6, color='g', edgecolor='black', label='Histogram (9 intervalov)')
plt.plot(x, y, linewidth=2, color='r', label='Gaussova krivka')
plt.title('Rozdelenie skóre hráčov do 9 intervalov a Gaussova krivka')
plt.xlabel('Skóre')
plt.ylabel('Počet hráčov')
plt.xticks([round(b, 2) for b in bins])  # Zaokrúhlenie hodnôt na X osi
plt.legend()
plt.grid(True)
plt.show()
