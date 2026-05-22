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
# CARICA JSON
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati_ruote = []

# =========================
# CALCOLO CICLICO
# =========================

def calcolo_ciclico(numeri):

    score_numeri = {}

    frequenze = Counter(numeri)

    for numero in set(numeri):

        score = 0

        # frequenza
        score += frequenze[numero] * 2

        # distanze cicliche
        for altro in numeri:

            dist = abs(numero - altro)

            if dist > 45:
                dist = 90 - dist

            if dist <= 9:
                score += 2

            elif dist <= 18:
                score += 1

        score_numeri[numero] = score

    ordinati = sorted(
        score_numeri.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ordinati

# =========================
# ANALISI RUOTE
# =========================

for ruota in RUOTE_ORDINE:

    storico = estrazioni[ruota]

    # ultime 12 estrazioni
    ultime_12 = storico[-12:]

    archivio = []

    for estrazione in ultime_12:
        archivio.extend(estrazione)

    # ultima estrazione
    ultima_estrazione = storico[-1]

    classifica = calcolo_ciclico(archivio)

    ambo = []

    for numero, score in classifica:

        # esclude numeri già usciti
        if numero not in ultima_estrazione:
            ambo.append(numero)

        if len(ambo) == 2:
            break

    score_finale = (
        classifica[0][1] + classifica[1][1]
    ) // 2

    risultati_ruote.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score_finale,
        "estrazione": ultima_estrazione
    })

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
# =========================

jolly = ordinati[:3]

# =========================
# AMBO FORTE
# =========================

ambo_forte = [
    r for r in ordinati
    if r["score"] >= 7
]

# =========================
# SALVA RISULTATI
# =========================

output = {
    "tutte": risultati_ruote,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Risultati generati correttamente.")
