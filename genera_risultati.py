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

DISTANZE_FORTI = [9, 18, 27, 45]

COLPI_VALIDITA = 6

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# FUNZIONI CICLICHE
# =========================

def normalizza(n):

    while n > 90:
        n -= 90

    while n < 1:
        n += 90

    return n


def distanza_ciclica(a, b):

    dist = abs(a - b)

    if dist > 45:
        dist = 90 - dist

    return dist


def complementare90(n):

    comp = 90 - n

    if comp == 0:
        comp = 90

    return comp


def vertibile(n):

    if n < 10:
        return n

    return int(str(n)[::-1])


# =========================
# MOTORE CICLOMETRICO
# =========================

def genera_previsione(storico, ultima_estrazione):

    convergenze = Counter()

    archivio = []

    for estr in storico:
        archivio.extend(estr)

    # =====================
    # ANALISI CICLICA
    # =====================

    for numero in archivio:

        # DISTANZE CICLICHE
        for d in DISTANZE_FORTI:

            avanti = normalizza(numero + d)
            dietro = normalizza(numero - d)

            convergenze[avanti] += 2
            convergenze[dietro] += 2

        # COMPLEMENTARE
        comp = complementare90(numero)
        convergenze[comp] += 3

        # VERTIBILE
        v = vertibile(numero)

        if v != numero:
            convergenze[v] += 2

    # =====================
    # ELIMINA NUMERI USCITI
    # =====================

    candidati = []

    ordinati = convergenze.most_common()

    for numero, score in ordinati:

        if numero not in ultima_estrazione:
            candidati.append((numero, score))

    # =====================
    # CREA AMBO
    # =====================

    ambo = []

    score_totale = 0

    for numero, score in candidati:

        if numero not in ambo:

            ambo.append(numero)
            score_totale += score

        if len(ambo) == 2:
            break

    score_finale = score_totale // 2

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

for ruota in RUOTE_ORDINE:

    storico_ruota = estrazioni[ruota]

    ultime_10 = storico_ruota[-10:]

    ultima_estrazione = storico_ruota[-1]

    ambo, score = genera_previsione(
        ultime_10,
        ultima_estrazione
    )

    colpi_rimanenti = calcola_colpi_rimanenti(
        storico_ruota,
        ambo
    )

    risultati.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "colpi": colpi_rimanenti,
        "estrazione": ultima_estrazione
    })

# =========================
# ORDINA PER SCORE
# =========================

ordinati = sorted(
    risultati,
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
    if r["score"] >= 12
]

# =========================
# SALVA JSON
# =========================

output = {
    "tutte": risultati,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Motore ciclometrico evoluto creato.")
