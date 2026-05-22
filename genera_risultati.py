import json

# =========================
# CONFIG
# =========================

COLPI_VALIDITA = 8

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# GENERA AMBO
# =========================

def genera_ambo(ultima, storico_ruota):

    frequenze = {}

    # analizza ultime 15 estrazioni
    recenti = storico_ruota[-15:]

    for estrazione in recenti:

        for numero in estrazione:

            frequenze[numero] = frequenze.get(numero, 0) + 1

    # ordina per frequenza
    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    ambo = []

    # evita numeri usciti nell'ultima estrazione
    for numero, freq in ordinati:

        if numero not in ultima:

            ambo.append(numero)

        if len(ambo) == 2:
            break

    # sicurezza
    if len(ambo) < 2:

        for n in range(1, 91):

            if n not in ultima and n not in ambo:
                ambo.append(n)

            if len(ambo) == 2:
                break

    # score
    score_totale = 0

    for numero in ambo:
        score_totale += frequenze.get(numero, 1)

    score_finale = score_totale

    return ambo, score_finale

# =========================
# CALCOLO COLPI RIMANENTI
# =========================

def calcola_colpi_rimanenti(storico_ruota, ambo):

    colpi = 0

    storico_inverso = storico_ruota[::-1]

    for estrazione in storico_inverso:

        colpi += 1

        if ambo[0] in estrazione or ambo[1] in estrazione:
            break

    rimanenti = COLPI_VALIDITA - colpi

    if rimanenti < 0:
        rimanenti = 0

    return rimanenti

# =========================
# ANALISI RUOTE
# =========================

risultati = []

for ruota, storico in estrazioni.items():

    # prende l'ultima estrazione
    ultima = storico[-1]

    # genera ambo
    ambo, score = genera_ambo(ultima, storico)

    # calcola colpi
    colpi_rimasti = calcola_colpi_rimanenti(storico, ambo)

    risultati.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "estrazione": ultima,
        "colpi_rimasti": colpi_rimasti
    })

# =========================
# ORDINA PER SCORE
# =========================

risultati_ordinati = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)

# =========================
# JOLLY
# SOLO PREVISIONI FRESCHE
# =========================

jolly = [
    r for r in risultati_ordinati
    if r["colpi_rimasti"] >= 4
][:3]

# =========================
# AMBO FORTE
# =========================

ambo_forte = [
    r for r in risultati_ordinati
    if r["colpi_rimasti"] > 0
][:10]

# =========================
# OUTPUT JSON
# =========================

output = {
    "tutte": risultati_ordinati,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

# =========================
# SALVA FILE
# =========================

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("risultati.json generato correttamente")
