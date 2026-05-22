import json
from collections import Counter, defaultdict

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

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# FUNZIONI CICLICHE
# =========================

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

    s = str(n)

    return int(s[::-1])


def normalizza(n):

    while n > 90:
        n -= 90

    while n < 1:
        n += 90

    return n


# =========================
# MOTORE CICLOMETRICO
# =========================

def genera_previsione(storico, ultima_estrazione):

    numeri = []

    for estr in storico:
        numeri.extend(estr)

    convergenze = Counter()

    # =====================
    # ANALISI CICLICA
    # =====================

    for n in numeri:

        # DISTANZE CICLICHE
        for d in DISTANZE_FORTI:

            n1 = normalizza(n + d)
            n2 = normalizza(n - d)

            convergenze[n1] += 2
            convergenze[n2] += 2

        # COMPLEMENTARE A 90
        comp = complementare90(n)
        convergenze[comp] += 3

        # VERTIBILE
        v = vertibile(n)

        if v != n:
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

    totale_score = 0

    for numero, score in candidati:

        if numero not in ambo:

            ambo.append(numero)
            totale_score += score

        if len(ambo) == 2:
            break

    score_finale = totale_score // 2

    return ambo, score_finale


# =========================
# ANALISI RUOTE
# =========================

risultati = []

for ruota in RUOTE_ORDINE:

    storico_ruota = estrazioni[ruota]

    # ultime 10 estrazioni
    ultime_10 = storico_ruota[-10:]

    ultima_estrazione = storico_ruota[-1]

    ambo, score = genera_previsione(
        ultime_10,
        ultima_estrazione
    )

    risultati.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
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
# OUTPUT
# =========================

output = {
    "tutte": risultati,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("Motore ciclometrico evoluto generato.")
