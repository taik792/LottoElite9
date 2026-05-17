import json

# CARICA ESTRAZIONI
with open("estrazioni.json", "r", encoding="utf-8") as f:
    dati = json.load(f)

risultati = []

for ruota, estrazioni in dati.items():

    # SALTA RUOTE VUOTE
    if not estrazioni:
        continue

    # PRENDE LE ULTIME 10 ESTRAZIONI
    ultime = estrazioni[-10:]

    # PRENDE L'ULTIMA ESTRAZIONE REALE
    ultima = estrazioni[-1]

    frequenze = {}

    # CONTA FREQUENZE
    for estrazione in ultime:

        for numero in estrazione:

            frequenze[numero] = frequenze.get(numero, 0) + 1

    # ORDINA PER FREQUENZA
    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # SE CI SONO ALMENO 2 NUMERI
    if len(ordinati) < 2:
        continue

    ambo = [
        ordinati[0][0],
        ordinati[1][0]
    ]

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

# ORDINE RUOTE
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

# ORDINA RISULTATI
risultati.sort(
    key=lambda x: ordine_ruote.index(x["ruota"])
)

# TOP 3 JOLLY
jolly = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)[:3]

# AMBI FORTI SCORE >= 7
forti = sorted(
    [x for x in risultati if x["score"] >= 7],
    key=lambda x: x["score"],
    reverse=True
)[:5]

output = {
    "tutte": risultati,
    "jolly": jolly,
    "forti": forti
}

# SALVA FILE
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print("risultati.json generato correttamente")