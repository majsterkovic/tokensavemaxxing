---
title: "Hierarchia Kontekstu (4-Warstwowy Model Pamięci Agenta)"
description: "Hierarchia Kontekstu (4-Warstwowy Model Pamięci Agenta)"
---

Proponowany (autorski) model warstwowego ładowania kontekstu, zapewniający równowagę między dostępnością wiedzy a dyscypliną budżetu tokenowego.

---

## 1. Cztery Warstwy Kontekstu

```
┌─────────────────────────────────────────────────────────────┐
│  Warstwa 0: Pasywne Reguły Bazowe (Always-On: <800 tok)     │
│  - 00-repo.mdc (topologia, stack, zakazy)                   │
│  - 10-efficiency.mdc (dyscyplina narzędzi i readów)         │
├─────────────────────────────────────────────────────────────┤
│  Warstwa 1: Pasywny Indeks Architektury (~1 500 tok)        │
│  - .cursor/REPO-MAP.md (wygenerowany przez gen-repo-map.py) │
│  - Ścieżki i publiczne symbole (bez importów i sygnatur)    │
├─────────────────────────────────────────────────────────────┤
│  Warstwa 2: Warunkowe Reguły Domenowe (Maski globs)         │
│  - ts-conventions.mdc (gdy edytowany .ts)                   │
│  - sql-rules.mdc (gdy edytowany plik migracji)              │
├─────────────────────────────────────────────────────────────┤
│  Warstwa 3: Dynamiczny Odczyt na Żądanie (On-Demand Read)   │
│  - Wskaźniki tekstowe ("Zobacz wzorzec w docs/api.md")      │
│  - Precyzyjne odczyty zakresowe (start_line, end_line)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Charakterystyka Warstw

### Warstwa 0: Pasywne Reguły Bazowe (`alwaysApply: true`)
- **Cel**: Wyznaczenie twardych granic operacyjnych i zakazów.
- **Limit (konwencja repo)**: budżet < 800 tokenów (max 25-30 linii tekstu).
- **Zasada**: Zero wklejonych bloków kodu. Wyłącznie zwięzłe nakazy/zakazy i linki do plików wzorcowych.

### Warstwa 1: Pasywny Indeks Architektury
- **Cel**: Wyeliminowanie operacji błądzenia i skanowania całego repozytorium.
- **Limit**: 1 000 - 3 000 tokenów.
- **Zasada**: Wyłącznie publiczne symbole (Python: moduł `ast`; TS/JS: heurystyka regex). Zero ciał funkcji i implementacji.

### Warstwa 2: Warunkowe Reguły Domenowe (`globs`)
- **Cel**: Wstrzykiwanie specyficznych konwencji tylko wtedy, gdy agent realnie dotyka powiązanych plików.
- **Koszt na starcie sesji**: treść reguły zwykle nie jest ładowana, dopóki nie pasuje plik; sprawdź to w widoku kontekstu swojego narzędzia.
- **Zasada**: Precyzyjne maski ścieżek, unikanie masek zbyt szerokich typu `**/*`.

### Warstwa 3: Dynamiczny Odczyt na Żądanie (Lazy Loading)
- **Cel**: Pobieranie szczegółowej dokumentacji tylko wtedy, gdy warunek logiczny jest spełniony.
- **Zasada**: W regule umieszczasz jedynie trigger:
  > *"Przed utworzeniem nowej tabeli w bazie przeczytaj `docs/database-naming-conventions.md`"*.
  Model sam podejmuje decyzję o odczytaniu pliku w odpowiednim momencie, dzięki czemu w pozostałych zadaniach plik nie zajmuje miejsca w oknie.
