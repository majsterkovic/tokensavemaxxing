---
title: "Ekonomia Tokenów, Prompt Cache i Cięcie Narzędzi"
description: "Ekonomia Tokenów, Prompt Cache i Cięcie Narzędzi"
---

Synteza badań i pomiarów telemetrycznych z realnych sesji deweloperskich (w tym Cursor Engineering Blog z września 2026 oraz publikacja Paritok arXiv:2609.22114).

---

## 1. Architektura Kosztu Tokenowego w Nowoczesnych Modelach

Większość programistów intuicyjnie optymalizuje długość odpowiedzi modelu (output tokens). W praktyce agentic coding:
- **Output tokens** stanowią zazwyczaj zaledwie **3% - 8%** łącznego wolumenu tokenów sesji.
- **Input tokens** (ładowany kontekst per turn: historia, pliki, schematy narzędzi) to **92% - 97%** kosztów.
- Każde odczytanie pliku 1000-liniowego przez narzędzie `read_file` jest re-transmitowane w każdej kolejnej turze rozmowy, o ile nie zadziała prompt caching lub kompresja historii.

### Wymiary optymalizacji:

| Mechanizm | Wpływ na tury 1-5 | Wpływ na tury 10+ | Złożoność wdrożenia |
|---|---|---|---|
| **Cięcie definicji narzędzi (MCP)** | **Bardzo wysoki (−46.9%)** | **Bardzo wysoki (−46.9%)** | 1 kliknięcie / config |
| **Wykluczenia indeksu (`.cursorignore`)** | Wysoki (−20% do −30%) | Wysoki | 1 plik |
| **Pasywna mapa repozytorium** | Średni | Bardzo wysoki (mniej `read_file`) | 1 skrypt generujący |
| **Prompt Caching Prefixes** | Bardzo wysoki (oszczędność $/ms) | Bardzo wysoki | Wymaga stabilnego prefiksu |
| **Kompresja kontekstu** | Niski (~2% per turn) | Ekstremalny (zapobiega n² bloat) | Wbudowany w silnik |

---

## 2. Kluczowe Odkrycia z Badań Cursora (Wrzesień 2026)

### A. Filtracja definicji narzędzi (Tool Definition Pruning)
Definicje narzędzi (JSON schema funkcji MCP, opisy argumentów) są dodawane do promptu systemowego w każdej turze.
- **Wynik pomiaru:** Wyłączenie nieużywanych serwerów MCP redukuje narzut o **46.9% łącznych tokenów** w sesjach korzystających z MCP.
- **Rekomendacja:** Zablokuj (zamroź) zestaw narzędzi na czas sesji. Zmiana zestawu narzędzi w locie unieważnia (invalidates) Prompt Cache dostawcy LLM.

### B. Dynamika Prompt Caching
Prompt cache (np. w Anthropic Claude lub Google Gemini) opiera się na dopasowaniu prefiksu tokenów (prefix matching):
- Każda zmiana na początku promptu (np. dynamicznie zmieniający się czas w nagłówku, dynamicznie wstrzykiwane zmienne środowiskowe przed regułami) powoduje **cache miss dla całego kontekstu**.
- **Złota zasada stabilności:**
  `[Niezmienne reguły i narzędzia] -> [Pasywna mapa repo] -> [Historia czatu] -> [Nowe zapytanie]`

### C. Kompresja zawartości i akumulacja kwadratowa
- W długich sesjach akumulacja odczytanych plików rośnie kwadratowo ($O(N^2)$ w odniesieniu do całkowitego wolumenu wysłanych tokenów w całej sesji).
- Kompresja odczytanych wcześniej plików na poziomie silnika przynosi około **2% redukcji prefiksu per turn**, ale już około **6. tury przewyższa zysk z filtracji narzędzi**.

### D. Format numeracji linii
- Modele LLM mają wbudowaną słabość w precyzyjnym liczeniu linii kodu przy edycjach blokowych.
- Eksperymenty Cursora wykazały, że formatowanie z numeracją co 10. linię lub precyzyjny blok kontekstowy redukuje tokeny odczytu o **1.6%**, całkowicie eliminując błędy lokalizacji edycji (offset drift).

---

## 3. Matryca Działań Natychmiastowych

1. **Odinstaluj/wyłącz serwery MCP**, z których nie korzystasz w danym repozytorium (np. zostaw `filesystem`, wyłącz `playwright`, `database-explorer`, `slack`, jeśli piszesz tylko komponenty Reacta).
2. **Nigdy nie pozwalaj agentowi na czytanie lockfile'ów** (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`) — potrafią mieć po 30 000 linii i natychmiast zepsuć okno kontekstowe.
3. **Wymuszaj zakresowe czytanie plików** (`start_line`, `end_line`) dla plików powyżej 300 linii.
