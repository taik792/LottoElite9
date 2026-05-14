import json
from collections import Counter
from itertools import combinations

# ==========================================
# CARICA ESTRAZIONI
# ==========================================

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {
    "top": {},
    "jolly": {},
    "ruote": {}
}

# ==========================================
# FUNZIONE CICLICA
# ==========================================

def genera_ambo_ciclico(estrazione):

    numeri = estrazione[:]

    frequenze = Counter()

    # Analizza tutte le coppie
    for a, b in combinations(numeri, 2):

        distanza = abs(a - b)

        if distanza > 45:
            distanza = 90 - distanza

        somma = (a + b) % 90
        if somma == 0:
            somma = 90

        frequenze[distanza] += 2
        frequenze[somma] += 1

    # Numeri più forti
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

top_list = []

for ruota, lista_estrazioni in estrazioni.items():

    ultima = lista_estrazioni[-1]

    ambo, score = genera_ambo_ciclico(ultima)

    risultati["ruote"][ruota.lower()] = {
        "estrazione": ultima,
        "ambo": ambo,
        "score": round(score, 2)
    }

    top_list.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score
    })

# ==========================================
# TOP 3
# ==========================================

top_ordinati = sorted(
    top_list,
    key=lambda x: x["score"],
    reverse=True
)[:3]

for i, item in enumerate(top_ordinati):

    risultati["top"][str(i)] = {
        "ruota": item["ruota"],
        "ambo": item["ambo"],
        "score": round(item["score"], 2)
    }

# ==========================================
# JOLLY
# ==========================================

migliore = top_ordinati[0]

risultati["jolly"] = {
    "ruota": migliore["ruota"],
    "ambo": migliore["ambo"],
    "score": round(migliore["score"], 2)
}

# ==========================================
# SALVA JSON
# ==========================================

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)

print("✅ Nuovo motore ciclico generato correttamente.")