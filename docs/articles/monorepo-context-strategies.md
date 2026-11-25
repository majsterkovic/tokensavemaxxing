# Strategie Kontekstu w Monorepo i Multi-Repo

Synteza analiz inżynierskich: Ivan Magda ("Fixing 40k CLAUDE.md warning in monorepo"), Matthew Wong ("Context engineering in monorepo AI agents") oraz wątków forum Cursora dotyczących środowisk multi-root.

---

## 1. Patologie Dużych Środowisk (Monorepo & Multi-Root)

Praca agenta w monorepo lub z kilkoma powiązanymi repozytoriami (np. `app/`, `web/`, `e2e/`) w jednym oknie IDE rodzi specyficzne, kosztowne problemy:

### Problem 1: Globalny wyciek reguł w Multi-Root Workspace (Błąd Cursora 155477)
W Cursorze, gdy otworzysz Multi-Root Workspace zawierający 3 repozytoria, pliki `AGENTS.md` i reguły `alwaysApply: true` z **każdego** repozytorium ładują się globalnie do każdej sesji.
- Rezultat: Sesja dotycząca prostego buga w CSS we frontendzie ładuje reguły bazy danych, workerów backendowych i testów e2e.
- Skutek: Natychmiastowe przekroczenie limitu 3000 tokenów reguł bazowych i degradacja precyzji.

### Problem 2: Zagnieżdżone `AGENTS.md` (Błąd Cursora 3.6 - 3.10)
Wersje Cursora 3.6+ potrafią skanować drzewo w dół i ładować zagnieżdżone `AGENTS.md` ze wszystkich podfolderów (zgłoszony przypadek: 600 000 tokenów samych reguł wciągniętych na starcie sesji).

### Problem 3: Otwarty Workspace Root bez Repo Gita
Jeśli rootem workspace w Cursorze jest nadrzędny folder, który sam nie jest repozytorium gita (np. folder ze skrótami do 3 repozytoriów), Agent Glob `**/*` ignoruje pliki `.gitignore` poszczególnych repozytoriów.
- Skanowanie potrafi zawiesić agenta na 3-5 minut i wczytać 3 000 plików ze skompilowanymi assetami zamiast 80 plików źródłowych.

---

## 2. Sprawdzone Wzorce Rozwiązań

### Wzorzec A: Otwieranie Podfolderu (Folder-Scoped Workspace)
Najprostsza i najbardziej radykalna optymalizacja:
- Zamiast otwierać nadrzędny katalog monorepo (`company-all/`), otwórz konkretny podfolder roboczy (`company-all/apps/web/`).
- **Efekt**: Reguły z innych modułów fizycznie nie istnieją w kontekście. Indeksowanie trwa 4 minuty zamiast 15 minut. Zużycie pamięci RAM spada z 5.5 GB do 2.8 GB.

### Wzorzec B: Reguły Scope'owane przez Frontmatter `globs`
W środowiskach wspierających reguły `.mdc` (Cursor) nigdy nie umieszczaj reguł technologicznych w `alwaysApply: true`. Używaj precyzyjnych masek:

```markdown
---
description: Reguły dla modułu rozliczeniowego i backendu
globs: ["services/billing/**", "packages/db/**"]
---
```
Taka reguła ma **zerowy koszt tokenowy** na początku sesji. Ładuje się do pamięci tylko wtedy, gdy agent otwiera lub modyfikuje plik pasujący do maski `globs`.

### Wzorzec C: Zabezpieczenie `.ignore` w roocie
Jeżeli musisz pracować w jednym oknie na wielu projektach, w roocie nadrzędnym utwórz plik `.ignore` w składni kompatybilnej z ripgrep:
```
node_modules/
.venv/
dist/
build/
.next/
*.generated.*
```
Ripgrep (używany przez agenta pod maską do grep/glob) respektuje plik `.ignore` nawet wtedy, gdy parser gita w IDE ulegnie awarii.
