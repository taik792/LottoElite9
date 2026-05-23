import json
from collections import Counter

COLPI_VALIDITA = 5

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

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

# =========================
# FUNZIONI
# =========================

def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)

def vertibile(n):
    s = str(n).zfill(2)
    return int(s[::-1])

def frequenza_numero(storico, numero, ultime=12):
    count = 0

    for estrazione in storico[-ultime:]:
        if numero in estrazione:
            count += 1

    return count

def calcola_colpi(storico, ambo):

    storico_recente = storico[::-1]

    colpi = 0

    for estrazione in storico_recente:

        if ambo[0] in estrazione or ambo[1] in estrazione:
            break

        colpi += 1

    rimanenti = COLPI_VALIDITA - colpi

    if rimanenti < 0:
        rimanenti = 0

    return rimanenti

# =========================
# ANALISI CICLOMETRICA
# =========================

def analizza_ruota(nome_ruota, storico):

    conteggio_ambi = Counter()

    ultime = storico[-18:]

    for estrazione in ultime:

        numeri = estrazione[:5]

        for i in range(len(numeri)):
            for j in range(i + 1, len(numeri)):

                a = numeri[i]
                b = numeri[j]

                dist = distanza(a, b)

                candidato1 = (a + dist) % 90
                candidato2 = (b + dist) % 90

                if candidato1 == 0:
                    candidato1 = 90

                if candidato2 == 0:
                    candidato2 = 90

                ambi = [
                    tuple(sorted((candidato1, candidato2))),
                    tuple(sorted((vertibile(candidato1), candidato2))),
                    tuple(sorted((candidato1, vertibile(candidato2))))
                ]

                for ambo in ambi:

                    score = 0

                    # distanza forte
                    if distanza(ambo[0], ambo[1]) <= 18:
                        score += 120

                    # vertibili
                    if vertibile(ambo[0]) == ambo[1]:
                        score += 180

                    # somma ciclometrica
                    if (ambo[0] + ambo[1]) % 9 == 0:
                        score += 90

                    # numeri consecutivi
                    if abs(ambo[0] - ambo[1]) <= 9:
                        score += 70

                    # penalità numeri troppo usciti
                    freq1 = frequenza_numero(storico, ambo[0])
                    freq2 = frequenza_numero(storico, ambo[1])

                    score -= freq1 * 25
                    score -= freq2 * 25

                    # bonus numeri poco usciti
                    if freq1 <= 1:
                        score += 40

                    if freq2 <= 1:
                        score += 40

                    # penalità se già usciti insieme
                    for estr in ultime[-10:]:

                        if ambo[0] in estr and ambo[1] in estr:
                            score -= 200

                    conteggio_ambi[ambo] += score

    migliori = conteggio_ambi.most_common(1)

    if not migliori:
        return None

    ambo, score = migliori[0]

    colpi = calcola_colpi(storico, ambo)

    return {
        "ruota": nome_ruota,
        "ambo": list(ambo),
        "score": int(score),
        "colpi_rimanenti": colpi,
        "ultima_estrazione": storico[-1]
    }

# =========================
# GENERA RISULTATI
# =========================

risultati = []

for ruota in RUOTE_ORDINE:

    if ruota not in estrazioni:
        continue

    risultato = analizza_ruota(
        ruota,
        estrazioni[ruota]
    )

    if risultato:
        risultati.append(risultato)

# =========================
# ORDINE SCORE
# =========================

jolly = sorted(
    risultati,
    key=lambda x: x["score"],
    reverse=True
)[:3]

ambo_forte = sorted(
    risultati,
    key=lambda x: (
        x["score"],
        x["colpi_rimanenti"]
    ),
    reverse=True
)[:5]

# =========================
# OUTPUT
# =========================

output = {
    "ruote": risultati,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

with open("risultati.json", "w") as f:
    json.dump(output, f, indent=2)

print("Risultati generati.")
