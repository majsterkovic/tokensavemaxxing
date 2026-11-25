---
title: "Playbook 03: tokensavemaxxing — Kompleksowa Metodologia Redukcji Zużycia Tokenów"
description: "Dokument bazowy oparty na sprawdzonym projekcie wdrożeniowym optymalizacji 3 powiązanych repozytoriów (`app` / `web` / `e2e`)."
---

> Dokument bazowy oparty na sprawdzonym projekcie wdrożeniowym optymalizacji 3 powiązanych repozytoriów (`app` / `web` / `e2e`).
> Cel: Redukcja kosztów per task o 50–70%, skrócenie indeksowania o 65% i podniesienie precyzji odpowiedzi za pierwszym razem do ~95%.

---

## 0. Zrób to PRZED Budowaniem Czegokolwiek (Zasada Pomiaru)

Bez pomiaru budujesz na domysłach. Jeden pomiar trwa 10 minut, oszczędza dzień pracy.

**Cursor 3.3+ → Context Usage Breakdown:**
Otwórz sesję, w której agent realnie pracował (nie świeżą, po kilkunastu tool-callach — chcesz zobaczyć stan, w którym sesja zebrała bagaż kontekstowy). Rozkład pokaże osobno:
- `rules`
- `skills`
- `MCP`
- `subagents` / `files read`

### Tabela Decyzyjna:
| Objaw w pomiarze | Wniosek diagnostyczny | Co wdrożyć |
|---|---|---|
| **Rules zjadają dużo (>2k tok)** | Za dużo `alwaysApply: true` lub zbyt długie reguły | Sekcja 4 |
| **Skills zjadają, a nie pomagają** | Warstwa „agent sam sięgnie" nie działa (56% pominięć) | Sekcja 3 & 5 |
| **MCP zjadają znaczną część okna** | Nieużywane serwery w workspace generują niepotrzebny szum | Sekcja 8 |
| **Wszystko mało, a koszt i tak wysoki** | Problem nie w konfiguracji, tylko w niekontrolowanych readach plików | Sekcja 1 & 2 |

**Zanotuj:** ile plików agent odczytał w jednej sesji. To jest Twój prawdziwy licznik. Reguły zmniejszą stały narzut; pliki to 90% zmiennych kosztów sesji.

---

## 1. Warstwa 0 — `.cursorignore` (Wdrażaj Pierwszą)

Zmierzone na repozytorium ~1M linii kodu, to samo zadanie testowe:

| Konfiguracja | Koszt tokenowy | Czas do znalezienia błędu | Poprawność za 1. razem |
|---|---|---|---|
| Domyślnie (brak ignore) | 120 000 tok | 90 s | ~50% |
| `.cursorignore` | 95 000 tok | 60 s | ~70% |
| `.cursorignore` + symbol pinning | **70 000 tok** | **natychmiast** | **~95%** |

### Podwójny efekt:
- **Indeksowanie:** 12 min → 4 min.
- **RAM:** 5.5 GB → 2.8 GB.
- **Efekt jakościowy:** Agent przestaje traktować kod generowany jako wzorzec dla kodu pisanego ręcznie! Model wcześniej uczył się z `*.generated.ts` i stosował niechciane wzorce w świeżym kodzie.

### `.cursorignore` vs `.cursorindexingignore`:
| Plik | Zachowanie AI | Zastosowanie |
|---|---|---|
| `.cursorignore` | AI nie ma dostępu wcale: nie indeksuje, nie czyta, nie cytuje | `.env`, sekrety, `node_modules/`, `dist/`, `build/`, `.next/`, lockfile'y |
| `.cursorindexingignore` | Nie pojawia się w wynikach wyszukiwania, ale AI może odczytać, gdy wskażesz ścieżkę | Fixture'y testowe, kod legacy, duże snapshoty |

W ~90% przypadków wystarcza sam `.cursorignore`.

### Sprawdzony szablon produkcyjny:
```
# Zależności
node_modules/
vendor/
.pnp/

# Artefakty buildu
**/dist/
**/build/
**/.next/
**/out/
**/.turbo/
**/coverage/

# Kod generowany — najgorszy winowajca jakości wyników
**/*.generated.ts
**/*.generated.js
**/__generated__/
**/prisma/generated/
**/graphql/generated/

# Lockfile'y (ogromne, rzadko przydatne agentowi)
package-lock.json
pnpm-lock.yaml
yarn.lock

# Binaria i mapy źródeł
**/*.map
**/*.min.js
**/*.min.css
**/*.bundle.js
**/*.wasm

# Dane testowe
**/__snapshots__/
**/fixtures/large/
**/cypress/videos/
**/cypress/screenshots/
```

