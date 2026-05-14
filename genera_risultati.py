import json

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    estrazioni = json.load(f)

# =========================
# FUNZIONI
# =========================

def modulo90(n):
    n = n % 90
    return 90 if n == 0 else n

def distanza(a, b):
    return modulo90(abs(a - b))

# =========================
# GENERA NUMERI CICLICI
# =========================

def genera_ciclo(numeri):

    risultati = []

    for i in range(len(numeri)):

        a = numeri[i]
        b = numeri[(i + 1) % len(numeri)]

        # SOMMA CICLICA
        somma = modulo90(a + b)

        # DISTANZA
        dist = distanza(a, b)

        # CHIUSURA INVERSA
        inv = modulo90(90 - dist)

        risultati.append(somma)
        risultati.append(dist)
        risultati.append(inv)

    return risultati

# =========================
# CREA AMBO
# =========================

def crea_ambo(numeri_estratti):

    candidati = genera_ciclo(numeri_estratti)

    # ELIMINA NUMERI GIÀ USCITI
    candidati = [
        n for n in candidati
        if n not in numeri_estratti
    ]

    # CONTA FREQUENZE
    frequenze = {}

    for n in candidati:
        frequenze[n] = frequenze.get(n, 0) + 1

    # ORDINA
    ordinati = sorted(
        frequenze.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # PRENDE I MIGLIORI
    migliori = [x[0] for x in ordinati[:2]]

    # SICUREZZA
    if len(migliori) < 2:

        for n in range(1, 91):

            if n not in migliori and n not in numeri_estratti:
                migliori.append(n)

            if len(migliori) == 2:
                break

    # SCORE
    score = sum(frequenze.get(n, 0) for n in migliori)

    return migliori, score

# =========================
# ANALISI RUOTE
# =========================

ruote = []

for ruota, lista in estrazioni.items():

    ultima = lista[-1]

    ambo, score = crea_ambo(ultima)

    ruote.append({
        "ruota": ruota,
        "ambo": ambo,
        "score": score,
        "estrazione": ultima
    })

# =========================
# ORDINA
# =========================

ruote.sort(
    key=lambda x: x["score"],
    reverse=True
)

# =========================
# TOP
# =========================

top = ruote[:3]

# =========================
# JOLLY
# =========================

jolly = top[0]

# =========================
# RISULTATO FINALE
# =========================

risultati = {
    "top": top,
    "jolly": jolly,
    "ruote": ruote
}

# =========================
# SALVA JSON
# =========================

with open("risultati.json", "w", encoding="utf-8") as f:

    json.dump(
        risultati,
        f,
        indent=4,
        ensure_ascii=False
    )

print("RISULTATI GENERATI")