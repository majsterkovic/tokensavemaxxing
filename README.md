# ⚡ tokensavemaxxing — The Agentic Coding & Context Engineering Vault

> *"Maksymalna efektywność kodu agentowego przy minimalnym zużyciu tokenów i zerowym szumie kontekstowym."*

Kompletna baza wiedzy, zbiór artykułów naukowych i branżowych, katalog narzędzi, receptury operacyjne (playbooks), szablony konfiguracji oraz skrypty do optymalizacji pracy z agentami AI (Cursor, Claude Code, Antigravity CLI, Windsurf, Aider).

Repozytorium powstało, aby zebrać w jednym miejscu rozproszone techniki inżynierii kontekstu, opracowania publikacji i wpisów inżynierskich (z linkami do źródeł) oraz mechanizmy ograniczające zbędny kontekst. Efekt zależy od projektu i trzeba go zmierzyć; repozytorium nie gwarantuje konkretnych procentów.

---

## 🧭 Mapa Repozytorium

```
tokensavemaxxing/
├── docs/
│   ├── articles/               # Kluczowe publikacje, analizy, benchmarki i streszczenia wiedzy (13 artykułów)
│   │   ├── index.md            # Indeks artykułów i mapa cytowań
│   │   ├── context-and-token-economics.md        # Prompt cache, tool pruning, koszty odczytu (Cursor, Paritok)
│   │   ├── passive-vs-active-context.md          # Vercel: indeks dokumentacji w AGENTS.md (100%) vs skill bez instrukcji (53%)
│   │   ├── instruction-following-decay.md        # Przeciążenie instrukcjami: jak pisać krótkie reguły
│   │   ├── monorepo-context-strategies.md        # Izolacja kontekstu w architekturach wielorepozytoriowych
│   │   ├── subagents-and-fanout.md               # Wzorce orkiestracji subagentów (read-only scout)
│   │   ├── spotify-shunt-and-portal.md           # Spotify: wtyczka Shunt i Portal
│   │   ├── inkling-2-mini-architecture.md        # Architektura Looped MoE Inkling 2 Mini
│   │   ├── token-finops-and-benchmarks.md        # Synteza FinOps i niezależnych benchmarków (RTK, ChatDev, LOOP)
│   │   ├── code-navigation-benchmarks.md         # Grep vs AST vs LSP vs Code Graph (arXiv:2608.13568v1)
│   │   ├── agent-skills-ecosystem-2026.md        # Ekosystem Agent Skills, standard SKILL.md i Superpowers
│   │   ├── dynamic-context-pruning-paper-2305-15805.md # Dynamic Context Pruning (ETH Zürich / NeurIPS)
│   │   ├── redis-context-pruning-guide.md        # Redis: pruning kontekstu i cache semantyczny
│   │   └── dycp-dialogue-pruning-2601-07994.md   # DYCP: Dialog Pruning z algorytmem Kadane'a (arXiv:2601.07994)
│   ├── tools/                  # Przewodnik po ekosystemie narzędzi i integracji
│   │   ├── index.md            # Macierz doboru narzędzi i porównanie środowisk
│   │   ├── my-toolset-inventory.md # Personalny inwentarz deweloperski (T3 Code, Herdr, OpenCode, WSL, Local)
│   │   ├── harnesses-and-ides.md # Cursor, Claude Code, Antigravity, Windsurf, Aider
│   │   ├── context-and-mapping.md# Indeks symboli, gen-repo-map, Repomix, files-to-prompt
│   │   ├── mcp-servers.md      # Zarządzanie serwerami MCP i narzut definicji narzędzi
│   │   ├── metrics-and-evals.md# Metryki, Context Usage Breakdown, szacowanie ROI
│   │   └── notes/              # Szczegółowe notatki per-narzędzie (13 opracowań)
│   ├── playbooks/              # Gotowe receptury workflow krok-po-kroku
│   │   ├── index.md            # Katalog procedur operacyjnych
│   │   ├── 01-feature-development.md     # Implementacja funkcjonalności w pętli spec -> plan -> exec
│   │   ├── 02-debugging-and-rca.md       # Diagnostyka i root cause analysis bez wypalania tokenów
│   │   ├── 03-token-savemaxxing.md       # Główna metodologia optymalizacji (3 repo, procedura, pułapki)
│   │   ├── 04-multi-repo-coordination.md # Praca z wieloma repo jednocześnie bez wycieku reguł
│   │   └── 05-code-review-and-refactor.md# Zautomatyzowany audyt kodu i bezpieczny refaktoring
│   └── architecture/           # Wzorce architektoniczne promptów i kontekstu
│       ├── index.md            # Indeks wzorców architektonicznych
│       ├── context-hierarchy.md# 4-warstwowy model kontekstu (System -> Map -> Globs -> On-Demand)
│       ├── subagent-patterns.md# Modele Explorer-Worker, Reviewer, Scatter-Gather
│       └── rule-hygiene.md     # Zasady pisania reguł: reaktywność, umowny budżet <2000 tok
├── templates/                  # Gotowe szablony do skopiowania do projektów
│   ├── .cursor/rules/          # Szablony reguł: 00-repo, 10-efficiency, ts-conventions
│   ├── .cursorignore.template  # Przykładowy wzorzec wykluczeń
│   ├── .ignore.template        # Zabezpieczenie ripgrep / agent glob
│   ├── AGENTS.md.template      # Skondensowany kontrakt i mapa symboli
│   └── prompts/                # Szablony promptów dla zadań, subagentów i review
└── scripts/                    # Skrypty wspomagające bez użycia tokenów LLM
    ├── gen-repo-map.py         # Mapa symboli: Python (ast), TS/JS (regex)
    ├── audit-context.sh        # Szacunek stałego narzutu instrukcji i obecność plików ignore
    └── test_scripts.py         # Testy obu skryptów (python3 -m unittest discover -s scripts)
```