**Czego NIE wykluczać:** `src/`, `lib/`, `app/`, plików testowych jednostkowych, konfiguracji projektu. Agent potrzebuje ich, aby zrozumieć system. Zbyt agresywne wykluczenia to częsty błąd.

---

## 2. Warstwa 1 — Indeks Strukturalny (`.cursor/REPO-MAP.md`)

To jest rdzeń optymalizacji potwierdzony empirycznie.
Format: indeks z symbolami, bez treści plików. Sortowany od najczęściej referencjonowanych:

```text
src/api/auth/session.ts
  exports: createSession, SessionUser, SessionConfig
  imported-by: src/api/middleware.ts, src/api/routes/login.ts
  kind: route-handler

src/lib/billing/invoice.ts
  exports: calculateInvoice, InvoiceLine
  imported-by: src/api/routes/invoice.ts, src/jobs/nightly-recalc.ts
  kind: domain
```

Skrypt `gen-repo-map.py` chodzi po repozytorium, wyciąga symbole przez AST, buduje graf importów i wypisuje mapę.
- **Deterministyczny, bez AI, bez sieci.**
- **Koszt:** ~1–3k tokenów w kontekście zamiast setek tysięcy przy chaotycznym skanowaniu.
- **Regeneracja:** Husky + lint-staged na staged plikach. Plik w gicie — diff w PR pokazuje zmianę publicznego API.

---

## 3. Dlaczego Indeks Musi Być Pasywny (Nie „Na Żądanie")

Benchmark Vercel na Next.js 16 API (trzy podejścia, te same dokumenty):

| Podejście | Pass rate | vs baseline |
|---|---|---|
| Baseline (bez dokumentacji) | 53% | — |
| Skill (agent autonomicznie decyduje) | 53% | +0 pp |
| Skill + twardy nakaz w prompcie | 79% | +26 pp |
| **Skompresowany indeks 8KB w AGENTS.md** | **100%** | **+47 pp** |

**W 56% przypadków skill nigdy nie został użyty**, mimo że agent miał do niego dostęp.
Trzy powody wyższości pasywnego kontekstu:
1. **Brak punktu decyzji:** Model nie musi oceniać, czy czegoś nie wie.
2. **Stała dostępność:** Brak opóźnień asynchronicznych.
3. **Brak problemów z sekwencyjnością operacji.**

---

## 4. Warstwa 2 — Reguły `.cursor/rules/*.mdc`

**Nigdy nie używaj przestarzałego `.cursorrules`** — w trybie Agent plik jest po cichu ignorowany!

### Budowa zestawu reguł:
| Plik | Frontmatter | Kiedy się ładuje | Szacunkowy koszt |
|---|---|---|---|
| `00-repo.mdc` | `alwaysApply: true` | Każda sesja | ~250 tok |
| `10-efficiency.mdc` | `alwaysApply: true` | Każda sesja | ~150 tok |
| `ts-conventions.mdc` | `globs: ["**/*.ts"]` | Gdy plik .ts w kontekście | 0 na starcie |
| `e2e-conventions.mdc` | `globs: ["e2e/**", "**/*.spec.ts"]` | Gdy e2e w kontekście | 0 na starcie |

### Żelazny budżet:
**Łącznie < 2 000 tokenów dla wszystkich plików z `alwaysApply: true`**.
Powyżej 2000–3000 tokenów jakość podążania za regułami degraduje **równomiernie w całym pliku** (badanie HumanLayer).

### Wskazówki zamiast wklejania kodu:
Zamiast wklejać 80-liniowy przykład:
> *"Wzoruj się na obsłudze błędów w `src/api/auth/route.ts`"*.
Wklejone przykłady deaktualizują się przy pierwszym refaktorze i uczą model nieistniejących struktur.

---

## 5. Warstwa 3 — Reguła Efektywności (`10-efficiency.mdc`)

Działa na **input**, nie na output. To źródło połowy oszczędności — pojedynczy 1000-liniowy `read_file` potrafi kosztować więcej niż cała odpowiedź modelu.

```markdown
---
description: Dyscyplina efektywności tokenowej w tym repozytorium
alwaysApply: true
---

- Przed wykonaniem `read` sprawdź `.cursor/REPO-MAP.md` i użyj `grep` dla konkretnego symbolu.
- Nie czytaj tego samego pliku dwukrotnie w ramach jednej sesji roboczej.
- Pliki powyżej 300 linii czytaj wyłącznie zakresem (start_line, end_line).
- Nie uruchamiaj `build` / `test` / `lint` po każdej drobnej edycji — tylko gdy zmiana jest ryzykowna lub użytkownik o to poprosi.
- Zakończ działanie natychmiast po wykonaniu zadania — bez zbędnych rund „dla upewnienia się".
- Całkowity zakaz odczytywania: `dist/`, `build/`, `node_modules/`, lockfile'ów, `*.generated.*`.
```

