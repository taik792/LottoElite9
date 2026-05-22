import json
from collections import Counter

# =========================
# CONFIG
# =========================

RUOTE_GEMELLE = {
    "Bari": "Cagliari",
    "Cagliari": "Bari",
    "Firenze": "Roma",
    "Roma": "Firenze",
    "Genova": "Milano",
    "Milano": "Genova",
    "Napoli": "Palermo",
    "Palermo": "Napoli",
    "Torino": "Venezia",
    "Venezia": "Torino"
}

DISTANZE = [9, 18, 27, 45]

# =========================
# FUNZIONI
# =========================

def distanza_ciclica(n, d):
    return ((n + d - 1) % 90) + 1

def speculare(n):
    s = str(n).zfill(2)
    return int(s[::-1])

def normalizza(n):
    while n > 90:
        n -= 90
    if n == 0:
        n = 90
    return n

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    archivio = json.load(f)

risultati = []

# =========================
# ANALISI RUOTE
# =========================

for ruota, estrazioni in archivio.items():

    ultime = estrazioni[-12:]
    ultima = estrazioni[-1]

    score_numeri = Counter()

    # -------------------------
    # ANALISI CICLICA
    # -------------------------

    for estrazione in ultime:

        for numero in estrazione:

            # DISTANZE CICLICHE
            for d in DISTANZE:
                candidato = distanza_ciclica(numero, d)
                score_numeri[candidato] += 2

            # SPECULARE
            spec = speculare(numero)
            if spec != numero:
                score_numeri[spec] += 1

    # -------------------------
    # SOMME CICLICHE
    # -------------------------

    for estrazione in ultime:

        for i in range(len(estrazione)):
            for j in range(i + 1, len(estrazione)):

                somma = normalizza(estrazione[i] + estrazione[j])
                score_numeri[somma] += 2

    # -------------------------
    # RUOTA GEMELLA
    # -------------------------

    gemella = RUOTE_GEMELLE.get(ruota)

    if gemella and gemella in archivio:

        ultime_gemella = archivio[gemella][-6:]

        for estrazione in ultime_gemella:

            for numero in estrazione:

                for d in [9, 18]:
                    candidato = distanza_ciclica(numero, d)
                    score_numeri[candidato] += 2

    # -------------------------
    # FILTRO NUMERI USCITI
    # -------------------------

    numeri_recenti = set()

    for estrazione in ultime[-3:]:
        numeri_recenti.update(estrazione)

    filtrati = {
        n: s
        for n, s in score_numeri.items()
        if n not in numeri_recenti
    }

    # -------------------------
    # TOP 2 NUMERI
    # -------------------------

    top = sorted(
        filtrati.items(),
        key=lambda x: x[1],
        reverse=True
    )[:2]

    if len(top) < 2:
        continue

    ambo = [top[0][0], top[1][0]]
    score = top[0][1] + top[1][1]

    risultati.append({
        "ru