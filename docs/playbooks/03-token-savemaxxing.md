---
title: "Playbook 03: tokensavemaxxing — Kompleksowa Metodologia Redukcji Zużycia Tokenów"
description: "Procedura redukcji zużycia tokenów dla układu 3 repozytoriów (app / web / e2e)."
---

> Punkt wyjścia: układ trzech powiązanych repozytoriów (`app` / `web` / `e2e`).
> Cel: mniej zbędnego kontekstu **bez pogorszenia jakości**.
>
> :warning: Wcześniejsza wersja obiecywała konkretne procenty oszczędności, skrócenie indeksowania i wzrost trafności oraz zawierała tabelę pomiarów. **Nie zapisano metodyki** (zadania, próba, wersje, sposób liczenia), więc te liczby usunięto. Dodaj je z powrotem razem z opisem pomiaru, jeśli go masz.

---

## 0. Zrób to PRZED Budowaniem Czegokolwiek (Zasada Pomiaru)

Bez pomiaru budujesz na domysłach. Jeden pomiar trwa 10 minut, oszczędza dzień pracy.

**W Cursorze: rozbicie użycia kontekstu (Context Usage Breakdown; dostępność zależy od wersji):**
Otwórz sesję, w której agent realnie pracował (nie świeżą, po kilkunastu tool-callach — chcesz zobaczyć stan, w którym sesja zebrała bagaż kontekstowy). Rozkład pokaże osobno:
- `rules`
- `skills`
- `MCP`
- `subagents` / `files read`

### Tabela Decyzyjna:
| Objaw w pomiarze | Wniosek diagnostyczny | Co wdrożyć |
|---|---|---|
| **Rules zjadają dużo (>2k tok)** | Za dużo `alwaysApply: true` lub zbyt długie reguły | Sekcja 4 |
| **Skills zjadają, a nie pomagają** | Agent może nie uruchamiać skilla (zob. sekcja 3) | Sekcja 3 & 5 |
| **MCP zjadają znaczną część okna** | Nieużywane serwery w workspace generują niepotrzebny szum | Sekcja 8 |
| **Wszystko mało, a koszt i tak wysoki** | Problem nie w konfiguracji, tylko w niekontrolowanych readach plików | Sekcja 1 & 2 |

**Zanotuj:** ile plików agent odczytał w jednej sesji. To jest Twój prawdziwy licznik. Reguły wpływają na stały narzut; odczyty plików i wyniki narzędzi często dominują w części zmiennej. Sprawdź proporcje u siebie.

---

## 1. Warstwa 0 — `.cursorignore` (Wdrażaj Pierwszą)

Wyklucz to, czego agent nie powinien czytać ani indeksować. Efekt zmierz na własnym repozytorium: to samo zadanie z wykluczeniami i bez, kilka powtórzeń, z zapisem tokenów, czasu i wyniku testów.

Spodziewany efekt jakościowy (hipoteza): mniej sytuacji, w których agent traktuje kod generowany jako wzorzec dla pisanego ręcznie.

