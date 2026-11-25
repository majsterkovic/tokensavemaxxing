# Środowiska Wykonawcze i Harnessy (Cursor, Claude Code, AGY, Windsurf, Aider)

Szczegółowy przegląd najpopularniejszych harnessów programistycznych pod kątem zarządzania kontekstem, zachowania pamięci podręcznej i podatności na błędy optymalizacji.

---

## 1. Cursor (IDE)

### Profil i Architektura
- **Typ**: Fork VS Code z głęboką integracją modeli frontier (Claude 3.7 Sonnet, GPT-4o, Gemini 2.0 Pro).
- **Format reguł**: `.cursor/rules/*.mdc` (zawiera frontmatter YAML: `description`, `globs`, `alwaysApply`).
- **Mechanizm indeksowania**: Wektorowy indeks codebase + ripgrep grep/glob + symbol provider.

### Dobre praktyki w Cursorze:
1. **Unikaj starego `.cursorrules`**: W trybie Agent plik `.cursorrules` w roocie jest po cichu ignorowany. Używaj wyłącznie `.cursor/rules/*.mdc`.
2. **Używaj `globs` zamiast `alwaysApply: true`**: Trzymaj w `alwaysApply: true` tylko `00-repo.mdc` (~15 linii) oraz `10-efficiency.mdc` (~10 linii). Reszta reguł (np. React, TypeScript, SQL, testy) powinna posiadać maskę `globs: ["**/*.tsx"]`.
3. **Pomiary przez Context Usage Breakdown**: Narzędzie wprowadzone w Cursorze 3.3+ pozwala zobaczyć dokładny rozkład tokenów: ile zabierają reguły, ile pliki, a ile schematy MCP.

### Znane pułapki:
- **Błąd multi-root (155477)**: Otwarcie kilku repozytoriów w jednym workspace powoduje wyciek reguł `alwaysApply: true` ze wszystkich projektów do każdej sesji.
- **Błąd zagnieżdżonych `AGENTS.md` (3.6 - 3.10)**: Automatyczne wciąganie plików `AGENTS.md` ze wszystkich podfolderów jako Always-Applied.
- **Bug ignorowania w non-git root**: Gdy folder nadrzędny nie ma `.git`, wyszukiwanie glob potrafi zignorować `.gitignore` i indeksować gigabajty `node_modules`.

---

## 2. Claude Code (Terminal CLI)

### Profil i Architektura
- **Typ**: Oficjalne narzędzie CLI od Anthropic, działające bezpośrednio w terminalu systemowym.
- **Format reguł**: `CLAUDE.md` w roocie repozytorium (oraz zagnieżdżone `CLAUDE.md` w podfolderach).
- **Zarządzanie agentami**: Wbudowana obsługa subagentów badawczych z własnym oknem kontekstowym.

### Dobre praktyki w Claude Code:
1. **Kompaktowy `CLAUDE.md`**: Claude Code ostrzega przed zbyt dużym plikiem (`40k CLAUDE.md warning`). Plik nie powinien przekraczać 100-150 linii zwięzłych poleceń kompilacji, testów i standardów formatowania.
2. **Agresywne użycie subagentów**: Zlecanie zadań przeszukiwania kodu subagentom read-only zmniejsza rozmiar historii czatu z tysięcy tokenów do zwięzłego podsumowania.
3. **Plik `.claudeignore`**: Warto zdefiniować wykluczenia dla snapshotów i danych testowych.

---

## 3. Google Antigravity (AGY CLI / Swarm)

### Profil i Architektura
- **Typ**: Zaawansowany harness agentowy obsługujący pojedyncze agenty, wyspecjalizowane subagenty oraz dynamiczne skrypty workflow (`run_workflow` w Pythonie) i roje (`swarm`).
- **Zarządzanie regułami**: Skills wbudowane oraz specyficzne dla projektu, pliki kontekstowe i instrukcje systemowe.
- **Narzędzia**: Bogaty zestaw wbudowanych narzędzi (bash, edycja wieloplikowa, subagenty z arbitrażem modeli: Flash vs Pro).

### Dobre praktyki w Antigravity:
1. **Arbitraż modeli (Flash vs Pro)**: Delegowanie researchu i skanowania do subagentów na modelu `flash` lub `flash_lite`, a zadań architektonicznych i zmian krytycznych do modelu `pro` / `inherit`.
2. **Dyscyplina wsadowa (Batching)**: Wymóg wykonywania niezależnych operacji `read_file` i `write_file` równolegle w jednej turze, co oszczędza tury i czas round-trip.
3. **Brak pętli odpytywania (No polling)**: Reaktywny system powiadomień oparty na taskach tła i kolejce wiadomości.

---

## 4. Aider & Windsurf

### Aider
- **Mocna strona**: Genialna, deterministyczna mapa repozytorium (`ctags / tree-sitter repo-map`), wstrzykiwana bezpośrednio do promptu przy minimalnym koszcie tokenów (~1024 tokeny).
- **Ograniczenie**: Przeznaczony głównie do pracy pojedynczego dewelopera w terminalu; brak wbudowanej zaawansowanej orkiestracji subagentów.

### Windsurf (Codeium)
- **Mocna strona**: Architektura "Cascade", łącząca głęboką analizę przepływu sterowania w kodzie z możliwością pracy agentowej w panelu bocznym.
- **Format reguł**: Reguły globalne i per-workspace, zbliżone koncepcyjnie do `.cursorrules`.
