import json
from collections import Counter

# =========================
# CARICA ESTRAZIONI
# =========================

with open("estrazioni.json", "r", encoding="utf-8") as f:
    dati = json.load(f)

# Se il JSON contiene {"estrazioni":[...]}
if isinstance(dati, dict) and "estrazioni" in dati:
    estrazioni = dati["estrazioni"]

# Se il JSON è già una lista
else:
    estrazioni = dati

# Prende ultime 12 estrazioni
ultime = estrazioni[-12:]

# =========================
# FUNZIONI
# =========================

def ciclo_piu9(n):
    return ((n + 8) % 90) + 1

def ciclo_meno9(n):
    return ((n - 10) % 90) + 1

def complementare90(n):
    return 90 - n if n != 90 else 90

def score_numero(n, frequenze):
    score = 0

    # Frequenza recente
    score += frequenze.get(n, 0)

    # Bonus numeri ciclici
    score += frequenze.get(ciclo_piu9(n), 0)
    score += frequenze.get(ciclo_meno9(n), 0)

    # Bonus complementare
    score += frequenze.get(complementare90(n), 0)

    return score

# =========================
# ELABORAZIONE
# =========================

top = []
jolly = []
amboForte = []

for estrazione in ultime:

    ruota = estrazione["ruota"]
    numeri = estrazione["numeri"]

    # Frequenze ultime 12 estrazioni della stessa ruota
    storico = []

    for e in ultime:
        if e["ruota"] == ruota:
            storico.extend(e["numeri"])

    frequenze = Counter(storico)

    candidati = []

    # Genera numeri da cicli
    for n in numeri:

        candidati.append(ciclo_piu9(n))
        candidati.append(ciclo_meno9(n))
        candidati.append(complementare90(n))

    # Rimuove numeri appena usciti
    candidati = [n for n in candidati if n not in numeri]

    # Rimuove duplicati
    candidati = list(set(candidati))

    # Calcolo score
    scored = []

    for n in candidati:
        s = score_numero(n, frequenze)
        scored.append((n, s))

    # Ordina per score
    scored.sort(key=lambda x: x[1], reverse=True)

    # Serve almeno 2 numeri
    if len(scored) < 2:
        continue

    n1 = scored[0][0]
    n2 = scored[1][0]

    score_finale = scored[0][1] + scored[1][1]

    risultato = {
        "ruota": ruota,
        "ambo": [n1, n2],
        "score": score_finale,
        "estrazione": numeri
    }

    top.append(risultato)

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
    "Venezia",
    "Nazionale"
]

top.sort(
    key=lambda x: ordine_ruote.index(x["ruota"])
    if x["ruota"] in ordine_ruote else 999
)

# =========================
# JOLLY
# =========================

jolly = sorted(top, key=lambda x: x["score"], reverse=True)[:3]

# =========================
# AMBO FORTE
# =========================

amboForte = sorted(top, key=lambda x: x["score"], reverse=True)[:5]

# =========================
# SALVA FILE
# =========================

risultati = {
    "top": top,
    "jolly": jolly,
    "amboForte": amboForte
}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2, ensure_ascii=False)

print("risultati.json generato correttamente")