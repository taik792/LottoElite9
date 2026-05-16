import json

# CARICA ESTRAZIONI
with open("estrazioni.json", "r", encoding="utf-8") as f:
    dati = json.load(f)

risultati = []

for ruota, estrazioni in dati.items():

    # ultime 12 estrazioni
    ultime = estrazioni[-12:]

    frequenze = {}

    for estrazione in ultime:

        for numero in estrazione:

            frequenze[numero] = frequenze.get(numero, 0) + 1

    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    if len(ordinati) < 2:
        continue

    ambo = [
        ordinati[0][0],
        ordinati[1][0]
    ]

    score = ordinati[0][1] + ordinati[1][1]

    risultati.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "estrazione": estrazioni[-1]
    })

# ORDINA PER SCORE
risultati = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)

# TOP = tutte ruote
top = risultati

# JOLLY = prime 3
jolly = risultati[:3]

# AMBO FORTE = prime 5
ambo_forte = risultati[:5]

output = {
    "tutte": top,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

# SALVA JSON
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("risultati.json generato correttamente")