import json

# ==========================================
# FUNZIONI CICLICHE
# ==========================================

def somma90(n):
    return n - 90 if n > 90 else n

def speculare(n):
    return 91 - n

def distanza(a, b):
    return abs(a - b)

# ==========================================
# CARICA ESTRAZIONI
# ==========================================

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "jolly": {},
    "ruote": {}
}

# ==========================================
# ANALISI RUOTE
# ==========================================

for ruota, lista_estrazioni in estrazioni.items():

    ultima = lista_estrazioni[-1]

    candidati = []

    # ==========================================
    # DISTANZA 9
    # ==========================================

    for n in ultima:

        candidati.append(sorted([n, somma90(n + 9)]))

    # ==========================================
    # DISTANZA 18
    # ==========================================

    for n in ultima:

        candidati.append(sorted([n, somma90(n + 18)]))

    # ==========================================
    # SPECULARI
    # ==========================================

    for n in ultima:

        candidati.append(sorted([n, speculare(n)]))

    # ==========================================
    # SOMME
    # ==========================================

    for i in range(len(ultima)):

        for j in range(i + 1, len(ultima)):

            s = somma90(ultima[i] + ultima[j])

            candidati.append(sorted([ultima[i], s]))

    # ==========================================
    # RIMOZIONE DUPLICATI
    # ==========================================

    unici = []

    visti = set()

    for c in candidati:

        if c[0] == c[1]:
            continue

        key = tuple(c)

        if key not in visti:

            visti.add(key)

            unici.append(c)

    # ==========================================
    # SCORING
    # ==========================================

    migliori = []

    for c in unici:

        a, b = c

        score = 0

        dist = distanza(a, b)

        # DISTANZE FORTI
        if dist == 9:
            score += 50

        if dist == 18:
            score += 45

        if dist == 27:
            score += 35

        # STESSA FIGURA
        if a % 9 == b % 9:
            score += 30

        # NUMERI ALTI
        if a > 45:
            score += 10

        if b > 45:
            score += 10

        # VICINANZA
        if dist <= 10:
            score += 20

        migliori.append({
            "ambo": c,
            "score": score
        })

    # ==========================================
    # ORDINA
    # ==========================================

    migliori.sort(key=lambda x: x["score"], reverse=True)

    migliore = migliori[0]

    risultati["ruote"][ruota] = {
        "estrazione": ultima,
        "ambo": migliore["ambo"],
        "score": migliore["score"]
    }

# ==========================================
# TOP
# ==========================================

top = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)

risultati["top"] = []

for ruota, dati in top[:3]:

    risultati["top"].append({
        "ruota": ruota,
        "ambo": dati["ambo"],
        "score": dati["score"]
    })

# ==========================================
# JOLLY
# ==========================================

risultati["jolly"] = risultati["top"][0]

# ==========================================
# SALVA RISULTATI
# ==========================================

with open("risultati.json", "w") as f:

    json.dump(risultati, f, indent=4)

print("✅ MOTORE CICLICO GENERATO")