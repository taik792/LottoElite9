import json
import os

COLPI_VALIDITA = 5

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# STORICO PREVISIONI
# =========================

STORICO_FILE = "storico_previsioni.json"

if os.path.exists(STORICO_FILE):
    with open(STORICO_FILE, "r", encoding="utf-8") as f:
        storico_previsioni = json.load(f)
else:
    storico_previsioni = []

# =========================
# RUOTE
# =========================

ruote = [
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
# ANALISI AMBO
# =========================

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

    numeri = [n[0] for n in ordinati[:2]]

    score = sum(n[1] for n in ordinati[:2])

    return numeri, score

# =========================
# CALCOLO COLPI
# =========================

def calcola_colpi(ruota, ambo):

    storico = estrazioni[ruota][-COLPI_VALIDITA:]

    colpi = 0

    for estrazione in reversed(storico):

        if ambo[0] in estrazione or ambo[1] in estrazione:
            break

        colpi += 1

    rimanenti = COLPI_VALIDITA - colpi

    if rimanenti < 0:
        rimanenti = 0

    return rimanenti

# =========================
# NUOVE PREVISIONI
# =========================

risultati = []

for ruota in ruote:

    storico = estrazioni[ruota]

    ultima = storico[-1]

    ambo, score = analizza_ambo(storico)

    # evita numeri usciti ultima estrazione

    if ambo[0] in ultima or ambo[1] in ultima:
        continue

    colpi = calcola_colpi(ruota, ambo)

    risultati.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "ultima": ultima,
        "colpi": colpi
    })

# =========================
# ORDINE SCORE
# =========================

risultati.sort(
    key=lambda x: x["score"],
    reverse=True
)

# =========================
# JOLLY
# =========================

jolly = risultati[:3]

# =========================
# AMBO FORTE
# =========================

ambo_forte = [
    r for r in risultati
    if r["score"] >= 6
]

# =========================
# AGGIORNA PREVISIONI ATTIVE
# =========================

nuovo_storico = []

for previsione in storico_previsioni:

    ruota = previsione["ruota"]
    ambo = previsione["ambo"]

    ultima = estrazioni[ruota][-1]

    # se esce elimina

    if ambo[0] in ultima or ambo[1] in ultima:
        continue

    previsione["colpi"] -= 1

    # se finiti elimina

    if previsione["colpi"] <= 0:
        continue

    nuovo_storico.append(previsione)

# aggiungi nuovi jolly

for j in jolly:

    esiste = False

    for s in nuovo_storico:

        if (
            s["ruota"] == j["ruota"]
            and s["ambo"] == j["ambo"]
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

# =========================
# SALVA STORICO
# =========================

with open(STORICO_FILE, "w", encoding="utf-8") as f:
    json.dump(
        nuovo_storico,
        f,
        indent=2,
        ensure_ascii=False
    )

# =========================
# OUTPUT FINALE
# =========================

output = {
    "ruote": risultati,
    "jolly": jolly,
    "ambo_forte": ambo_forte,
    "previsioni_attive": nuovo_storico
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print("RISULTATI GENERATI")
print("PREVISIONI ATTIVE:", len(nuovo_storico))