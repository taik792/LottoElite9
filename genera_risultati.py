import json
from collections import Counter

RUOTE_ORDINE = [
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

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# PRENDE LE ULTIME 12 ESTRAZIONI
ultime = estrazioni[-12:]

risultati_ruote = []
jolly = []
ambo_forte = []

# =========================
# FUNZIONE CICLICA
# =========================

def calcolo_ciclico(numeri):

    frequenze = Counter()
    distanze = Counter()

    # frequenze
    for n in numeri:
        frequenze[n] += 1

    # distanze cicliche
    for i in range(len(numeri)-1):
        a = numeri[i]
        b = numeri[i+1]

        dist = abs(a - b)

        if dist > 45:
            dist = 90 - dist

        distanze[dist] += 1

    score_numeri = {}

    for n in set(numeri):

        score = 0

        # frequenza
        score += frequenze[n] * 2

        # vicinanza ciclica
        for altro in numeri:

            dist = abs(n - altro)

            if dist > 45:
                dist = 90 - dist

            if dist <= 9:
                score += 2
            elif dist <= 18:
                score += 1

        score_numeri[n] = score

    ordinati = sorted(score_numeri.items(), key=lambda x: x[1], reverse=True)

    return ordinati

# =========================
# ANALISI RUOTE
# =========================

for ruota in RUOTE_ORDINE:

    archivio_ruota = []

    for estrazione in ultime:
        if ruota in estrazione:
            archivio_ruota.extend(estrazione[ruota])

    # ultima estrazione
    ultima_estrazione = ultime[-1][ruota]

    # calcolo ciclico
    classifica = calcolo_ciclico(archivio_ruota)

    ambo = []

    for numero, score in classifica:

        # ESCLUDE numeri già usciti nell'ultima estrazione
        if numero not in ultima_estrazione:
            ambo.append(numero)

        if len(ambo) == 2:
            break

    score_finale = (
        classifica[0][1] + classifica[1][1]
    ) // 2

    risultato = {
        "ruota": ruota,
        "ambo": ambo,
        "score": score_finale,
        "estrazione": ultima_estrazione
    }

    risultati_ruote.append(risultato)

# =========================
# ORDINA PER SCORE
# =========================

ordinati = sorted(
    risultati_ruote,
    key=lambda x: x["score"],
    reverse=True
)

# =========================
# JOLLY
# PRIME 3 RUOTE
# =========================

jolly = ordinati[:3]

# =========================
# AMBO FORTE
# SOLO SCORE >= 7
# =========================

ambo_forte = [
    r for r in ordinati
    if r["score"] >= 7
]

# =========================
# SALVA JSON
# =========================

output = {
    "tutte": risultati_ruote,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Risultati generati correttamente.")
