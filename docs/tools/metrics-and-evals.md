---
title: "Metryki, Pomiary Kontekstu i Ewaluacje (Evals)"
description: "Metryki, Pomiary Kontekstu i Ewaluacje (Evals)"
---


# Metryki, Pomiary Kontekstu i Ewaluacje (Evals)

Przewodnik po pomiarach telemetrycznych efektywności agentów, kalkulacji kosztów i zapobieganiu domysłom przy optymalizacji środowiska programistycznego.

---

## 1. Zasada Zero: "Bez Pomiaru Budujesz na Domysłach"

Optymalizacja bez danych telemetrycznych prowadzi do błędnych decyzji (np. wycinania pożytecznych reguł architektonicznych, podczas gdy prawdziwym winowajcą był nieskonfigurowany serwer MCP albo niechcący odczytywany lockfile o wadze 500 KB).

### Jak zmierzyć stan bazowy:
1. **Cursor 3.3+ -> Context Usage Breakdown**:
   Otwórz sesję, w której agent realnie pracował przez kilkanaście tur (nie świeży czat).
   Sprawdź podział procentowy i tokenowy:
   - `Rules`: stały narzut reguł `.cursor/rules/*.mdc`.
   - `Skills / Prompts`: instrukcje dynamiczne.
   - `MCP Servers`: definicje narzędzi.
   - `Files Read`: dynamicznie odczytana treść plików projektu.

### Tabela Diagnostyczna Objawów:

| Objaw w Breakdown | Wniosek diagnostyczny | Wdrażana interwencja |
|---|---|---|
| **Rules zjadają >2000 tokenów** | Za dużo `alwaysApply: true` lub zbyt długie opisy | Przejście na maski `globs`, kompresja do zwięzłych zakazów |
| **MCP zjadają >30% okna** | Za dużo aktywnych serwerów z dziesiątkami funkcji | Wyłączenie nieużywanych serwerów z workspace |
| **Pliki stanowią 90%+ kosztów** | Agent skanuje repozytorium na oślep, brak mapy | Wdrożenie `REPO-MAP.md` + dyscyplina `10-efficiency.mdc` |
| **Skills mają 0 wywołań** | Model nie wie, kiedy użyć skilla (problem decyzyjny) | Zastąpienie skilla pasywnym fragmentem w `AGENTS.md` |

---

## 2. Główne Wskaźniki Efektywności (KPIs)

1. **Liczba plików odczytanych na zadanie (Files Read per Task)**:
   - Zdrowy wynik: **1 - 4 pliki** dla standardowego zadania / bugfixa.
   - Stan patologiczny: **> 15 plików** (świadczy o braku mapy repozytorium i błądzeniu po kodzie).
2. **Koszt tokenowy tury startowej (Turn 0 Token Baseline)**:
   - Zdrowy wynik: **< 3 000 tokenów** (reguły + mapa repozytorium + podstawowe narzędzia).
   - Stan patologiczny: **> 12 000 tokenów** (przeładowany kontekst przed napisaniem pierwszego słowa).
3. **Wskaźnik sukcesu za pierwszym razem (First-Pass Accuracy)**:
   - Odsetek zadań rozwiązanych bez konieczności interwencji programisty i poprawek w kolejnych turach.
   - Wdrożenie `.cursorignore` + pinning symboli podnosi ten wskaźnik z ~50% do **95%**.

---

## 3. Zautomatyzowany Audyt Lokalny: `scripts/audit-context.sh`

W katalogu `scripts/` znajduje się skrypt powłoki, który:
- Zlicza liczbę tokenów we wszystkich plikach reguł `.cursor/rules/`.
- Sprawdza obecność plików `.cursorignore` oraz `.ignore`.
- Ostrzega, jeśli całkowity rozmiar reguł ładowanych na stałe przekracza bezpieczny próg 2 000 tokenów.
