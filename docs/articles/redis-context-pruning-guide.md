---
title: "Redis: Pruning Kontekstu a 'Context Rot' i Cache Semantyczny"
description: "Redis: Pruning Kontekstu a 'Context Rot' i Cache Semantyczny"
---

Analiza publikacji inżynierskiej Redis (*"Context Pruning: Cut LLM Tokens Without Losing Quality"*, 2026).

---

## 1. Zjawisko "Context Rot" (Dlaczego Duże Okno Nie Rozwiązuje Problemu)

Współczesne modele oferują okna kontekstowe sięgające miliona tokenów (1M+). Wielu programistów zakłada, że skoro model pomieści całe repozytorium, można bezkarnie wstrzykiwać surowe zrzuty danych.

Redis zwraca uwagę na zjawisko **Context Rot (Gnicie Kontekstu)**:
- Wraz ze wzrostem liczby nieistotnych tokenów w oknie, model traci ostrość uwagi (attention dilution).
- Pojawiają się halucynacje, pomijanie instrukcji z promptu systemowego oraz błędne łączenie faktów z odległych tur.
- **Wniosek**: Pruning kontekstu to nie tylko oszczędność pieniędzy (FinOps) — **odpowiednio przycięty kontekst bezpośrednio podnosi jakość i poprawność generowanego kodu**.

---

## 2. Dwie Metodologie Pruningu według Redis

```
┌────────────────────────────────────────────────────────┐
│             Techniki Pruningu Kontekstu                │
├──────────────────────────┬─────────────────────────────┤
│  Token-Level Pruning     │  Chunk-Level / Query-Aware  │
│  (np. LLMLingua-2)       │  (Zalecany dla Kodu i RAG)  │
├──────────────────────────┼─────────────────────────────┤
│ - Mały enkoder ocenia    │ - Analiza całych bloków     │
│   każdy token            │   funkcji / modułów         │
│ - Usuwanie spójników     │ - Zachowuje składnię i AST  │
│   i powtórzeń            │ - Usuwa całe martwe sekcje  │
│ - Ryzykowne w kodzie     │ - Bezpieczne dla TypeScript/│
│   (może wyciąć średnik   │   Python                    │
│   lub nawias)            │                             │
└──────────────────────────┴─────────────────────────────┘
```

Dla programowania agentowego Redis rekomenduje **Chunk-Level & Query-Aware Pruning**:
- W kodzie źródłowym wycięcie pojedynczego tokenu (np. `!`, `?`, `}`) może zmienić semantykę programu.
- Dlatego przycinanie kodu powinno operować na granicach bloków AST (funkcje, klasy, pliki), a nie na losowych pojedynczych tokenach.

---

## 3. Architektura Produkcyjna: Pruning + Semantic Caching (Redis)

Redis proponuje 3-stopniowy pipeline obsługi zapytań:

```
Zapytanie Agenta / Programisty
              │
              ▼
    [1. Semantic Cache (Redis)]
    Porównanie wektora zapytania z bazą wcześniejszych odpowiedzi
              │
      ┌───────┴───────┐
      ▼               ▼
[Cache HIT]     [Cache MISS]
Zwrot gotowej         │
odpowiedzi            ▼
(0 tokenów LLM, [2. Query-Aware Context Pruning]
 5 ms czasu)    Usunięcie nieistotnych chunków i martwych bloków
                      │
                      ▼
                [3. Inferencja LLM]
                Wysyłka oczyszczonego kontekstu do modelu
```

- **Cache Hit**: Identyczne lub bardzo zbliżone zapytanie (np. częste pytania o schemat bazy czy konfigurację środowiska) pobierane jest z cache semantycznego w kilka milisekund, z zerowym kosztem API.
- **Cache Miss**: Zapytanie przechodzi przez filtr pruningu, który wycina szum przed uderzeniem do LLM.
