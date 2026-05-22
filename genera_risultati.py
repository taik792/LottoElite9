import json
import os

# =====================================================
# CONFIG
# =====================================================

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

# =====================================================
# CARICA ESTRAZIONI
# =====================================================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =====================================================
# CREA STORICO
# =====================================================

if os.path.exists(STORICO_FILE):

    with open(STORICO_FILE, "r", encoding="utf-8") as f:
        storico_previsioni = json.load(f)

else:

    storico_previsioni = []

# =====================================================
# FUNZIONI CICLOMETRICHE
# =====================================================

def distanza_ciclica(a, b):

    d = abs(a - b)

    return min(d, 90 - d)

# -----------------------------------------------------

def vertibile(numero):

    s = str(numero).zfill(2)

    return int(s[::-1])

# -----------------------------------------------------

def complementare(numero):

    return 90 - numero

# -----------------------------------------------------

def stessa_finale(a, b):

    return a % 10 == b % 10

# -----------------------------------------------------

def stessa_decina(a, b):

    return a // 10 == b // 10

# =====================================================
# MOTORE CICLOMETRICO
# =====================================================

def analizza_ciclometria(ruota, storico):

    score_numeri = {}

    ultime = storico[-12:]

    # =========================================
    # ANALISI DISTANZE
    # =========================================

    for estrazione in ultime:

        for i in range(len(estrazione)):

            for j in range(i + 1, len(estrazione)):

                n1 = estrazione[i]
                n2 = estrazione[j]

                dist = distanza_ciclica(n1, n2)

                # DISTANZA IMPORTANTE

                if dist in [9, 18, 27, 45]:

                    score_numeri[n1] = (
                        score_numeri.get(n1, 0) + 4
                    )

                    score_numeri[n2] = (
                        score_numeri.get(n2, 0) + 4
                    )

                # VERTIBILI

                if vertibile(n1) == n2:

                    score_numeri[n1] = (
                        score_numeri.get(n1, 0) + 5
                    )

                    score_numeri[n2] = (
                        score_numeri.get(n2, 0) + 5
                    )

                # COMPLEMENTARI

                if complementare(n1) == n2:

                    score_numeri[n1] = (
                        score_numeri.get(n1, 0) + 3
                    )

                    score_numeri[n2] = (
                        score_numeri.get(n2, 0) + 3
                    )

                # STESSA FINALE

                if stessa_finale(n1, n2):

                    score_numeri[n1] = (
                        score_numeri.get(n1, 0) + 2
                    )

                    score_numeri[n2] = (
                        score_numeri.get(n2, 0) + 2
                    )

                # STESSA DECINA

                if stessa_decina(n1, n2):

                    score_numeri[n1] = (
                        score_numeri.get(n1, 0) + 1
                    )

                    score_numeri[n2] = (
                        score_numeri.get(n2, 0) + 1
                    )

    # =========================================
    # FREQUENZA RECENTE
    # =========================================

    for estrazione in ultime:

        for numero in estrazione:

            score_numeri[numero] = (
                score_numeri.get(numero, 0) + 1
            )

    # =========================================
    # ORDINE SCORE
    # =========================================

    ordinati = sorted(

        score_numeri.items(),

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

# =====================================================
# CALCOLA COLPI
# =====================================================

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

    rimanenti = (
        COLPI_VALIDITA - colpi_passati
    )

    if rimanenti < 0:
        rimanenti = 0

    return rimanenti

# =====================================================
# GENERA RISULTATI
# =====================================================

risultati = []

for ruota in ORDINE_RUOTE:

    storico = estrazioni[ruota]

    ultima = storico[-1]

    ambo, score = analizza_ciclometria(
        ruota,
        storico
    )

    # EVITA NUMERI USCITI

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

        "ruota": ru