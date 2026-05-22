import json
import os

# =========================================
# CONFIG
# =========================================

COLPI_VALIDITA = 5

ORDINE_RUOTE = [
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

STORICO_FILE = "storico_previsioni.json"

# =========================================
# CARICA ESTRAZIONI
# =========================================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================================
# CARICA STORICO
# =========================================

if os.path.exists(STORICO_FILE):

    with open(STORICO_FILE, "r", encoding="utf-8") as f:
        storico_previsioni = json.load(f)

else:

    storico_previsioni = []

# =========================================
# ANALISI AMBO
# =========================================

def analizza_ambo(storico):

    frequenze = {}

    ultime = storico[-12:]

    for estrazione in ultime:

        for numero in estrazione:

            frequenze[numero] = (
                frequenze.get(numero, 0) + 1
            )

    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    numeri = [n[0] for n in ordinati[:2]]

    score = sum(
        n[1] for n in ordinati[:2]
    )

    return numeri, score

# =========================================
# CALCOLO COLPI
# =========================================

def calcola_colpi(ruota, ambo):

    storico = estrazioni[ruota][-COLPI_VALIDITA:]

    colpi = 0

    for estrazione in reversed(storico):

        if (
            ambo[0] in estrazione
            or
            ambo[1] in estrazione
        ):
            break

        colpi += 1

    rimanenti = COLPI_VALIDITA - colpi

    if rimanenti < 0:
        rimanenti = 0

    return rimanenti

# =========================================
# GENERA RISULTATI
# =========================================

risultati = []

for ruota in ORDINE_RUOTE:

    storico = estrazioni[ruota]

    ultima = storico[-1]

    ambo, score = analizza_ambo(storico)

    # ESCLUDE NUMERI USCITI
    if (
        ambo[0] in ultima
        or
        ambo[1] in ultima
    ):
        continue

    colpi = calcola_colpi(
        ruota,
        ambo
    )

    risultati.append({

        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "ultima": ultima,
        "colpi": colpi

    })

# =========================================
# ORDINE SCORE
# =========================================

risultati_score = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)

# =========================================
# JOLLY
# SOLO PREVISIONI FRESCHE
# =========================================

jolly = [

    r for r in risultati_score

    if r["colpi"] >= 4

][:3]

# =========================================
# AMBO FORTE
# =========================================

ambo_forte = [

    r for r in risultati_score

    if r["colpi"] > 0

][:10]

# =========================================
# AGGIORNA PREVISIONI ATTIVE
# =========================================

nuovo_storico = []

for previsione in storico_previsioni:

    ruota = previsione["ruota"]

    ambo = previsione["ambo"]

    ultima = estrazioni[ruota][-1]

    # SE ESCE ELIMINA
    if (
        ambo[0] in ultima
        or
        ambo[1] in ultima
    ):
        continue

    previsione["colpi"] -= 1

    # SE FINITI ELIMINA
    if previsione["colpi