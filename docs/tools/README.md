# Kompendium Narzędzi Programowania Agentowego

Przewodnik po współczesnym stosie technologicznym (tech stack) programisty współpracującego z agentami AI: od harnessów i środowisk IDE, przez narzędzia deterministycznego mapowania repozytorium, po serwery protokołu MCP i systemy ewaluacji.

---

## 🗂️ Struktura Sekcji Narzędzi

| Moduł | Zakres | Główne technologie |
|---|---|---|
| [my-toolset-inventory.md](my-toolset-inventory.md) | **Twój spersonalizowany inwentarz narzędzi** | T3 Code, Herdr, Claude Code, Codex, Antigravity, OpenCode, WSL, Local Models (12 GB) |
| **[notes/](notes/)** | **Dedykowane notatki per-narzędzie** | [claude-code.md](notes/claude-code.md), [codex.md](notes/codex.md), [antigravity-cli.md](notes/antigravity-cli.md), [opencode.md](notes/opencode.md), [herdr.md](notes/herdr.md), [t3-code.md](notes/t3-code.md), [openbot.md](notes/openbot.md), [wsl.md](notes/wsl.md), [local-models-12gb.md](notes/local-models-12gb.md) |
| [harnesses-and-ides.md](harnesses-and-ides.md) | Środowiska wykonawcze agentów, edytory, terminale | Cursor, Claude Code, Antigravity CLI, Windsurf, Aider, OpenCode |
| [context-and-mapping.md](context-and-mapping.md) | Deterministyczne indeksowanie i destylacja kodu | AST, tree-sitter, `gen-repo-map`, Repomix, files-to-prompt |
| [mcp-servers.md](mcp-servers.md) | Model Context Protocol: zarządzanie i optymalizacja | GitHub MCP, Postgres MCP, Playwright, Filesystem, Audyt narzutu |
| [metrics-and-evals.md](metrics-and-evals.md) | Monitorowanie zużycia kontekstu i weryfikacja poprawności | Context Breakdown, Langfuse, Promptfoo, test pass-rate |

---

## 🧭 Macierz Doboru Środowiska Roboczego

| Narzędzie | Najlepsze zastosowanie | Model pracy | Kluczowa zaleta | Na co uważać |
|---|---|---|---|---|
| **T3 Code** | Cockpit GUI dla wielu agentów, praca wieloprojektowa | GUI Control Plane | Inbox-style wątki, BYOK, git worktrees | Telemetria (warto wyłączyć) |
| **Herdr** | Wielozadaniowość terminalowa, sesje długodystansowe | TUI / Desktop Daemon | Agenci działają w tle po zamknięciu okna, statusy OSC 7501 | Narzędzie relatywnie świeże |
| **Claude Code** | Szybkie operacje w terminalu, pipeline'y CLI, git workflows | Terminal CLI | Świetne subagenty badawcze, mały narzut UI, dostęp do powłoki | Brak podglądu diffa w GUI |
| **Antigravity (AGY)** | Złożone przepływy multi-agent, workflow scripts, swarmy | CLI & IDE Extension | Koordynacja subagentów, skrypty w Pythonie, arbitraż Flash/Pro | Wyłączaj zbędne MCP |
| **OpenCode** | Elastyczny TUI agent łączący modele chmurowe i lokalne | Terminal TUI | Tryby `plan`/`build`, integracja z LSP, 75+ modeli | Konfiguracja providerów |
| **Codex** | Złożona logika matematyczna i algorytmiczna | CLI / Web | Modele reasoning (o3-mini, GPT-4o) | Koszt tokenów rozumowania |
| **Cursor** | Kompleksowe tworzenie aplikacji, refaktoringi full-stack | IDE (fork VS Code) | Natywne inline diffs, `.cursor/rules/*.mdc` | Wyciek reguł w multi-root |

---

## 📐 Zasada Doboru Narzędzi: "Determinizm przed LLM"

Złota zasada inżynierii agentowej głosi:
> **Nigdy nie płać tokenami modelu za to, co można obliczyć deterministycznym skryptem w 10 milisekund.**

- Generowanie mapy eksportów -> **AST / tree-sitter (skrypt Python)**, nie prompt do LLM.
- Formatowanie kodu -> **Prettier / Ruff**, nie reguła w pliku `.mdc`.
- Sprawdzanie typów -> **tsc / mypy**, nie model frontier.
- Weryfikacja składni -> **Linter**, nie "sprawdź czy nie ma literówek".
