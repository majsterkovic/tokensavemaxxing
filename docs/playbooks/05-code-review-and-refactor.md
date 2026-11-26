---
title: "Playbook 05: Bezpieczny Refaktoring i Zautomatyzowany Code Review"
description: "Playbook 05: Bezpieczny Refaktoring i Zautomatyzowany Code Review"
---

Procedura przeprowadzania dużych zmian strukturalnych kodu oraz audytu pull requestów przy pomocy niezależnego subagenta recenzenta.

---

## 1. Pułapka Samooceny Agenta (Self-Review Bias)

Model, który właśnie napisał 150 linii kodu, może przeoczać własne błędy, gdy zapytasz go w tym samym czacie: *"Czy widzisz tu jakieś błędy?"*.
Prawdopodobna przyczyna: wcześniejsze tokeny w historii kierują ocenę ku własnym założeniom.

### Rozwiązanie: Niezależny Subagent Reviewer
Recenzja kodu musi odbywać się:
- Albo w **świeżej, czystej sesji czatu**.
- Albo przez **niezależnego subagenta**, który otrzymuje jedynie `git diff` i reguły architektoniczne projektu.

---

## 2. Procedura Refaktoringu Krok po Kroku

### Krok 1: Weryfikacja Siatki Bezpieczeństwa (Test Coverage)
Przed dotknięciem kodu upewnij się, że istniejące testy przechodzą:
```bash
pnpm test
```
Jeśli testów brakuje — pierwszym krokiem jest napisanie testów charakteryzacyjnych (characterization tests), które utrwalają bieżące zachowanie systemu.

### Krok 2: Wyznaczenie Granic Refaktoringu (Refactoring Boundary)
Wyraźnie poinstruuj agenta:
> *"Zmieniamy wyłącznie strukturę wewnętrzną modułu X. Publiczne sygnatury metod, nazwy parametrów i zachowanie w przypadkach brzegowych muszą pozostać w 100% niezmienione. Żadnych zmian wykraczających poza wyznaczony moduł."*

### Krok 3: Inspekcja Ddiffa przez Subagenta Reviewera
Przekaż wygenerowany diff (`git diff HEAD~1`) do subagenta z promptem:
```text
ROLA: Surowy Senior Code Reviewer.
ZADANIE: Przejrzyj poniższy diff pod kątem:
1. Potencjalnych wycieków pamięci lub nieobsłużonych odrzuceń Promise.
2. Złamania reguł typowania (czy nie pojawiło się `any`).
3. Zgodności z konwencją architektoniczną projektu.
WYMÓG: Podaj tylko krytyczne uwagi w punktach z numerami linii. Jeśli diff jest poprawny — odpowiedz krótkim "LGTM".
```
