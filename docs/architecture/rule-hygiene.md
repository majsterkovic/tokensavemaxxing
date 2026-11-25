---
title: "Higiena i Dyscyplina Reguł (Rule Hygiene)"
description: "Higiena i Dyscyplina Reguł (Rule Hygiene)"
---


# Higiena i Dyscyplina Reguł (Rule Hygiene)

Zasady tworzenia, utrzymania i czyszczenia reguł dla modeli językowych, aby uniknąć degradacji uwagi i efektu "Rule Bloat".

---

## 1. Trzy Prawa Higieny Reguł

### Prawo 1: Reaktywność Zamiast Przewidywania
Nigdy nie pisz reguły "na zapas" na wypadek błędu, którego model jeszcze nigdy w tym projekcie nie popełnił.
Regułę dodajesz **wyłącznie wtedy, gdy model realnie popełnił ten sam błąd w co najmniej dwóch różnych sesjach**.

### Prawo 2: Determinizm Przed Promptem
Jeśli regułę można wymusić deterministycznym narzędziem w pipeline:
- Linter (ESLint, Biome, Ruff)
- Formatowanie (Prettier, Black)
- Kompilator typów (TypeScript, mypy)
- Pre-commit hook
-> **Wymuś to narzędziem, a nie regułą w promptach LLM.** Szkoda budżetu uwagi modelu na pilnowanie średników czy sortowania importów.

### Prawo 3: Zasada Ścisłego Budżetu (Strict Token Budget)
Całkowity rozmiar wszystkich reguł ładowanych na stałe w każdej sesji (`alwaysApply: true`) **nie może przekraczać 2 000 tokenów** (optymalnie < 800 tokenów).

---

## 2. Antywzorce w Pisaniu Reguł

| Antywzorzec | Dlaczego szkodzi | Prawidłowa alternatywa |
|---|---|---|
| **Wklejanie bloków kodu (80 linii)** | Zjada setki tokenów, deaktualizuje się przy zmianie bibliotek | Wskaźnik tekstowy: *"Wzoruj się na `src/api/auth.ts`"* |
| **Pozytywne frazesy** (*"Pisz czysty kod, bądź pomocny"*) | Zero wartości decyzyjnej, rozcieńcza uwagę | Konkretne zakazy negatywne: *"Nigdy nie używaj `any`"* |
| **Zagnieżdżone `AGENTS.md`** | W Cursorze 3.6-3.10 potrafią wciągnąć 600k tokenów | Pojedynczy plik `.mdc` z polem `globs` |
| **Używanie przestarzałego `.cursorrules`** | Po cichu ignorowany w trybie Agent | Migracja do `.cursor/rules/*.mdc` |
| **Ignorowanie maski `globs`** | Wszystkie reguły ładują się zawsze, zjadając kontekst | Przypisywanie reguł do rozszerzeń: `globs: ["**/*.tsx"]` |
