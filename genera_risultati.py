import json
from collections import Counter

# =========================
# CARICA JSON
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# FUNZIONI CICLICHE
# =========================

def piu9(n):
    return ((n + 8) % 90) + 1

def meno9(n):
    return ((n - 10) % 90) + 1

def complementare(n):
    return 90 - n if n != 90 else 90

# =========================
# SCORE
# =========================

def calcola_score(numero, frequenze):

    score = 0

    score += frequenze.get(numero, 0)

    score += frequenze.get(piu9(numero), 0)

    score += frequenze.get(meno9(numero), 0)

    score += frequenze.get(complementare(numero), 0)

    return score

# =========================
# ORDINE RUOTE
# =========================

ordine_ruote = [
    "Bari",
    "Cagliari",
    "Firenze",
    "Genova",
    "Milano",
    "Napoli",
    "Palermo",
    "Roma",
    "Torino",
    "Venezia",
    "Nazionale"
]

# =========================
# ELABORAZIONE
# =========================

top = []

for ruota in ordine_ruote:

    if ruota not in estrazioni:
        continue

    storico_ruota = estrazioni[ruota]

    # Ultime 12 estrazioni
    ultime = storico_ruota[-12:]

    # Ultima estrazione reale
    ultima = ultime[-1]

    # Frequenze
    tutti_numeri = []

    for estrazione in ultime:
        tutti_numeri.extend(estrazione)

    frequenze = Counter(tutti_numeri)

    candidati = []

    # Genera numeri ciclici
    for n in ultima:

        candidati.append(piu9(n))
        candidati.append(meno9(n))
        candidati.append(complementare(n))

    # Rimuove numeri usciti
    candidati = [n for n in candidati if n not in ultima]

    # Rimuove duplicati
    candidati = list(set(candidati))

    scored = []

    for n in candidati:

        s = calcola_score(n, frequenze)

        scored.append((n, s))

    # Ordina per score
    scored.sort(key=lambda x: x[1], reverse=True)

    if len(scored) < 2:
        continue

    ambo = [
        scored[0][0],
        scored[1][0]
    ]

    score_finale = scored[0][1] + scored[1][1]

    risultato = {
        "ruota": ruota,
        "ambo": ambo,
        "score": score_finale,
        "estrazione": ultima
    }

    top.append(risultato)

# =========================
# JOLLY
# =========================

jolly = sorted(
    top,
    key=lambda x: x["score"],
    reverse=True
)[:3]

# =========================
# AMBO FORTE
# =========================

amboForte = sorted(
    top,
    key=lambda x: x["score"],
    reverse=True
)[:5]

# =========================
# OUTPUT
# =========================

risultati = {
    "top": top,
    "jolly": jolly,
    "amboForte": amboForte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2, ensure_ascii=False)

print("risultati.json generato correttamente")