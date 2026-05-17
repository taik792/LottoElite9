import json

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    dati = json.load(f)

risultati = []

# =========================
# ANALISI RUOTE
# =========================

for ruota, estrazioni in dati.items():

    # SALTA RUOTE VUOTE
    if not estrazioni or len(estrazioni) < 2:
        continue

    # ULTIMA ESTRAZIONE
    ultima = estrazioni[-1]

    # ULTIME 10 ESTRAZIONI
    ultime10 = estrazioni[-10:]

    frequenze = {}

    # CONTA FREQUENZE
    for estrazione in ultime10:

        for numero in estrazione:

            # ESCLUDE NUMERI USCITI
            # NELL'ULTIMA ESTRAZIONE
            if numero in ultima:
                continue

            frequenze[numero] = frequenze.get(numero, 0) + 1

    # ORDINA FREQUENZE
    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # SERVONO ALMENO 2 NUMERI
    if len(ordinati) < 2:
        continue

    # CREA AMBO
    ambo = [
        ordinati[0][0],
        ordinati[1][0]
    ]

    # SCORE
    score = (
        ordinati[0][1] +
        ordinati[1][1]
    )

    risultati.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "estrazione": ultima
    })

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
    "Venezia"
]

risultati.sort(
    key=lambda x: ordine_ruote.index(x["ruota"])
)

# =========================
# JOLLY
# TOP 3 SCORE
# =========================

jolly = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)[:3]

# =========================
# AMBI FORTI
# SCORE >= 7
# =========================

forti = sorted(
    [x for x in risultati if x["score"] >= 7],
    key=lambda x: x["score"],
    reverse=True
)[:5]

# =========================
# OUTPUT JSON
# =========================

output = {
    "tutte": risultati,
    "jolly": jolly,
    "forti": forti
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("risultati.json generato correttamente")