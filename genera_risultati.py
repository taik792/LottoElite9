import json
import os
from collections import Counter

# =========================================================
# LOTTO ELITE PRO - MOTORE CICLOMETRICO REALE
# =========================================================

COLPI_VALIDITA = 5

STORICO_FILE = "storico_previsioni.json"

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

DISTANZE_FORTI = [9, 18, 27, 45]

# =========================================================
# CARICA ESTRAZIONI
# =========================================================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================================================
# CREA STORICO
# =========================================================

if os.path.exists(STORICO_FILE):

    with open(STORICO_FILE, "r", encoding="utf-8") as f:
        storico_previsioni = json.load(f)

else:

    storico_previsioni = []

# =========================================================
# FUNZIONI CICLOMETRICHE
# =========================================================

def normalizza(n):

    while n > 90:
        n -= 90

    while n < 1:
        n += 90

    return n

# ---------------------------------------------------------

def distanza(a, b):

    d = abs(a - b)

    if d > 45:
        d = 90 - d

    return d

# ---------------------------------------------------------

def vertibile(n):

    s = str(n).zfill(2)

    return int(s[::-1])

# ---------------------------------------------------------

def complementare(n):

    c = 90 - n

    if c == 0:
        c = 90

    return c

# ---------------------------------------------------------

def somma90(a, b):

    return normalizza(a + b)

# ---------------------------------------------------------

def differenza90(a, b):

    return normalizza(abs(a - b))

# ---------------------------------------------------------

def stessa_finale(a, b):

    return a % 10 == b % 10

# ---------------------------------------------------------

def stessa_decina(a, b):

    return a // 10 == b // 10

# =========================================================
# MOTORE CICLOMETRICO
# =========================================================

def analizza_ciclometria(ruota, storico):

    score = Counter()

    ultime = storico[-12:]

    archivio = []

    for estrazione in ultime:
        archivio.extend(estrazione)

    # =====================================================
    # DISTANZE CICLICHE
    # =====================================================

    for i in range(len(archivio)):

        for j in range(i + 1, len(archivio)):

            n1 = archivio[i]
            n2 = archivio[j]

            dist = distanza(n1, n2)

            if dist in DISTANZE_FORTI:

                score[n1] += 5
                score[n2] += 5

                # numeri derivati

                score[normalizza(n1 + dist)] += 3
                score[normalizza(n2 + dist)] += 3

    # =====================================================
    # VERTIBILI
    # =====================================================

    for n in archivio:

        v = vertibile(n)

        if v != n:

            score[v] += 4

    # =====================================================
    # COMPLEMENTARI
    # =====================================================

    for n in archivio:

        c = complementare(n)

        score[c] += 3

    # =====================================================
    # SOMME CICLICHE
    # =====================================================

    for i in range(len(archivio)):

        for j in range(i + 1, len(archivio)):

            s = somma90(
                archivio[i],
                archivio[j]
            )

            score[s] += 4

    # =====================================================
    # DIFFERENZE CICLICHE
    # =====================================================

    for i in range(len(archivio)):

        for j in range(i + 1, len(archivio)):

            d = differenza90(
                archivio[i],
                archivio[j]
            )

            score[d] += 4

    # =====================================================
    # FINALI UGUALI
    # =====================================================

    for i in range(len(archivio)):

        for j in range(i + 1, len(archivio)):

            a = archivio[i]
            b = archivio[j]

            if stessa_finale(a, b):

                score[a] += 2
                score[b] += 2

    # =====================================================
    # DECINE UGUALI
    # =====================================================

    for i in range(len(archivio)):

        for j in range(i + 1, len(archivio)):

            a = archivio[i]
            b = archivio[j]

            if stessa_decina(a, b):

                score[a] += 1
                score[b] += 1

    # =====================================================
    # FREQUENZE RECENTI
    # =====================================================

    frequenze = Counter(archivio)

    for numero, freq in frequenze.items():

        score[numero] += freq

    # =====================================================
    # ORDINA
    # =====================================================

    ordinati = sorted(
        score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    if len(ordinati) < 2:
        return [1, 90], 0

    ambo = [
        ordinati[0][0],
        ordinati[1][0]
    ]

    score_finale = (
        ordinati[0][1]
        +
        ordinati[1][1]
    )

    return ambo, score_finale

# =========================================================
# CALCOLA COLPI
# =========================================================

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

# =========================================================
# GENERA RISULTATI
# =========================================================

risultati = []

for ruota in ORDINE_RUOTE:

    storico = estrazioni[ruota]

    ultima = storico[-1]

    ambo, score_finale = analizza_ciclometria(
        ruota,
        storico
    )

    # elimina numeri usciti

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
        "score": score_finale,
        "ultima": ultima,
        "colpi": colpi

    })

# =========================================================
# ORDINA SCORE
# =========================================================

risultati_score = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)

# =========================================================
# JOLLY
# =========================================================

jolly = [

    r for r in risultati_score

    if r["colpi"] >= 4

][:3]

# =========================================================
# AMBO FORTE
# =========================================================

ambo_forte = [

    r for r in risultati_score

    if r["score"] >= 40

][:10]

# =========================================================
# AGGIORNA STORICO
# =========================================================

nuovo_storico = []

for previsione in storico_previsioni:

    ruota = previsione["ruota"]

    ambo = previsione["ambo"]

    ultima = estrazioni[ruota][-1]

    # elimina se uscito

    if (
        ambo[0] in ultima
        or
        ambo[1] in ultima
    ):
        continue

    previsione["colpi"] -= 1

    if previsione["colpi"] <= 0:
        continue

    nuovo_storico.append(previsione)

# =========================================================
# AGGIUNGI NUOVI JOLLY
# =========================================================

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

# =========================================================
# RUOTE ORDINATE
# =========================================================

ruote_ordinate = sorted(
    risultati,
    key=lambda x: ORDINE_RUOTE.index(
        x["ruota"]
    )
)

# =========================================================
# OUTPUT
# =========================================================

output = {

    "ruote": ruote_ordinate,

    "jolly": jolly,

    "ambo_forte": ambo_forte,

    "previsioni_attive": nuovo_storico

}

# =========================================================
# SALVA STORICO
# =========================================================

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

# =========================================================
# SALVA RISULTATI
# =========================================================

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

print("LOTTO ELITE PRO - MOTORE CICLOMETRICO REALE GENERATO")
print("PREVISIONI ATTIVE:", len(nuovo_storico))