import json
from itertools import combinations

# =========================
# CONFIG
# =========================

TOP_JOLLY = 3
TOP_FORTE = 5
COLPI_VALIDITA = 6

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# FUNZIONI
# =========================

def frequenza(numero, storico):

    conta = 0

    for estrazione in storico[-20:]:

        if numero in estrazione:
            conta += 1

    return conta


def ritardo(numero, storico):

    colpi = 0

    for estrazione in reversed(storico):

        colpi += 1

        if numero in estrazione:
            return colpi

    return 50


def distanza_ciclica(n1, n2):

    d = abs(n1 - n2)

    return min(d, 90 - d)


def score_ambo(n1, n2, storico):

    score = 0

    # =========================
    # FREQUENZA
    # =========================

    f1 = frequenza(n1, storico)
    f2 = frequenza(n2, storico)

    score += (f1 + f2) * 12

    # =========================
    # RITARDO
    # =========================

    r1 = ritardo(n1, storico)
    r2 = ritardo(n2, storico)

    score += (r1 + r2) * 8

    # =========================
    # DISTANZE CICLOMETRICHE
    # =========================

    distanza = distanza_ciclica(n1, n2)

    if distanza in [9, 18, 27, 36, 45]:
        score += 220

    elif distanza in [5, 10, 15]:
        score += 120

    elif distanza <= 2:
        score += 40

    # =========================
    # ASSENZA RECENTE
    # =========================

    uscito_recente = False

    for estrazione in storico[-6:]:

        if n1 in estrazione and n2 in estrazione:
            uscito_recente = True
            break

    if not uscito_recente:
        score += 180

    # =========================
    # RITORNO PERIODICO
    # =========================

    intervalli = []

    ultimo = None

    for idx, estrazione in enumerate(storico):

        if n1 in estrazione or n2 in estrazione:

            if ultimo is not None:
                intervalli.append(idx - ultimo)

            ultimo = idx

    if len(intervalli) >= 2:

        media = sum(intervalli) / len(intervalli)

        if 4 <= media <= 12:
            score += 200

    # =========================
    # PENALITA NUMERI VICINI
    # =========================

    if abs(n1 - n2) == 1:
        score -= 180

    return int(score)


def calcola_colpi_rimanenti(storico, ambo):

    colpi = 0

    storico_inverso = storico[::-1]

    for estrazione in storico_inverso:

        colpi += 1

        if ambo[0] in estrazione or ambo[1] in estrazione:
            break

    rimanenti = COLPI_VALIDITA - colpi

    if rimanenti < 0:
        rimanenti = 0

    return rimanenti


# =========================
# ANALISI PRINCIPALE
# =========================

risultati = []

ambi_usati = set()

for ruota, storico in estrazioni.items():

    numeri = list(range(1, 91))

    migliori = []

    for n1, n2 in combinations(numeri, 2):

        ambo_ordinato = tuple(sorted([n1, n2]))

        # evita ambi duplicati
        if ambo_ordinato in ambi_usati:
            continue

        score = score_ambo(n1, n2, storico)

        migliori.append({

            "ambo": [n1, n2],
            "score": score

        })

    migliori = sorted(
        migliori,
        key=lambda x: x["score"],
        reverse=True
    )

    previsione_valida = None

    for candidato in migliori:

        colpi = calcola_colpi_rimanenti(
            storico,
            candidato["ambo"]
        )

        # prende solo ambi ancora vivi
        if colpi > 0:

            previsione_valida = {

                "ruota": ruota,

                "ambo": candidato["ambo"],

                "score": candidato["score"],

                "ultima_estrazione": storico[-1],

                "colpi_rimanenti": colpi

            }

            ambi_usati.add(
                tuple(sorted(candidato["ambo"]))
            )

            break

    # fallback sicurezza
    if previsione_valida is None:

        previsione_valida = {

            "ruota": ruota,

            "ambo": [1, 90],

            "score": 0,

            "ultima_estrazione": storico[-1],

            "colpi_rimanenti": 0
        }

    risultati.append(previsione_valida)

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

risultati_ordinati = []

for nome in ordine_ruote:

    for r in risultati:

        if r["ruota"] == nome:
            risultati_ordinati.append(r)

# =========================
# JOLLY
# =========================

jolly = sorted(

    [r for r in risultati if r["colpi_rimanenti"] > 0],

    key=lambda x: x["score"],

    reverse=True

)[:TOP_JOLLY]

# =========================
# AMBO FORTE
# =========================

ambo_forte = sorted(

    [r for r in risultati if r["colpi_rimanenti"] > 0],

    key=lambda x: x["score"],

    reverse=True

)[:TOP_FORTE]

# =========================
# PREVISIONI ATTIVE
# =========================

previsioni_attive = [

    r for r in risultati
    if r["colpi_rimanenti"] > 0

]

# =========================
# OUTPUT JSON
# =========================

output = {

    "ruote": risultati_ordinati,

    "jolly": jolly,

    "ambo_forte": ambo_forte,

    "previsioni_attive": previsioni_attive

}

with open("risultati.json", "w", encoding="utf-8") as f:

    json.dump(
        output,
        f,
        indent=4,
        ensure_ascii=False
    )

print("risultati.json generato correttamente")
