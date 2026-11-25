# Playbook 04: Koordynacja Pracy w Multi-Repo (`app` / `web` / `e2e`)

Zasady i wzorce organizacji pracy z agentami AI w projektach podzielonych na kilka powiązanych repozytoriów gitowych.

---

## 1. Topologia Trzech Repozytoriów

Typowy podział architektoniczny:
- **`app/`**: Serwer backendowy, baza danych, logika biznesowa (Node / Go / Python).
- **`web/`**: Aplikacja frontendowa (Next.js / React / Vite).
- **`e2e/`**: Integracyjne testy end-to-end (Playwright / Cypress).

---

## 2. Trzy Strategie Organizacji Środowiska

### Strategia 1: Osobne Okna IDE (Rekomendowana)
- Otwórz 3 niezależne okna edytora: jedno na `app/`, drugie na `web/`, trzecie na `e2e/`.
- **Zalety:**
  - 100% czystości kontekstowej.
  - Reguły backendowe nigdy nie zanieczyszczają sesji frontendowej.
  - Pomiary Context Usage Breakdown są precyzyjnie przypisane do danego projektu.

### Strategia 2: Multi-Root Workspace z Maskami `globs`
Jeśli musisz widzieć wszystkie 3 drzewa w jednym panelu bocznym edytora:
- W każdym repozytorium **kategorycznie zrezygnuj** z umieszczania specyficznych reguł w `alwaysApply: true`.
- Używaj precyzyjnych prefixów w `globs`:
  ```markdown
  ---
  globs: ["app/**"]
  ---
  ```
- **Uwaga:** Pamiętaj o znanym błędzie Cursora 155477 — reguły `alwaysApply: true` z roota któregokolwiek repozytorium wczytają się do wszystkich sesji. Dlatego `alwaysApply: true` ogranicz do absolutnego minimum.

### Strategia 3: Kontrakt API w Pasywnym Pliku
Gdy zmieniasz endpoint w backendzie (`app/`) i musisz dostosować frontend (`web/`):
1. Zakończ pracę w oknie backendu i wygeneruj/zaktualizuj plik kontraktu (np. `openapi.json` lub plik typów TypeScript `types/api.ts`).
2. W oknie frontendu wskaż agentowi plik kontraktu jako jedyne źródło prawdy. Agent nie musi czytać implementacji kontrolera z backendu — wystarczy mu sam schemat typów.
