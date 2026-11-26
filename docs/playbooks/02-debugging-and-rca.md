---
title: "Playbook 02: Diagnostyka Błędów i Root Cause Analysis (RCA)"
description: "Playbook 02: Diagnostyka Błędów i Root Cause Analysis (RCA)"
---

Procedura lokalizacji i usuwania trudnych błędów oraz anomalii regresyjnych bez zanieczyszczania kontekstu setkami linii logów.

---

## 1. Antywzorzec: "Wklejanie 500 linii stack trace"

Gdy wklejasz do agenta cały zrzut konsoli z 500 liniami stack trace'a:
- Duża część to zwykle wewnętrzne ramki wywołań bibliotek z `node_modules`.
- Agent traci orientację w gąszczu identyfikatorów i zaczyna sugerować losowe zmiany w bibliotekach zewnętrznych.

### Wzorzec: Precyzyjna Ekstrakcja
Wklejaj tylko:
1. Treść błędu (Error message).
2. Pierwsze 3 ramki wywołania z kodu Twojej aplikacji (Twoje pliki i numery linii).
3. Obserwowane zachowanie vs zachowanie oczekiwane.

---

## 2. 4-Krokowy Algorytm Debugowania

### Krok 1: Hipoteza i Lokalizacja
Agent formułuje 2-3 prawdopodobne przyczyny i wskazuje konkretny plik źródłowy na podstawie ramki błędu.

### Krok 2: Odczyt Zakresowy
Zamiast czytać cały 800-liniowy plik, agent czyta wyłącznie funkcję wywołującą:
```text
read_file(path="src/services/payment.ts", start_line=120, end_line=160)
```

### Krok 3: Napisanie Testu Reprodukującego (Failing Test)
Zanim jakakolwiek linijka kodu źródłowego zostanie zmieniona:
- Tworzony jest minimalistyczny test jednostkowy, który odtwarza błąd i w tym momencie **nie przechodzi (czerwony)**.
- Dzięki temu mamy powtarzalny dowód błędu i sposób sprawdzenia poprawki. Sam czerwony test nie dowodzi jeszcze, że znamy przyczynę.

### Krok 4: Atomowa Poprawka i Walidacja (Green Test)
- Edycja właściwej linijki kodu.
- Uruchomienie testu reprodukującego — test **przechodzi (zielony)**.
- Sprawdzenie, czy nie powstały regresje w sąsiadujących testach modułu.
