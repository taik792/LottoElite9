import json
from collections import Counter

# =========================
# CONFIG
# =========================

TOP_MINIMO = 8
JOLLY_MINIMO = 11
FORTE_MINIMO = 13

NUMERI_DA_USARE = 12

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    dati = json.load(f)

top = []
jolly = []
ambo_forte = []

# =========================
# ANALISI RUOTE
# =========================

for ruota, estrazioni in dati.items():

    # prende le ultime 12 estrazioni
    ultime = estrazioni[-NUMERI_DA_USARE:]

    frequenze = Counter()

    # conta tutti i numeri
    for estrazione in ultime:
        for numero in estrazione:
            frequenze[numero] += 1

    # prende i 2 numeri più frequenti
    migliori = frequenze.most_common(2)

    if len(migliori) < 2:
        continue

    n1 = migliori[0][0]
    n2 = migliori[1][0]

    score = migliori[0][1] + migliori[1][1]

    ultima_estrazione = estrazioni[-1]

    dato = {
        "ruota": ruota,
        "ambo": [n1, n2],
        "score": score,
        "estrazione": ultima_estrazione
    }

    # =========================
    # TOP
    # =========================

    if score >= TOP_MINIMO:
        top.append(dato)

    # =========================
    # JOLLY
    # =========================

    if score >= JOLLY_MINIMO:
        jolly.append(dato)

    # =========================
    # AMBO FORTE
    # =========================

    if score >= FORTE_MINIMO:
        ambo_forte.append(dato)

# =========================
# ORDINA
# =========================

top = sorted(top, key=lambda x: x["score"], reverse=True)
jolly = sorted(jolly, key=lambda x: x["score"], reverse=True)
ambo_forte = sorted(ambo_forte, key=lambda x: x["score"], reverse=True)

# =========================
# SALVA
# =========================

risultati = {
    "top": top,
    "jolly": jolly,
    "ambo_forte": ambo_forte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=4, ensure_ascii=False)

print("risultati.json generato correttamente")