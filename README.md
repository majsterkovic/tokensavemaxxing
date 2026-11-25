# ⚡ tokensavemaxxing — The Agentic Coding & Context Engineering Vault

> *"Maksymalna efektywność kodu agentowego przy minimalnym zużyciu tokenów i zerowym szumie kontekstowym."*

Kompletna baza wiedzy, zbiór artykułów naukowych i branżowych, katalog narzędzi, receptury operacyjne (playbooks), szablony konfiguracji oraz skrypty do optymalizacji pracy z agentami AI (Cursor, Claude Code, Antigravity CLI, Windsurf, Aider).

Repozytorium powstało, aby zebrać w jednym miejscu rozproszone techniki inżynierii kontekstu, empiryczne badania (Vercel, Cursor, HumanLayer) oraz gotowe mechanizmy obniżające koszty sesji o **50–70%** przy jednoczesnym **wzroście trafności generowanego kodu z 50% do 95%+**.

---

## 🧭 Mapa Repozytorium

```
tokensavemaxxing/
├── docs/
│   ├── articles/               # Kluczowe publikacje, analizy, benchmarki i streszczenia wiedzy (13 artykułów)
│   │   ├── README.md           # Indeks artykułów i mapa cytowań
│   │   ├── context-and-token-economics.md        # Prompt cache, tool pruning, koszty odczytu (Cursor, Paritok)
│   │   ├── passive-vs-active-context.md          # Benchmark Vercel: AGENTS.md (100%) vs skills (53%)
│   │   ├── instruction-following-decay.md        # Badanie HumanLayer: limit 2000 tokenów i równomierna degradacja
│   │   ├── monorepo-context-strategies.md        # Izolacja kontekstu w architekturach wielorepozytoriowych
│   │   ├── subagents-and-fanout.md               # Wzorce orkiestracji subagentów (read-only scout)
│   │   ├── spotify-shunt-and-portal.md           # Spotify: 90% cięcia tokenów, shunt i AiKA
│   │   ├── inkling-2-mini-architecture.md        # Architektura Looped MoE Inkling 2 Mini
│   │   ├── token-finops-and-benchmarks.md        # Synteza FinOps i niezależnych benchmarków (RTK, ChatDev, LOOP)
│   │   ├── code-navigation-benchmarks.md         # Grep vs AST vs LSP vs Code Graph (arXiv:2608.13568v1)
│   │   ├── agent-skills-ecosystem-2026.md        # Ekosystem Agent Skills, standard SKILL.md i Superpowers
│   │   ├── dynamic-context-pruning-paper-2305-15805.md # Dynamic Context Pruning (ETH Zürich / NeurIPS)
│   │   ├── redis-context-pruning-guide.md        # Redis: Context Rot i Semantic Caching
│   │   └── dycp-dialogue-pruning-2601-07994.md   # DYCP: Dialog Pruning z algorytmem Kadane'a (arXiv:2601.07994)
│   ├── tools/                  # Przewodnik po ekosystemie narzędzi i integracji
│   │   ├── README.md           # Macierz doboru narzędzi i porównanie środowisk
│   │   ├── my-toolset-inventory.md # Personalny inwentarz deweloperski (T3 Code, Herdr, OpenCode, WSL, Local)
│   │   ├── harnesses-and-ides.md # Cursor, Claude Code, Antigravity, Windsurf, Aider
│   │   ├── context-and-mapping.md# AST, tree-sitter, gen-repo-map, Repomix, files-to-prompt
│   │   ├── mcp-servers.md      # Zarządzanie serwerami MCP i redukcja narzutu narzędzi (−46.9%)
│   │   ├── metrics-and-evals.md# Metryki, Context Usage Breakdown, szacowanie ROI
│   │   └── notes/              # Szczegółowe notatki per-narzędzie (13 opracowań)
│   ├── playbooks/              # Gotowe receptury workflow krok-po-kroku
│   │   ├── README.md           # Katalog procedur operacyjnych
│   │   ├── 01-feature-development.md     # Implementacja funkcjonalności w pętli spec -> plan -> exec
│   │   ├── 02-debugging-and-rca.md       # Diagnostyka i root cause analysis bez wypalania tokenów
│   │   ├── 03-token-savemaxxing.md       # Główna metodologia optymalizacji (3 repo, pomiary, pułapki)
│   │   ├── 04-multi-repo-coordination.md # Praca z wieloma repo jednocześnie bez wycieku reguł
│   │   └── 05-code-review-and-refactor.md# Zautomatyzowany audyt kodu i bezpieczny refaktoring
│   └── architecture/           # Wzorce architektoniczne promptów i kontekstu
│       ├── README.md           # Indeks wzorców architektonicznych
│       ├── context-hierarchy.md# 4-warstwowy model kontekstu (System -> Map -> Globs -> On-Demand)
│       ├── subagent-patterns.md# Modele Explorer-Worker, Reviewer, Scatter-Gather
│       └── rule-hygiene.md     # Zasady pisania reguł: reaktywność, budżet <2000 tok
├── templates/                  # Gotowe szablony do skopiowania do projektów
│   ├── .cursor/rules/          # Szablony reguł: 00-repo, 10-efficiency, ts-conventions
│   ├── .cursorignore.template  # Sprawdzony produkcyjny wzorzec wykluczeń
│   ├── .ignore.template        # Zabezpieczenie ripgrep / agent glob
│   ├── AGENTS.md.template      # Skondensowany kontrakt i mapa symboli (8KB)
│   └── prompts/                # Szablony promptów dla zadań, subagentów i review
└── scripts/                    # Skrypty wspomagające bez użycia tokenów LLM
    ├── gen-repo-map.py         # Deterministyczny generator mapy symboli i eksportów przez AST
    └── audit-context.sh        # Skrypt audytujący rozmiar reguł i ignorowane pliki
```

