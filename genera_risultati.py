import json
from collections import Counter
from itertools import combinations

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

# =========================
# FUNZIONI
# =========================

def distanza(a, b):
    d = abs(a - b)
    return min(d, 90 - d)

def vertibile(n):
    if n < 10:
        return n * 10
    return int(str(n)[::-1])

def figura(n):
    return ((n - 1) % 9) + 1

def decina(n):
    return n // 10

# =========================
# ANALISI CICLICA EVOLUTA
# =========================

risultati_ruote = []

for ruota, lista_estrazioni in estrazioni.items():

    if len(lista_estrazioni) < 6:
        continue

    ultime3 = lista_estrazioni[-3:]
    ultima = lista_estrazioni[-1]

    numeri_recenti = []
    for estr in ultime3:
        numeri_recenti.extend(estr)

    candidati = []

    # genera tutti gli ambi
    for a, b in combinations(set(numeri_recenti), 2):

        score = 0

        # =====================
        # DISTANZA CICLICA
        # =====================

        dist = distanza(a, b)

        if dist in [9, 18, 27, 36, 45]:
            score += 3

        # =====================
        # FIGURA UGUALE
        # =====================

        if figura(a) == figura(b):
            score += 2

        # =====================
        # STESSA DECINA
        # =====================

        if decina(a) == decina(b):
            score += 1

        # =====================
        # VERTIBILI
        # =====================

        if vertibile(a) == b or vertibile(b) == a:
            score += 3

        # =====================
        # SOMMA CICLICA
        # =====================

        somma = a + b

        if somma in [90, 45, 54, 72]:
            score += 2

        # =====================
        # RIPETIZIONE NELLE 3 ESTRAZIONI
        # =====================

        freq = numeri_recenti.count(a) + numeri_recenti.count(b)

        if freq >= 3:
            score += 2

        # =====================
        # PRESENZA ULTIMA ESTRAZIONE
        # =====================

        presenti_ultima = 0

        if a in ultima:
            presenti_ultima += 1

        if b in ultima:
            presenti_ultima += 1

        if presenti_ultima == 2:
            score += 3
        elif presenti_ultima == 1:
            score += 1

        # =====================
        # FILTRO FINALE
        # =====================

        if score >= 6:
            candidati.append({
                "ambo": sorted([a, b]),
                "score": score
            })

    # ordina per score
    candidati = sorted(
        candidati,
        key=lambda x: x["score"],
        reverse=True
    )

    # evita duplicati
    visti = set()
    finali = []

    for c in candidati:

        key = tuple(c["ambo"])

        if key not in visti:
            visti.add(key)

            finali.append({
                "ruota": ruota,
                "ambo": c["ambo"],
                "score": c["score"],
                "estrazione": ultima
            })

        if len(finali) >= 1:
            break

    risultati_ruote.extend(finali)

# =========================
# ORDINA TOP
# =========================

risultati_ruote = sorted(
    risultati_ruote,
    key=lambda x: x["score"],
    reverse=True
)

top = risultati_ruote[:3]

# =========================
# JOLLY
# =========================

jolly = top[0] if top else {}

# =========================
# SALVA JSON
# =========================

risultati = {
    "top": top,
    "jolly": jolly,
    "ruote": risultati_ruote
}

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)

print("✅ Nuovo Motore Ciclico Evoluto generato!")