---

## ⚡ 5 Filarów Tokensavemaxxing

| Filar | Działanie | Czego się spodziewać |
|---|---|---|
| **1. Warstwa Zerowa (`.cursorignore`)** | Wykluczenie kodu generowanego, map źródeł, lockfile'ów, assetów | Mniej szumu w indeksie; efekt zmierz u siebie |
| **2. Pasywna Mapa Symboli (`REPO-MAP.md`)** | Lista publicznych symboli Pythona (`ast`) i eksportów TS/JS (regex), bez grafu importów | Może ograniczyć liczbę odczytów; efektu tej mapy nie zmierzono |
| **3. Narzędzia MCP na żądanie** | Dynamiczne ładowanie definicji; wyłączanie zbędnych serwerów | [Cursor](https://cursor.com/blog/improved-token-efficiency): −46,9% tokenów w sesjach wywołujących MCP dla ładowania **na żądanie** (nie dla wyłączania serwerów) |
| **4. Dyscyplina Reguł** | Krótkie reguły stałe, reszta przez `globs` | Mniejszy stały narzut; budżet poniżej 2000 tok to konwencja repo |
| **5. Subagenty Badawcze (Scouts)** | Eksploracja w osobnym kontekście, raport ze ścieżkami i liniami | Czystszy główny kontekst; łączne zużycie może wzrosnąć |

---

## 🔗 Przewodnik Nawigacyjny po Sekcjach

- **[Baza Wiedzy i Artykuły](docs/articles/index.md)** — 13 kompleksowych analiz: ekonomia tokenów, przeciążenie instrukcjami, Vercel, Spotify shunt, Looped MoE Inkling 2 Mini, nawigacja AST/LSP, FinOps, Dynamic Context Pruning i KadaneDial.
- **[Kompendium Narzędzi](docs/tools/index.md)** — macierz doboru środowisk (Cursor, Claude Code, Antigravity, OpenCode), [personalny inwentarz narzędzi](docs/tools/my-toolset-inventory.md) oraz dedykowane notatki techniczne w `docs/tools/notes/`.
- **[Receptury Operacyjne (Playbooks)](docs/playbooks/index.md)** — standardowe procedury krok-po-kroku: [01 Feature Development](docs/playbooks/01-feature-development.md), [02 Debugging & RCA](docs/playbooks/02-debugging-and-rca.md), [03 Token Savemaxxing](docs/playbooks/03-token-savemaxxing.md), [04 Multi-Repo](docs/playbooks/04-multi-repo-coordination.md), [05 Code Review](docs/playbooks/05-code-review-and-refactor.md).
- **[Wzorce Architektoniczne](docs/architecture/index.md)** — [hierarchia kontekstu](docs/architecture/context-hierarchy.md), [higiena reguł](docs/architecture/rule-hygiene.md) i [wzorce subagentów](docs/architecture/subagent-patterns.md).
- **[Szablony Promptów i Konfiguracji](templates/AGENTS.md.template)** — wzorzec `AGENTS.md`, szablony reguł w `templates/.cursor/rules/` oraz prompty w `templates/prompts/`.

---

## 🚀 Szybki Start

1. **Wdróż wykluczenia i szablony reguł efektywności w swoim projekcie:**
   ```bash
   cp templates/.cursorignore.template /twoj-projekt/.cursorignore
   cp templates/.ignore.template /twoj-projekt/.ignore
   mkdir -p /twoj-projekt/.cursor/rules
   for f in templates/.cursor/rules/*.template; do
     cp "$f" "/twoj-projekt/.cursor/rules/$(basename "$f" .template)"
   done
   ```

2. **Wygeneruj mapę symboli bez używania tokenów AI:**
   ```bash
   python3 scripts/gen-repo-map.py /twoj-projekt > /twoj-projekt/.cursor/REPO-MAP.md
   ```

3. **Przetestuj higienę kontekstu i budżet reguł:**
   ```bash
   bash scripts/audit-context.sh /twoj-projekt
   ```

4. **Przejdź do głównego playbooka:**
   Czytaj [docs/playbooks/03-token-savemaxxing.md](docs/playbooks/03-token-savemaxxing.md).