---

## ⚡ 5 Filarów Tokensavemaxxing

| Filar | Działanie | Rezultat |
|---|---|---|
| **1. Warstwa Zerowa (`.cursorignore`)** | Wycięcie generowanego kodu, map źródeł, lockfile'ów, assetów | Indeksowanie 12 min → 4 min; koszt sesji −20% |
| **2. Pasywna Mapa Symboli (`REPO-MAP.md`)** | Deterministyczny graf eksportów i importów przez AST (~2k tok) | Zastępuje setki `read_file`, pass rate skacze do 100% |
| **3. Czystka MCP (Tool Pruning)** | Wyłączenie nieużywanych serwerów protokołu MCP z workspace | Natychmiastowe obcięcie stałego narzutu tury o do **46.9%** |
| **4. Dyscyplina Reguł (`<2000 tok`)** | Przejście z `alwaysApply: true` na reguły z maskami `globs` | Zapobieganie równomiernej degradacji uwagi modelu |
| **5. Subagenty Badawcze (Scouts)** | Tani model (Flash/Haiku) z zakazem cytowania kodu (tylko wniosek + linie) | Redukcja zanieczyszczenia sesji głównej z 6k do <450 tok |

---

## 🔗 Przewodnik Nawigacyjny po Sekcjach

- **[Baza Wiedzy i Artykuły](docs/articles/README.md)** — 13 kompleksowych analiz: ekonomia tokenów, HumanLayer, Vercel, Spotify shunt, Looped MoE Inkling 2 Mini, nawigacja AST/LSP, FinOps, Dynamic Context Pruning i KadaneDial.
- **[Kompendium Narzędzi](docs/tools/README.md)** — macierz doboru środowisk (Cursor, Claude Code, Antigravity, OpenCode), [personalny inwentarz narzędzi](docs/tools/my-toolset-inventory.md) oraz dedykowane notatki techniczne w `docs/tools/notes/`.
- **[Receptury Operacyjne (Playbooks)](docs/playbooks/README.md)** — standardowe procedury krok-po-kroku: [01 Feature Development](docs/playbooks/01-feature-development.md), [02 Debugging & RCA](docs/playbooks/02-debugging-and-rca.md), [03 Token Savemaxxing](docs/playbooks/03-token-savemaxxing.md), [04 Multi-Repo](docs/playbooks/04-multi-repo-coordination.md), [05 Code Review](docs/playbooks/05-code-review-and-refactor.md).
- **[Wzorce Architektoniczne](docs/architecture/README.md)** — [hierarchia kontekstu](docs/architecture/context-hierarchy.md), [higiena reguł](docs/architecture/rule-hygiene.md) i [wzorce subagentów](docs/architecture/subagent-patterns.md).
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