---

## 6. Warstwa 4 — Otwieranie Podfolderu Zamiast Roota

Najtańsza optymalizacja, wymagająca 0 linii kodu:
- Jeśli masz 3 repozytoria (`app`, `web`, `e2e`), otwórz konkretny podfolder (np. `app/`) jako dedykowany workspace.
- Reguły z maskami `globs` z innych repozytoriów nigdy się nie załadują.
- Zabezpiecza przed wyciekiem `alwaysApply: true` z sąsiednich projektów.

---

## 7. Subagenty Badawcze do Eksploracji

Subagent posiada własne, niezależne okno kontekstu. Po zakończeniu zwraca tylko zwięzły wniosek do głównego wątku.
- Wynik w praktyce: **6 100 tokenów czytania plików zamienia się w 420 tokenów syntetycznej konkluzji**.
- **Warunek:** Zawsze żądaj **wniosku + dokładnych ścieżek i linii**. Kategorycznie zabroń subagentowi wklejania bloków kodu.
- **Arbitraż kosztowy:** Używaj tańszego modelu (np. Gemini Flash / Claude Haiku) dla fazy eksploracji read-only (oszczędność ~15–25×).

---

## 8. Prompt Cache i Kolejność Tokenów

Wnioski z analizy telemetrycznej Cursora (wrzesień 2026):
1. **Filtracja definicji narzędzi (Tool Pruning):** Wyłączenie nieużywanych serwerów MCP redukuje łącznie **46.9% tokenów** w sesjach z MCP. Zestaw narzędzi powinien być zamrożony na czas całej sesji dla stabilności pamięci podręcznej.
2. **Kompresja kontekstu:** Zmniejsza prefiks o ~2% per turn, ale akumuluje się kwadratowo i staje się kluczowa powyżej 6. tury.
3. **Numeracja linii:** Zastąpienie pełnego kodu numeracją co 10. linię lub precyzyjnym zakresem obniża narzut odczytu o 1.6% i zapobiega błędom przesunięcia edycji.

---

## 9. Harmonogram Wdrożenia Krok po Kroku

| Krok | Działanie | Czas | Oczekiwany efekt |
|---|---|---|---|
| **1** | Pomiar bazowy — Context Usage Breakdown | 10 min | Punkt odniesienia (baseline) |
| **2** | Wdrożenie `.cursorignore` w repozytoriach | 20 min | ~20% oszczędności + koniec uczenia się na generowanym kodzie |
| **3** | Wyłączenie nieużywanych serwerów MCP | 5 min | Do −46.9% tokenów na start |
| **4** | Wdrożenie `10-efficiency.mdc` | 10 min | Najwyższy natychmiastowy ROI |
| **5** | Utworzenie `00-repo.mdc` + reguły per-glob | 45 min | Jakość i precyzja architektury |
| **6** | Generowanie `REPO-MAP.md` przez `gen-repo-map.py` | 15 min | Największa redukcja operacji `read_file` |
| **7** | Delegowanie poszukiwań do subagentów | Na bieżąco | Czysta historia w zadaniach złożonych |

---

## 10. Katalog Znanych Pułapek i Rozwiązań

- **Błąd: `.cursorrules` jest ignorowany** w trybie Agent -> Migruj natychmiast do `.cursor/rules/*.mdc`.
- **Błąd: Wciąganie zagnieżdżonych `AGENTS.md` (Cursor 3.6–3.10)** -> Nie twórz zagnieżdżonych plików `AGENTS.md`. Używaj reguł `.mdc` z polem `globs`.
- **Błąd: Multi-root wyciek reguł root-level** -> Otwieraj repozytoria w osobnych oknach lub używaj masek `globs` w regułach.
- **Błąd: Wyszukiwanie w workspace bez gita** -> Dodaj plik `.ignore` w składni ripgrep do roota folderu nadrzędnego.
- **Błąd: Używanie `@`-importów w promptach systemowych** -> Pliki importowane przez `@` rozwijają się w całości od tury 0. Zastąp je wskaźnikiem tekstowym: *"Przed edycją endpointu zobacz wzorzec w `docs/api.md`"*.
- **Błąd: Wykluczanie testów jednostkowych z indeksu** -> Agent traci wiedzę, jak poprawnie wywoływać testowane funkcje. Nigdy nie wykluczaj `*.test.*` bez krytycznej potrzeby.
- **Błąd: Sesje-tasiemce (>30 tur)** -> Historia rośnie i jest przesyłana w każdym zapytaniu. Jedno zadanie = jedna sesja. Po rozwiązaniu problemu zamknij czat i otwórz nowy.
