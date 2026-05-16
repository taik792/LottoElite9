# ======================================================
# LOTTO ELITE PRO - MOTORE 10 PRO ADATTIVO
# Versione Python
# genera_risultati.py
# ======================================================

import json

# ==========================
# CARICA ESTRAZIONI
# ==========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# ultime 12 estrazioni
ultime = estrazioni[-12:]

# ==========================
# FUNZIONI
# ==========================

def fuori90(n):
    while n > 90:
        n -= 90

    while n < 1:
        n += 90

    return n


def distanza90(a, b):
    d = abs(a - b)
    return min(d, 90 - d)


def complementare90(n):
    return fuori90(90 - n)


def frequenza_numero(numero, ruota_estrazioni):

    count = 0

    for estr in ruota_estrazioni:
        if numero in estr["numeri"]:
            count += 1

    return count


# ==========================
# COSTRUZIONE ARCHIVIO RUOTE
# ==========================

archivio_ruote = {}

for estrazione in ultime:

    for ruota, numeri in estrazione["ruote"].items():

        if ruota not in archivio_ruote:
            archivio_ruote[ruota] = []

        archivio_ruote[ruota].append({
            "data": estrazione["data"],
            "numeri": numeri
        })


# ==========================
# GENERATORE AMBI
# ==========================

def genera_ambi(ruota, dati_ruota):

    ultima = dati_ruota[-1]
    penultima = dati_ruota[-2]

    ultimi_numeri = ultima["numeri"]
    vecchi_numeri = penultima["numeri"]

    candidati = []

    # ==========================
    # DERIVATI CICLICI
    # ==========================

    for i in range(len(ultimi_numeri)):

        n = ultimi_numeri[i]

        candidati.append(fuori90(n + 9))
        candidati.append(fuori90(n - 9))

        candidati.append(fuori90(n + 18))
        candidati.append(fuori90(n - 18))

        candidati.append(complementare90(n))

        # media dinamica
        media = round((n + vecchi_numeri[i]) / 2)
        candidati.append(fuori90(media))

        # distanza ciclica
        dist = distanza90(n, vecchi_numeri[i])
        candidati.append(fuori90(n + dist))

    # ==========================
    # PULIZIA
    # ==========================

    candidati = [
        n for n in candidati
        if 1 <= n <= 90
    ]

    # elimina numeri appena usciti
    candidati = [
        n for n in candidati
        if n not in ultimi_numeri
    ]

    # ==========================
    # SCORE DINAMICO
    # ==========================

    score_map = {}

    for n in candidati:

        score = 0

        # frequenza recente
        freq = frequenza_numero(n, dati_ruota)

        # meno frequente = più forte
        score += (12 - freq)

        # vicinanza ciclica
        for e in ultimi_numeri:

            d = distanza90(n, e)

            if d <= 9:
                score += 2

            if d <= 5:
                score += 2

        # bonus complementare
        if complementare90(n) in ultimi_numeri:
            score += 3

        score_map[n] = score

    # ==========================
    # ORDINA
    # ==========================

    ordinati = sorted(
        score_map.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # ==========================
    # CREA AMBI
    # ==========================

    risultati = []

    i = 0

    while i < len(ordinati) - 1:

        n1 = ordinati[i][0]
        n2 = ordinati[i + 1][0]

        if n1 != n2:

            score = round(
                (ordinati[i][1] + ordinati[i + 1][1]) / 2
            )

            risultati.append({
                "ruota": ruota,
                "ambo": [n1, n2],
                "score": score,
                "estrazione": ultimi_numeri
            })

        if len(risultati) >= 3:
            break

        i += 2

    return risultati


# ==========================
# GENERAZIONE COMPLETA
# ==========================

top = []
jolly = []
ambo_forte = []

for ruota, dati_ruota in archivio_ruote.items():

    risultati = genera_ambi(
        ruota,
        dati_ruota
    )

    if len(risultati) > 0:
        top.append(risultati[0])

    if len(risultati) > 1:
        jolly.append(risultati[1])

    if len(risultati) > 2:
        ambo_forte.append(risultati[2])

# ==========================
# ORDINA SCORE
# ==========================

top.sort(
    key=lambda x: x["score"],
    reverse=True
)

jolly.sort(
    key=lambda x: x["score"],
    reverse=True
)

ambo_forte.sort(
    key=lambda x: x["score"],
    reverse=True
)

# ==========================
# OUTPUT
# ==========================

output = {
    "top": top,
    "jolly": jolly,
    "amboForte": ambo_forte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )

print("✅ MOTORE 10 PRO GENERATO")