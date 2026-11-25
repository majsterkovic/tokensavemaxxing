# Kompendium Narzędzi Programowania Agentowego

Przewodnik po współczesnym stosie technologicznym (tech stack) programisty współpracującego z agentami AI: od harnessów i środowisk IDE, przez narzędzia deterministycznego mapowania repozytorium, po serwery protokołu MCP i systemy ewaluacji.

---

## 🗂️ Struktura Sekcji Narzędzi

| Moduł | Zakres | Główne technologie |
|---|---|---|
| [harnesses-and-ides.md](harnesses-and-ides.md) | Środowiska wykonawcze agentów, edytory, terminale | Cursor, Claude Code, Antigravity CLI, Windsurf, Aider, OpenCode |
| [context-and-mapping.md](context-and-mapping.md) | Deterministyczne indeksowanie i destylacja kodu | AST, tree-sitter, `gen-repo-map`, Repomix, files-to-prompt |
| [mcp-servers.md](mcp-servers.md) | Model Context Protocol: zarządzanie i optymalizacja | GitHub MCP, Postgres MCP, Playwright, Filesystem, Audyt narzutu |
| [metrics-and-evals.md](metrics-and-evals.md) | Monitorowanie zużycia kontekstu i weryfikacja poprawności | Context Breakdown, Langfuse, Promptfoo, test pass-rate |

---

## 🧭 Macierz Doboru Środowiska Roboczego

| Narzędzie | Najlepsze zastosowanie | Model pracy | Kluczowa zaleta | Na co uważać |
|---|---|---|---|---|
| **Cursor** | Kompleksowe tworzenie aplikacji, refaktoringi full-stack, UI | IDE (fork VS Code) | Natywna integracja z edytorem, `.cursor/rules/*.mdc`, inline diffs | Wyciek reguł w multi-root, bugi ładowania `AGENTS.md` |
| **Claude Code** | Szybkie operacje w terminalu, pipeline'y CLI, git workflows | Terminal CLI | Świetne subagenty badawcze, mały narzut UI, bezpośredni dostęp do powłoki | Brak natywnego podglądu diffa przed zatwierdzeniem w UI |
| **Antigravity (AGY)** | Złożone przepływy multi-agent, workflow scripts, swarmy | CLI & IDE Extension | Koordynacja subagentów (`invoke_subagent`), workflow scripts w Pythonie, MCP | Wymaga dyscypliny w zamykaniu zbędnych narzędzi |
| **Aider** | Czysty terminal, git-native commits, repo-mapping | Terminal CLI | Automatyczne tworzenie precyzyjnych commitów gita, wbudowany ctag-repomap | Mniej elastyczny w obsłudze wieloetapowych zadań subagentowych |
| **Windsurf** | Środowisko z kaskadową pamięcią ("Cascade") | IDE | Śledzenie stanu i kroków procesu w panelu bocznym | Mniejsza społeczność tworząca reguły i szablony niż w Cursorze |

---

## 📐 Zasada Doboru Narzędzi: "Determinizm przed LLM"

Złota zasada inżynierii agentowej głosi:
> **Nigdy nie płać tokenami modelu za to, co można obliczyć deterministycznym skryptem w 10 milisekund.**

- Generowanie mapy eksportów -> **AST / tree-sitter (skrypt Python)**, nie prompt do LLM.
- Formatowanie kodu -> **Prettier / Ruff**, nie reguła w pliku `.mdc`.
- Sprawdzanie typów -> **tsc / mypy**, nie model frontier.
- Weryfikacja składni -> **Linter**, nie "sprawdź czy nie ma literówek".
