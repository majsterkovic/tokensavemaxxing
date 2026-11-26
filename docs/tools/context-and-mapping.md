---
title: "Narzędzia Mapowania Bazy Kodu i Inżynierii Kontekstu"
description: "Narzędzia Mapowania Bazy Kodu i Inżynierii Kontekstu"
---

Zestawienie deterministycznych narzędzi do ekstrakcji wiedzy o architekturze, grafach zależności i symbolach bez marnowania tokenów modeli LLM.

---

## 1. Dlaczego Determinizm Wygrywa z "Agent Scanning"?

Typowy proces agenta bez mapy repozytorium:
1. Agent wykonuje `list_dir` lub `glob` (znajduje 200 plików).
2. Agent zgaduje, które pliki mogą być istotne.
3. Wykonuje (przykład ilustracyjny) 15 wywołań `read_file` po 500 linii każde = **7 500 linii kodu w kontekście**.
4. Szukana funkcja może być dopiero w kolejnym pliku.

Proces z mapą repozytorium (`REPO-MAP.md`):
1. Agent czyta skondensowany indeks wygenerowany deterministycznie:
   ```text
   src/auth/session.ts
     exports: createSession, verifySession
   ```
2. Agent wie, w którym pliku szukać; linię znajduje przez `grep`.
3. Wykonuje **jedno** precyzyjne czytanie zakresowe: `read_file(path="src/auth/session.ts", start=20, end=45)`.
4. W tym hipotetycznym przykładzie: **25 linii zamiast 7 500**. To ilustracja, nie pomiar.

---

## 2. Przegląd Narzędzi Mapujących

### A. Własny generator mapy: `gen-repo-map.py` (w katalogu `scripts/`)
- **Działanie**: Publiczne funkcje i klasy Pythona (`ast`) oraz nazwy eksportów TS/JS (wyrażenia regularne, heurystyka). Nie obsługuje Go, nie używa tree-sitter i nie buduje grafu importów.
- **Zaleta**: Bez zewnętrznych zależności, działa offline, można go wywołać z hooka pre-commit.
- **Koszt**: **0 tokenów LLM**.

### B. Repomix (dawniej Claude-Pack / Repo-Pack)
- **Repo**: `https://github.com/yamadashy/repomix`
- **Działanie**: Pakuje całe repozytorium do jednego, bezpiecznego dla LLM pliku Markdown lub XML z usuniętymi zbędnymi plikami, komentarzami i znormalizowanymi ścieżkami.
- **Kiedy stosować**: Przy tworzeniu snapshotu bazy wiedzy lub przygotowywaniu zewnętrznego kontekstu dla modelu o ogromnym oknie (np. Gemini 1.5/2.0 Pro 2M context window).

### C. Tree-Sitter & ast-grep
- **ast-grep**: `https://ast-grep.github.io/`
- **Działanie**: Wyszukiwanie wzorców w kodzie oparte na składniowym drzewie rozbioru (AST), a nie na czystym tekście.
- **Zastosowanie w promptach**: Pozwala agentowi formułować precyzyjne kwerendy AST, np. znajdź wszystkie wywołania `executeRawSql` zamiast grepować po stringach.

### D. ctags / Universal Ctags
- Używany przez Aidera.
- Generuje plik tagów z definicjami klas, funkcji, zmiennych i interfejsów.
- Bardzo szybki, wspiera ponad 40 języków programowania.

---

## 3. Automatyzacja w Pipeline CI/Git

Aby mapa repozytorium nie uległa dezaktualizacji (drift):
1. **Hook pre-commit (Husky)** — plik `.husky/pre-commit` w projekcie, do którego skopiowano skrypt:
   ```sh
   python3 scripts/gen-repo-map.py . > .cursor/REPO-MAP.md && git add .cursor/REPO-MAP.md
   ```
   Przekierowanie `>` wymaga powłoki, dlatego nie wpisuj tej komendy wprost w listę `lint-staged`. Skrypt czyta drzewo robocze, więc uwzględni też zmiany niedodane do indeksu. Nagłówek mapy zawiera nazwę katalogu, która może się różnić między klonami.
2. **Korzyść w Code Review**:
   Gdy programista dodaje lub modyfikuje publiczne API modułu, zmiana w `.cursor/REPO-MAP.md` pojawia się w diffie PR-a. Recenzent widzi dodane, usunięte i przemianowane symbole. Zmian samych sygnatur mapa nie pokazuje.
