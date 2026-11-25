---
title: "Playbook 01: Implementacja Nowej Funkcjonalności (Spec-First)"
description: "Playbook 01: Implementacja Nowej Funkcjonalności (Spec-First)"
---


# Playbook 01: Implementacja Nowej Funkcjonalności (Spec-First)

Ustrukturyzowany proces tworzenia nowej funkcjonalności od specyfikacji technicznej do zweryfikowanego kodu z minimalnym zużyciem tokenów.

---

## 1. Filozofia: "Spec-First, Code-Second"

Najczęstszą przyczyną przepalania tokenów jest natychmiastowe proszenie agenta o pisanie kodu:
- Agent zgaduje architekturę, pisze 200 linii, po czym okazuje się, że założył inną strukturę bazy lub format odpowiedzi API.
- Każda kolejna poprawka to kolejna długa runda edycji i rosnący dług kontekstowy.

### Rozwiązanie: 3-Fazowy Cykl
```
[Faza 1: Mini-Spec & Plan] -> [Faza 2: Subagent Scout] -> [Faza 3: Implementacja & Test]
```

---

## 2. Krok po Kroku

### Faza 1: Krótka Specyfikacja (Zlecenie w 1. turze)
Użytkownik wysyła zwięzły brief określający cel, wejście, wyjście i ograniczenia.

**Wzór promptu:**
```text
ZADANIE: Dodanie możliwości pobierania faktury w formacie PDF w module billing.
WEJŚCIE: GET /api/invoices/:id/pdf (autoryzowany nagłówkiem Bearer).
WYJŚCIE: application/pdf strumieniowany z bucketu S3 lub wygenerowany w locie.
OGRANICZENIA:
- Użyj istniejącego serwisu PDF w `src/lib/pdf/generator.ts`.
- Nie dodawaj nowych zależności npm bez uprzedniej zgody.
KROK 1: Przygotuj plan w punktach (max 5 kroków) i wskaż pliki do modyfikacji. NIE pisz jeszcze kodu.
```

### Faza 2: Szybka Eksploracja (Przez Subagenta lub Mapę)
Agent korzysta z `.cursor/REPO-MAP.md`, aby zlokalizować istniejące powiązania (np. middleware autoryzacji, generator PDF). Jeśli potrzebne jest szersze rozeznanie — deleguje to do subagenta badawczego.

### Faza 3: Precyzyjna Implementacja i Test Jednostkowy
Po zaakceptowaniu planu przez użytkownika:
1. Agent tworzy test jednostkowy sprawdzający kontrakt API (TDD).
2. Agent dokonuje edycji kodu w docelowych plikach.
3. Uruchamia wyłącznie ten konkretny test (nie cały pakiet testów):
   ```bash
   pnpm test src/api/invoices/pdf.spec.ts
   ```

---

## 3. Definition of Done (Kiedy Zamknąć Czat)
- [ ] Test jednostkowy dla nowej funkcji przechodzi pomyślnie.
- [ ] Linter i TypeScript compiler nie zgłaszają błędów w zmodyfikowanych plikach.
- [ ] Czat zostaje zarchiwizowany/zamknięty — kolejne zadanie rozpoczyna się w czystym oknie.