### `.cursorignore` vs `.cursorindexingignore`:
| Plik | Zachowanie AI | Zastosowanie |
|---|---|---|
| `.cursorignore` | Blokuje dostęp Agenta, Taba i odwołań `@` do plików. **Terminal i narzędzia MCP używane przez Agenta nadal mogą je odczytać**, a pełna ochrona nie jest gwarantowana ([dokumentacja](https://cursor.com/docs/context/ignore-files)) | `.env`, `node_modules/`, `dist/`, `build/`, `.next/`, lockfile'y |
| `.cursorindexingignore` | Nie pojawia się w wynikach wyszukiwania, ale AI może odczytać, gdy wskażesz ścieżkę (⚠️ niezweryfikowane: sprawdzona strona dokumentacji nie opisuje tego pliku) | Fixture'y testowe, kod legacy, duże snapshoty |

Zwykle wystarcza sam `.cursorignore`.

### Przykładowy szablon:
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

Indeks ścieżek i publicznych symboli, bez treści plików. Rzeczywisty format wyjścia `gen-repo-map.py` (przykład ilustracyjny):

```text
src/api/auth/session.ts
  exports: SessionConfig, SessionUser, createSession

src/lib/billing/invoice.ts
  exports: InvoiceLine, calculateInvoice
```

Co robi skrypt:
- Python: publiczne funkcje i klasy najwyższego poziomu (moduł `ast`),
- TypeScript/JavaScript: nazwy eksportów (wyrażenia regularne, heurystyka),
- działa deterministycznie, bez AI i sieci,
- **nie** buduje grafu importów, nie sortuje po liczbie referencji, nie wypisuje metod ani sygnatur.

Rozmiar zależy od repozytorium; sprawdź go po wygenerowaniu. **Efektu tej mapy na koszt lub trafność nie zmierzono.** Najbliższy publiczny punkt odniesienia to [benchmark `ast-grep outline`](https://ast-grep.github.io/blog/ast-grep-outline), który bada inną technikę (zarys pliku na żądanie).

Regeneracja: ręcznie lub hookiem pre-commit — przykład w [Kontekst i Mapowanie](/tokensavemaxxing/tools/context-and-mapping/). Z mapą w gicie zmiany nazw publicznych symboli widać w diffie PR.

---

## 3. Dlaczego Indeks Powinien Być Pasywny

[Ewaluacja Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) na nowych API Next.js 16:

| Podejście | Pass rate | vs baseline |
|---|---|---|
| Baseline (bez dokumentacji) | 53% | — |
| Skill (agent sam decyduje) | 53% | +0 pp |
| Skill + jawna instrukcja w `AGENTS.md` | 79% | +26 pp |
| **Indeks dokumentacji Next.js (8 KB) w `AGENTS.md`** | **100%** | **+47 pp** |

**W 56% przypadków skill nie został użyty.** Robocze wyjaśnienia autorów: brak punktu decyzyjnego, stała dostępność w każdej turze i brak problemu kolejności.

**Zakres:** to był indeks **dokumentacji**, nie mapa kodu. Wynik nie dowodzi skuteczności `REPO-MAP.md`. Szczegóły i ograniczenia: [Pasywny Kontekst vs Skille](/tokensavemaxxing/articles/passive-vs-active-context/).

---

## 4. Warstwa 2 — Reguły `.cursor/rules/*.mdc`

**Zamiast `.cursorrules` używaj `.cursor/rules/*.mdc`** — sprawdzona [dokumentacja reguł](https://cursor.com/docs/rules) opisuje reguły `.mdc` i `AGENTS.md`, a `.cursorrules` nie wymienia.

### Budowa zestawu reguł:
| Plik | Frontmatter | Kiedy się ładuje | Szacunkowy koszt |
|---|---|---|---|
| `00-repo.mdc` | `alwaysApply: true` | Każda sesja | ~250 tok |
| `10-efficiency.mdc` | `alwaysApply: true` | Każda sesja | ~150 tok |
| `ts-conventions.mdc` | `globs: ["**/*.ts"]` | Gdy plik .ts w kontekście | 0 na starcie |
| `e2e-conventions.mdc` | `globs: ["e2e/**", "**/*.spec.ts"]` | Gdy e2e w kontekście | 0 na starcie |

### Umowny budżet:
**Łącznie < 2 000 tokenów dla wszystkich plików z `alwaysApply: true`**.
To konwencja tego repozytorium, nie próg z badania. Ogólną radę, by plik był krótki, daje [poradnik HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — zob. [analizę](/tokensavemaxxing/articles/instruction-following-decay/).

### Wskazówki zamiast wklejania kodu:
Zamiast wklejać 80-liniowy przykład:
> *"Wzoruj się na obsłudze błędów w `src/api/auth/route.ts`"*.
Wklejone przykłady deaktualizują się przy pierwszym refaktorze i uczą model nieistniejących struktur.

---

## 5. Warstwa 3 — Reguła Efektywności (`10-efficiency.mdc`)

Działa na **input**, nie na output: pojedynczy odczyt 1000-liniowego pliku potrafi kosztować więcej niż odpowiedź modelu, a potem zostaje w historii. Progi poniżej to konwencje.

```markdown
---
description: Dyscyplina efektywności tokenowej w tym repozytorium
alwaysApply: true
---

- Przed wykonaniem `read` sprawdź `.cursor/REPO-MAP.md` i użyj `grep` dla konkretnego symbolu.
- Nie czytaj ponownie pliku, który się nie zmienił i którego treść nadal masz w kontekście.
- Pliki powyżej 300 linii czytaj wyłącznie zakresem (start_line, end_line).
- W trakcie pracy uruchamiaj najwęższy test dla zmienianego kodu zamiast całego pakietu.
- Przed zgłoszeniem zakończenia zawsze uruchom weryfikację zmienionego zakresu (testy, typecheck, lint) i podaj wynik.
- Całkowity zakaz odczytywania: `dist/`, `build/`, `node_modules/`, lockfile'ów, `*.generated.*`.
```

---

## 6. Warstwa 4 — Otwieranie Podfolderu Zamiast Roota

Najtańsza optymalizacja, wymagająca 0 linii kodu:
- Jeśli masz 3 repozytoria (`app`, `web`, `e2e`), otwórz konkretny podfolder (np. `app/`) jako dedykowany workspace.
- Reguły projektowe z sąsiednich repozytoriów zwykle się nie ładują.
- Reguły globalne i pliki z katalogów nadrzędnych (np. `CLAUDE.md` w Claude Code) nadal mogą się ładować — sprawdź w widoku kontekstu.

---

## 7. Subagenty Badawcze do Eksploracji

Subagent posiada własne, niezależne okno kontekstu. Po zakończeniu zwraca tylko zwięzły wniosek do głównego wątku.
- Przykład (**liczby ilustracyjne, bez zapisanej metodyki**): zamiast 6100 tokenów odczytów do **głównego** wątku trafia około 420 tokenów raportu. Subagent sam zużywa tokeny, więc łączne zużycie może być wyższe.
- **Domyślnie żądaj wniosku z dokładnymi ścieżkami i liniami**, bez dużych bloków kodu; krótki cytat dopuszczaj, gdy od treści zależy decyzja.
- **Tańszy model** (klasy Flash / Haiku) może wystarczyć do eksploracji read-only. Różnicę ceny sprawdź w cenniku, a jakość raportu na swoich zadaniach.

---

## 8. Prompt Cache i Kolejność Tokenów

Źródła i zakres liczb: [Ekonomia Tokenów](/tokensavemaxxing/articles/context-and-token-economics/).

1. **Narzędzia na żądanie** ([Cursor](https://cursor.com/blog/improved-token-efficiency)): dynamiczne ładowanie narzędzi MCP dało **−46,9% łącznych tokenów w sesjach, które wywołały narzędzie MCP**. To nie jest pomiar wyłączania serwerów. Dodatkowo (zalecenie autorskie) nie zmieniaj bez potrzeby zestawu narzędzi w trakcie sesji, bo może to unieważnić cache.
2. **Kompresja kontekstu** ([Paritok, arXiv:2609.22114](https://arxiv.org/html/2609.22114) — nie Cursor): ok. 2% prefiksu na turę; suma rośnie w przybliżeniu kwadratowo i w ich pomiarze około 6. tury przewyższała zysk z filtrowania narzędzi.
3. **Numeracja linii** (Cursor): numerowanie co 10. linię zmniejszyło liczbę tokenów odczytywanych z cache o 1,6% bez spadku jakości. To mechanizm harnessu.

---

## 9. Harmonogram Wdrożenia Krok po Kroku

| Krok | Działanie | Co sprawdzić |
|---|---|---|
| **1** | Pomiar bazowy: rozbicie użycia kontekstu | Punkt odniesienia |
| **2** | `.cursorignore` w repozytoriach | Czy potrzebne pliki nadal są dostępne |
| **3** | Wyłączenie zbędnych serwerów MCP | Zmiana stałego narzutu |
| **4** | `10-efficiency.mdc` | Liczba i rozmiar odczytów, wynik testów |
| **5** | `00-repo.mdc` + reguły per-glob | Czy reguły ładują się wtedy, gdy powinny |
| **6** | `REPO-MAP.md` przez `gen-repo-map.py` | Czy spada liczba odczytów |
| **7** | Subagenty do dużej eksploracji | Główny kontekst **i** łączne zużycie |

Kolejność to propozycja autorska. Zmieniaj jedną rzecz naraz i porównuj z baseline.

---

## 10. Katalog Pułapek i Rozwiązań

Punkty o błędach Cursora pochodzą ze zgłoszeń **niezweryfikowanych** w sprawdzonych źródłach. Odtwórz problem, zanim zmienisz konfigurację.

- **Starszy format `.cursorrules`** -> Migruj do `.cursor/rules/*.mdc`.
- ⚠️ **Zgłoszenie: Wciąganie zagnieżdżonych `AGENTS.md` (Cursor 3.6–3.10)** -> Nie twórz zagnieżdżonych plików `AGENTS.md`. Używaj reguł `.mdc` z polem `globs`.
- ⚠️ **Zgłoszenie: Multi-root wyciek reguł root-level** -> Otwieraj repozytoria w osobnych oknach lub używaj masek `globs` w regułach.
- **Błąd: Wyszukiwanie w workspace bez gita** -> Możesz dodać plik `.ignore` (składnia ripgrep) w roocie; sprawdź, czy wyszukiwarka narzędzia go respektuje.
- **Błąd: Używanie `@`-importów w promptach systemowych** -> Pliki importowane przez `@` rozwijają się w całości od tury 0. Zastąp je wskaźnikiem tekstowym: *"Przed edycją endpointu zobacz wzorzec w `docs/api.md`"*.
- **Błąd: Wykluczanie testów jednostkowych z indeksu** -> Agent traci wiedzę, jak poprawnie wywoływać testowane funkcje. Nigdy nie wykluczaj `*.test.*` bez krytycznej potrzeby.
- **Sesje-tasiemce (np. >30 tur, próg umowny)** -> Historia rośnie i jest przesyłana w każdym zapytaniu. Jedno zadanie = jedna sesja. Po rozwiązaniu problemu zamknij czat i otwórz nowy.
