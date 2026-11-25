---
title: "Kompendium Narzędzi Programowania Agentowego"
description: "Przewodnik po stosie technologicznym: harnessy AI, notatki per-narzędzie, mapowanie AST, serwery MCP i metryki."
---

Przewodnik po stosie technologicznym programisty pracującego z agentami AI — od harnessów i multiplekserów sesji, przez deterministyczne mapowanie kodu, po narzędzia redukcji tokenów.

## 🗂️ Moduły Sekcji Narzędzi

| Moduł | Zakres |
|---|---|
| [Spersonalizowany Inwentarz Stosu](/tokensavemaxxing/tools/my-toolset-inventory/) | Architektura 4-warstwowa i tabela routingu zadań między narzędziami |
| [Notatki Per-Narzędzie (13 narzędzi)](/tokensavemaxxing/tools/notes/) | Dedykowane karty: Claude Code, Codex, Antigravity, OpenCode, Herdr, T3 Code, RTK, WSL, Local 12 GB |
| [Harnessy i IDE](/tokensavemaxxing/tools/harnesses-and-ides/) | Porównanie środowisk wykonawczych: Cursor, Claude Code, Antigravity, OpenCode |
| [Kontekst i Mapowanie AST](/tokensavemaxxing/tools/context-and-mapping/) | Deterministyczne indeksowanie: `tree-sitter`, `gen-repo-map`, Repomix |
| [Serwery MCP — Audyt i Pruning](/tokensavemaxxing/tools/mcp-servers/) | Zarządzanie narzutem definicji narzędzi i wycinanie zbędnych serwerów |
| [Metryki i Ewaluacje](/tokensavemaxxing/tools/metrics-and-evals/) | Context Breakdown, śledzenie kosztów sesji i weryfikacja jakości |

## 🧭 Szybki Wybór Środowiska

| Narzędzie | Najlepsze zastosowanie | Kluczowa zaleta |
|---|---|---|
| **T3 Code** | Cockpit GUI dla wielu agentów | Inbox-style wątki, BYOK, git worktrees |
| **Herdr** | Sesje w tle ("tmux dla agentów") | Persistence i statusy OSC 7501 |
| **Claude Code** | Szybkie operacje CLI i git workflows | Subagenty badawcze, niski narzut UI |
| **Antigravity (AGY)** | Złożone swarmy i Python workflows | Koordynacja subagentów, arbitraż Flash/Pro |
| **OpenCode** | Praca TUI z modelami cloud + local | Tryby `plan`/`build`, integracja z LSP |
| **Codex** | Trudna logika algorytmiczna i RCA | Modele reasoning (`o3-mini`, GPT-4o) |
| **Cursor** | Edycja full-stack w IDE | Inline diffs, reguły `.cursor/rules/*.mdc` |

:::tip[Złota zasada: Determinizm przed LLM]
**Nigdy nie płać tokenami modelu za to, co można policzyć skryptem w 10 ms.** Mapę eksportów generuj przez AST (`gen-repo-map.py`), formatowanie przez Prettier/Ruff, a typy przez `tsc`/`mypy`.
:::
