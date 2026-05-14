import json
from collections import Counter
from itertools import combinations

# ==========================================
# CARICA ESTRAZIONI
# ==========================================

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

# ==========================================
# STRUTTURA RISULTATI
# ==========================================

risultati = {
    "top": [],
    "jolly": {},
    "ruote": {}
}

# ==========================================
# FUNZIONE MOTORE CICLICO
# ==========================================

def genera_ambo_ciclico(estrazione):

    frequenze = Counter()

    # Tutte le combinazioni di 2 numeri
    for a, b in combinations(estrazione, 2):

        # DISTANZA CICLICA
        distanza = abs(a - b)

        if distanza > 45:
            distanza = 90 - distanza

        # SOMMA CICLICA
        somma = (a + b) % 90

        if somma == 0:
            somma = 90

        # PESI
        frequenze[distanza] += 2
        frequenze[somma] += 1

    migliori = frequenze.most_common(2)

    if len(migliori) < 2:
        return [1, 90], 0

    numero1 = migliori[0][0]
    numero2 = migliori[1][0]

    score = migliori[0][1] + migliori[1][1]

    return [numero1, numero2], score

# ==========================================
# ANALISI RUOTE
# ==========================================

classifica = []

for ruota, lista_estrazioni in estrazioni.items():

    ultima = lista_estrazioni[-1]

    ambo, score = genera_ambo_ciclico(ultima)

    # SALVA RUOTA
    risultati["ruote"][ruota.lower()] = {
        "estrazione": ultima,
        "ambo": ambo,
        "score": round(score, 2)
    }

    # CLASSIFICA TOP
    classifica.append({
        "ruota": ruota,
        "ambo": ambo,
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
        "ambo": item["ambo"],
        "score": round(item["score"], 2)
    })

# ==========================================
# JOLLY
# ==========================================

migliore = top3[0]

risultati["jolly"] = {
    "ruota": migliore["ruota"],
    "ambo": migliore["ambo"],
    "score": round(migliore["score"], 2)
}

# ==========================================
# SALVA FILE JSON
# ==========================================

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)

print("✅ risultati.json generato correttamente")