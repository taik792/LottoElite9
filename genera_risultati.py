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
# CREA STORICO SE NON ESISTE
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

            frequenze[numero] = frequenze.get(numero, 0) + 1

    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    if len(ordinati) < 2:
        return [1, 90], 0

    ambo = [
        ordinati[0][0],
        ordinati[1][0]
    ]

    score = (
        ordinati[0][1]
        +
        ordinati[1][1]
    )

    return ambo, score

# =========================================
# CALCOLA COLPI RIMANENTI
# =========================================

def calcola_colpi(ruota, ambo):

    storico = estrazioni[ruota][-COLPI_VALIDITA:]

    colpi_passati = 0

    for estrazione in reversed(storico):

        if (
            ambo[0] in estrazione
            or
            ambo[1] in estrazione
        ):
            break

        colpi_passati += 1

    colpi_rimanenti = (
        COLPI_VALIDITA - colpi_passati
    )

    if colpi_rimanenti < 0:
        colpi_rimanenti = 0

    return colpi_rimanenti

# =========================================
# GENERA RISULTATI
# =========================================

risultati = []

for ruota in ORDINE_RUOTE:

    storico = estrazioni[ruota]

    ultima = storico[-1]

    ambo, score = analizza_ambo(storico)

    # ESCLUDI NUMERI USCITI

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
# ORDINA PER SCORE
# =========================================

risultati_score = sorted(

    risultati,

    key=lambda x: x["score"],

    reverse=True

)

# =========================================
# JOLLY
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

    # ELIMINA SE USCITO

    if (
        ambo[0] in ultima
        or
        ambo[1] in ultima
    ):
        continue

    previsione["colpi"] -= 1

    # ELIMINA SE FINITI

    if previsione["colpi"] <= 0:
        continue

    nuovo_storico.append(previsione)

# =========================================
# AGGIUNGI NUOVI JOLLY
# =========================================

for j in jolly:

    esiste = False

    for s in nuovo_storico:

        if (
            s["ruota"] == j["ruota"]
            and
            s["ambo"] == j["ambo"]
        ):

            esiste = True
            break

    if not esiste:

        nuovo_storico.append({

            "ruota": j["ruota"],
            "ambo": j["ambo"],
            "score": j["score"],
            "ultima": j["ultima"],
            "colpi": COLPI_VALIDITA

        })

# =========================================
# RUOTE ORDINATE
# =========================================

ruote_ordinate = sorted(

    risultati,

    key=lambda x: ORDINE_RUOTE.index(
        x["ruota"]
    )

)

# =========================================
# OUTPUT
# =========================================

output = {

    "ruote": ruote_ordinate,

    "jolly": jolly,

    "ambo_forte": ambo_forte,

    "previsioni_attive": nuovo_storico

}

# =========================================
# SALVA STORICO
# =========================================

with open(
    STORICO_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        nuovo_storico,
        f,
        indent=2,
        ensure_ascii=False
    )

# =========================================
# SALVA RISULTATI
# =========================================

with open(
    "risultati.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print("RISULTATI GENERATI")
print(
    "PREVISIONI ATTIVE:",
    len(nuovo_storico)
)