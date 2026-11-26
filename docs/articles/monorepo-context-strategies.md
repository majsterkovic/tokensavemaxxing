---
title: "Strategie Kontekstu w Monorepo i Multi-Repo"
description: "Jak ograniczać stale ładowany kontekst w monorepo: podfoldery, reguły scope'owane i ładowanie na żądanie."
---

Synteza trzech poradników: [Ivan Magda](https://ivanmagda.dev/posts/fixing-40k-claude-md-warning-monorepo), [Matthews Wong](https://www.matthewswong.com/en/blog/context-engineering-monorepo-ai-agents) i [Start Debugging](https://startdebugging.net/2026/05/how-to-structure-a-monorepo-so-claude-codes-context-stays-small). Dotyczą głównie **Claude Code**. Zachowania innych narzędzi sprawdź w ich dokumentacji.

---

## 1. Co się ładuje i kiedy (Claude Code)

- `CLAUDE.md` z katalogu startowego i katalogów nadrzędnych ładują się w całości na starcie sesji.
- `CLAUDE.md` z podkatalogów ładują się **dopiero wtedy, gdy Claude czyta tam plik**.
- Importy `@plik` porządkują treść, ale nie zmniejszają stałego kontekstu.
- Odczyty wykonane przez subagenta nie trafiają do głównego okna.
- [Dokumentacja Claude Code](https://code.claude.com/docs/en/memory) zaleca **mniej niż 200 linii na plik `CLAUDE.md`**.

### Przykład z praktyki
Magda zmniejszył stale ładowaną treść `CLAUDE.md` w monorepo z około **92 tys. do 25 tys. znaków (−73%)**, przenosząc szczegóły do dokumentów czytanych na żądanie. To przypadek jednego projektu. Autor ocenia, że przestrzeganie instrukcji się poprawiło, ale nie podaje pomiaru.

---

## 2. Wzorce

### Wzorzec A: start w podfolderze
Uruchamiaj agenta w podfolderze, który edytujesz (`apps/web/`), i trzymaj mały plik instrukcji w roocie. Pamiętaj, że instrukcje z katalogów nadrzędnych nadal się ładują. W Claude Code można je pominąć ustawieniem `claudeMdExcludes`.

### Wzorzec B: reguły scope'owane przez `globs` (Cursor)

```markdown
---
description: Reguły dla modułu rozliczeniowego i backendu
globs: ["services/billing/**", "packages/db/**"]
---
```
Treść takiej reguły dołącza się przy pracy z pasującymi plikami, więc zwykle nie obciąża innych sesji. Sprawdź w swojej wersji Cursora, kiedy faktycznie się ładuje ([dokumentacja reguł](https://cursor.com/docs/rules)). W Claude Code podobną rolę pełnią reguły ze ścieżkami w `.claude/rules/`.

### Wzorzec C: plik `.ignore` w roocie
```
node_modules/
.venv/
dist/
build/
.next/
*.generated.*
```
`ripgrep` respektuje `.ignore`. Czy wyszukiwarka danego harnessa używa `ripgrep` z tym ustawieniem, trzeba sprawdzić.

---

## 3. Zgłoszenia o Cursorze — ⚠️ niezweryfikowane

Wcześniejsza wersja przedstawiała poniższe punkty jako fakty. **Sprawdzone źródła ich nie potwierdzają**, więc traktuj je jako hipotezy do odtworzenia:

- ładowanie reguł `alwaysApply: true` i `AGENTS.md` ze wszystkich repozytoriów w multi-root workspace,
- ładowanie wielu zagnieżdżonych `AGENTS.md` w wersjach 3.6+,
- pomijanie `.gitignore` podrzędnych repozytoriów, gdy root workspace nie jest repozytorium git.

Usunięto też liczby bez znalezionego źródła (rozmiar załadowanych reguł, czas indeksowania i zużycie RAM, numer błędu na forum).

## Źródła

- [Ivan Magda: Fixing the 40k CLAUDE.md warning in a monorepo](https://ivanmagda.dev/posts/fixing-40k-claude-md-warning-monorepo)
- [Matthews Wong: Context engineering for AI coding agents in a monorepo](https://www.matthewswong.com/en/blog/context-engineering-monorepo-ai-agents)
- [Start Debugging: How to structure a monorepo](https://startdebugging.net/2026/05/how-to-structure-a-monorepo-so-claude-codes-context-stays-small)
- [Cursor Docs: Rules](https://cursor.com/docs/rules)
- [Claude Code Docs: Memory](https://code.claude.com/docs/en/memory)
