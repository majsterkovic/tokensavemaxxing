---
title: "Nawigacja po Repozytorium: Grep vs AST vs LSP vs Code Graph"
description: "Co faktycznie zmierzono dla grep, zarysu AST, LSP i grafów kodu w pętli agenta oraz jakie są ograniczenia tych pomiarów."
---

Zestawienie pomiarów dotyczących przeszukiwania kodu przez agenta. Każdy pochodzi z innego eksperymentu, więc procentów **nie można porównywać między wierszami**.

---

## 1. Porównanie metod

| Metoda | Co zmierzono | Źródło i ograniczenia |
|---|---|---|
| **`ripgrep` / `grep`** | Punkt odniesienia. Bez indeksu i serwera; przy popularnych nazwach daje szum | — |
| **Zarys AST** (`ast-grep outline`) | Mediana kosztu Claude Code: VS Code −35%, Django −55%, OkHttp −40% | [Benchmark autorów narzędzia](https://ast-grep.github.io/blog/ast-grep-outline); w mniejszych repozytoriach bywało drożej |
| **LSP** | W badanych zadaniach zwykle drożej niż grep; lepsza precyzja przy szukaniu referencji | [Wstępne badanie, Pengcheng Xu](https://arxiv.org/html/2608.13568v1); małe próby |
| **Code graph** | 58% mniej wywołań narzędzi, 22% szybciej | Deklaracja narzędzia codegraph cytowana u [Antão Almady](https://antaoalmada.dev/posts/Code-Agent-Knowledge-Graphs) (mediana z 4 przebiegów) |

---

## 2. Szczegóły

### A. LSP vs grep ([arXiv:2608.13568v1](https://arxiv.org/html/2608.13568v1))

*Does a Language Server Save Tokens for Coding Agents? A Measurement Methodology and Preliminary Study* (czerwiec 2026). Zadania na pythonowym `requests` i dwóch repozytoriach TypeScript, modele Claude.

- **Lokalizacja po nazwie symbolu** (Opus 4.8): tylko LSP kosztował **+6% tokenów**, a mając wybór, agent z LSP nie korzystał. Dla Sonnet 4.6 narzut wyniósł +118%, a Haiku 4.5 zyskał (−26%).
- **Kompletność referencji** (Opus 4.8): LSP dał pełną precyzję (1,00 vs 0,76), ale kosztował **około 19% więcej**.
- **Rename w wielu plikach:** grep miał `pass@1` 1,00. LSP zwracający same lokalizacje miał 0,67. Dołączenie tekstu linii do wyników podniosło go do **0,83** i zmniejszyło liczbę odczytów plików na epizod z **15,2 do 3,2**. Grep nadal wygrywał, bo rename obejmuje też komentarze i stringi.

Te liczby **nie pokazują**, że LSP jest tańszy od grep przy refaktoringu. Wartości 0,67 → 0,83 porównują dwa warianty LSP.

### B. Zarys AST ([ast-grep outline](https://ast-grep.github.io/blog/ast-grep-outline))

Zarys pokazuje strukturę pliku bez ciał funkcji. W benchmarku na siedmiu repozytoriach autorzy podają spadek mediany kosztu o 35% (VS Code), 55% (Django) i 40% (OkHttp). **Mediana** pokrycia i precyzji względem wyniku referencyjnego została na 100%, ale pojedyncze przebiegi nie zawsze się z nim zgadzały. W małych repozytoriach zarys czasem tylko dokładał pracy.

### C. Grafy kodu

[Almada](https://antaoalmada.dev/posts/Code-Agent-Knowledge-Graphs) opisuje kilka narzędzi i przytacza ich wyniki, w tym akademicką ewaluację (arXiv:2603.27277, 31 repozytoriów): 10× mniej tokenów i 2,1× mniej wywołań niż przy eksploracji plik po pliku, przy 83% jakości odpowiedzi. Przegląd narzędzi daje też [Repowise](https://repowise.dev/blog/comparisons/best-code-graph-mcp-servers), który jest jednocześnie dostawcą jednego z nich.

---

## 3. Przepływ warstwowy (propozycja tego repozytorium)

To **zalecenie autorskie**, niezmierzone jako całość.

```
[Krok 1: Grep]            znajdź plik po nazwie symbolu
       │
       ▼
[Krok 2: Zarys]           ast-grep outline (numery linii) zamiast czytania całego pliku
       │                  REPO-MAP.md pokazuje tylko pliki i eksporty, bez numerów linii
       ▼
[Krok 3: Odczyt zakresu]  np. read_file(start=40, end=65)
       │
       ▼
[Krok 4: LSP]             gdy potrzebne są dokładne referencje typów
```

Przy rename nadal sprawdź grep-em komentarze i stringi.

## Źródła

- [Pengcheng Xu, arXiv:2608.13568v1](https://arxiv.org/html/2608.13568v1)
- [ast-grep: outline](https://ast-grep.github.io/blog/ast-grep-outline)
- [Antão Almada: Code Agent Knowledge Graphs](https://antaoalmada.dev/posts/Code-Agent-Knowledge-Graphs)
- [Repowise: Best code graph MCP servers](https://repowise.dev/blog/comparisons/best-code-graph-mcp-servers) (materiał dostawcy)
- Do dalszej lektury, niewykorzystane jako dowód liczb: [grep vs LSP harness](https://www.agentconnect.md/blog/grep-beat-lsp-harness), [Particula](https://particula.tech/blog/semantic-code-search-vs-grep-coding-agents), [yage.ai](https://yage.ai/share/why-coding-agents-still-use-grep-en-20260327.html), [wątek r/ClaudeCode „Is grep enough?”](https://www.reddit.com/r/ClaudeCode/comments/1ujnpy6/is_grep_enough_code_navigation_for_agents_measured) (⚠️ treści wątku nie udało się pobrać przy weryfikacji)
