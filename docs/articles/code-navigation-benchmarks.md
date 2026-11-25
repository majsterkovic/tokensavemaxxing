---
title: "Benchmarki Nawigacji po Repozytorium: Grep vs AST vs LSP vs Code Graph"
description: "Benchmarki Nawigacji po Repozytorium: Grep vs AST vs LSP vs Code Graph"
---

Kompleksowa synteza badań empirycznych (m.in. arXiv:2608.13568v1, ast-grep, Repowise, Antão Almada, Reddit r/ClaudeCode) dotyczących optymalizacji przeszukiwania kodu w pętli agenta.

---

## 1. Wielkie Porównanie Metod Nawigacji

Większość agentów domyślnie próbuje czytać pliki od początku do końca (`cat` / `read_file`), co jest główną przyczyną marnotrawstwa tokenów. Wybór odpowiedniej warstwy nawigacji determinuje koszt sesji:

| Metoda | Narzut i Czas Startu | Wpływ na Tokeny | Kiedy Bezwzględnie Wygrywa |
|---|---|---|---|
| **`ripgrep` / `grep`** | Błyskawiczny (<10 ms), 0 konfiguracji | Baza odniesienia (duży szum przy nieunikalnych nazwach) | Proste wyszukiwanie ciągów znaków, logi, unikalne ID |
| **AST / Tree-sitter** (`ast-grep outline`, `repo-map`) | Bardzo szybki (<50 ms), brak demona | **35% – 55% mniej tokenów** (~50% mniejszy kontekst) | **Pierwszy rzut oka na plik**: zarys funkcji, sygnatury, interfejsy zamiast czytania ciała metod |
| **LSP** (`Serena MCP`, `agent-lsp`) | Wolny start serwera, bywa kruchy w procesach CLI | **+6% do +19% drożej** w prostym szukaniu, ale **5× do 1441× taniej** przy rename | Wieloplikowy refaktoring, skoki do definicji (go-to-def), śledzenie typów |
| **Code Graph** (AST + Call Graph przez MCP) | Wymaga wstępnego indeksowania projektu | **Do ~10× mniej tokenów**, 58% mniej wywołań narzędzi | Złożone pytania architektoniczne w wielkich monorepo |
| **Wyszukiwanie Semantyczne** (BM25 + wektory) | Wymaga bazy wektorowej i embeddingów | ~40% mniej tokenów przy nieznanych nazwach | Gdy programista/agent nie zna dokładnej nazwy funkcji |

---

## 2. Co Pokazują Twarde Benchmarki z 2026 Roku?

### A. Paradoks Grep vs LSP (Badanie arXiv:2608.13568v1)
Naukowcy zbadali zachowanie agentów wyposażonych w LSP oraz narzędzia tekstowe:
- **W prostych zadaniach eksploracyjnych** zmuszenie agenta do korzystania z LSP **zwiększyło zużycie tokenów o 6% do 19%** (ze względu na narzut protokołu JSON-RPC i rozbudowane odpowiedzi serwera językowego).
- **Przełom przy refaktoringu**: W zadaniach typu multi-file rename / safe refactor, LSP podbiło wskaźnik sukcesu `pass@1` z **0.67 do 0.83**, redukując liczbę dodatkowych odczytów plików z **15.2 do zaledwie 3.2**.

### B. Bezwzględna Przewaga AST (`ast-grep outline` & Tree-sitter)
W benchmarku `is-grep-enough` przeprowadzonym na 10 potężnych repozytoriach (Redis, Django, Bitcoin, VS Code):
- **Zarys AST (Outline)** wyciąga strukturę modułu (nazwy klas, metod, dekoratory) bez ciał funkcji.
- **Wyniki empiryczne redukcji kosztów w Claude Code**:
  - **VS Code**: spadek kosztów o **35%**
  - **OkHttp**: spadek kosztów o **40%**
  - **Django**: spadek kosztów o **55%**
  Przy zachowaniu **100% poprawności** lokalizacji właściwych fragmentów kodu.

### C. Grafy Wiedzy o Kodzie (Code Graphs — Antão Almada & Repowise)
- Zbudowanie grafu relacji wywołań (`Caller -> Callee`) w serwerze MCP (np. Codebase-Memory / Repowise) zredukowało liczbę wywołań narzędzi o **58%**, skracając czas wykonania zadania o **22%**.
- Agent nie musi czytać 12 plików pośrednich, aby zrozumieć, skąd pochodzi dany parametr — odpytuje graf jednym zapytaniem.

---

## 3. Złoty Standard Przepływu w tokensavemaxxing (Podejście Warstwowe)

```
[Krok 1: Precyzyjny Grep]
Znalezienie pliku po nazwie symbolu przez ripgrep (0.01s, 0 tokenów)
       │
       ▼
[Krok 2: AST Outline zamiast cat/read_file]
ast-grep outline lub REPO-MAP.md — poznanie linii start/end metody (oszczędność 50%)
       │
       ▼
[Krok 3: Precyzyjny Odczyt Zakresowy]
read_file(start=40, end=65) — przeczytanie TYLKO 25 linii implementacji
       │
       ▼
[Krok 4: Weryfikacja Typów i Referencji (LSP)]
Uruchomienie serwera LSP TYLKO wtedy, gdy zmiana dotyka interfejsów w wielu plikach
```
