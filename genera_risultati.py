import json
from collections import Counter
from itertools import combinations

# ==========================================
# CARICA ESTRAZIONI
# ==========================================

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

# ==========================================
# RUOTE FISSE
# ==========================================

RUOTE = [
    "bari",
    "cagliari",
    "firenze",
    "genova",
    "milano",
    "napoli",
    "palermo",
    "roma",
    "torino",
    "venezia"
]

# ==========================================
# STRUTTURA RISULTATI
# ==========================================

risultati = {
    "top": [],
    "jolly": {},
    "ruote": {}
}

# ==========================================
# MOTORE CICLICO
# ==========================================

def genera_ambo_ciclico(estrazione):

    frequenze = Counter()

    for a, b in combinations(estrazione, 2):

        distanza = abs(a - b)

        if distanza > 45:
            distanza = 90 - distanza

        somma = (a + b) % 90

        if somma == 0:
            somma = 90

        frequenze[distanza] += 2
        frequenze[somma] += 1

    migliori = frequenze.most_common(2)

    if len(migliori) < 2:
        return [1, 90], 0

    n1 = migliori[0][0]
    n2 = migliori[1][0]

    score = migliori[0][1] + migliori[1][1]

    return [n1, n2], score

# ==========================================
# ANALISI RUOTE
# ==========================================

classifica = []

for ruota in RUOTE:

    # Cerca la ruota ignorando maiuscole/minuscole
    dati_ruota = None

    for key in estrazioni.keys():

        if key.lower().strip() == ruota:
            dati_ruota = estrazioni[key]
            break

    if not dati_ruota:
        continue

    ultima = dati_ruota[-1]

    numeri, score = genera_ambo_ciclico(ultima)

    risultati["ruote"][ruota] = {
        "ultima_estrazione": ultima,
        "numeri": numeri,
        "score": round(score, 2)
    }

    classifica.append({
        "ruota": ruota.capitalize(),
        "numeri": numeri,
        "score": score
    })

# ==========================================
# TOP 3
# ==========================================

top3 = sorted(
    classifica,
    key=lambda x: x["score"],
    reverse=True
)[:3]

for item in top3:

    risultati["top"].append({
        "ruota": item["ruota"],
        "numeri": item["numeri"],
        "score": round(item["score"], 2)
    })

# ==========================================
# JOLLY
# ==========================================

migliore = top3[0]

risultati["jolly"] = {
    "ruota": migliore["ruota"],
    "numeri": migliore["numeri"],
    "score": round(migliore["score"], 2)
}

# ==========================================
# SALVA JSON
# ==========================================

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)

print("✅ risultati.json generato correttamente")