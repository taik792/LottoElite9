import json
from collections import Counter
from itertools import combinations

# CARICA ESTRAZIONI
with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {
    "top": {},
    "jolly": {},
    "ruote": {}
}

# ANALISI RUOTE
for ruota, lista_estrazioni in estrazioni.items():

    frequenza = Counter()
    coppie = Counter()

    # ultime 16 estrazioni
    ultime = lista_estrazioni[-16:]

    for estrazione in ultime:

        # frequenza numeri
        for n in estrazione:
            frequenza[n] += 1

        # coppie
        for c in combinations(sorted(estrazione), 2):
            coppie[c] += 1

    score_ambi = []

    # crea score sugli ambi
    for ambo, freq in coppie.items():

        n1, n2 = ambo

        score = (
            freq * 10 +
            frequenza[n1] * 2 +
            frequenza[n2] * 2
        )

        # bonus numeri vicini
        if abs(n1 - n2) <= 7:
            score += 4

        # bonus numeri alti
        if n1 >= 70 or n2 >= 70:
            score += 2

        score_ambi.append({
            "ambo": [n1, n2],
            "score": round(score, 2)
        })

    # ordina
    score_ambi.sort(key=lambda x: x["score"], reverse=True)

    miglior_ambo = score_ambi[0]

    # salva risultati
    risultati["ruote"][ruota] = {
        "ultima_estrazione": lista_estrazioni[-1],
        "ambo": miglior_ambo["ambo"],
        "score": miglior_ambo["score"]
    }

# TOP 3
top3 = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)[:3]

for ruota, dati in top3:
    risultati["top"][ruota] = {
        "ambo": dati["ambo"],
        "score": dati["score"]
    }

# JOLLY
jolly_ruota, jolly_dati = top3[0]

risultati["jolly"][jolly_ruota] = {
    "ambo": jolly_dati["ambo"]
}

# SALVA JSON
with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("✅ Motore 9 AMBO generato!")
