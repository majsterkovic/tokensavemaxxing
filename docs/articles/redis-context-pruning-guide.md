---
title: "Redis: Pruning Kontekstu i Cache Semantyczny"
description: "Przewodnik Redis o przycinaniu kontekstu, jego ograniczeniach i łączeniu z cache semantycznym."
---

Analiza przewodnika Redis [Context Pruning: Cut LLM Tokens Without Losing Quality](https://redis.io/blog/context-pruning-llm-tokens). To materiał dostawcy, który sprzedaje cache semantyczny.

---

## 1. Dlaczego duże okno nie wystarcza

Przewodnik wskazuje, że dłuższy kontekst może pogarszać wyniki:
- efekt **„lost in the middle”** (informacja ze środka jest gorzej wykorzystywana),
- sama długość wejścia może obniżać jakość,
- źle zarządzany kontekst powoduje zatrucie (utrwalone błędne dane), rozproszenie, pomyłki i sprzeczności.

Pruning **często, ale nie zawsze**, poprawia jakość. Redis opisuje też ryzyka: zbyt mocne cięcie traci informacje i może zwiększać halucynacje, a w krótkich kontekstach jakość zwykle spada wraz z kompresją.

---

## 2. Granulacja pruningu

| Podejście | Uwagi z przewodnika |
|---|---|
| **Na poziomie tokenów** (np. LLMLingua-2) | Nadaje się do ogólnego tekstu; w kodzie może zepsuć składnię |
| **Na poziomie fragmentów** | Dla kodu zalecane są całe jednostki logiczne, np. definicje funkcji i bloki klas |
| **Query-aware** | Zachowuje tokeny istotne dla pytania; wskazane, gdy ważna jest dokładność |

Przykład z przewodnika: na SWE-Bench wyspecjalizowany SWE-Pruner osiągnął 64% sukcesu zadań, a LLMLingua-2 54%. Liczby pochodzą z prac przytoczonych przez Redis, których tu nie weryfikowano.

---

## 3. Pruning z cache semantycznym

```
Zapytanie → cache semantyczny ── trafienie ──→ zapisana odpowiedź (bez inferencji)
                   │
                chybienie
                   ▼
          pobranie kontekstu → pruning → LLM → zapis odpowiedzi w cache
```

Dla usługi Redis LangCache producent podaje do 15× szybsze odpowiedzi przy trafieniach i do 73% niższe koszty **we własnych benchmarkach**.

**Uwaga (autorska):** w programowaniu agentowym odpowiedź zależy od aktualnego stanu repozytorium. Zwrócenie odpowiedzi z cache dla „podobnego” pytania może dać nieaktualny wynik, więc potrzebne są reguły unieważniania.

## Źródła

- [Redis: Context pruning for LLM tokens](https://redis.io/blog/context-pruning-llm-tokens)
