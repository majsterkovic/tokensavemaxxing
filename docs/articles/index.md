---
title: "Baza Wiedzy — Artykuły, Badania i Publikacje"
description: "Syntezy publikacji, benchmarków i artykułów inżynierskich o optymalizacji kontekstu, z linkami do źródeł."
---

Syntezy prac naukowych, wpisów inżynierskich i poradników o ekonomii tokenów i inżynierii kontekstu. Mają różną wagę dowodową, od preprintów po materiały dostawców i opracowania autorskie.

## 📚 Indeks publikacji

| Publikacja | Główny wniosek |
|---|---|
| [Ekonomia Tokenów i Prompt Cache](/tokensavemaxxing/articles/context-and-token-economics/) | Cursor: narzędzia MCP na żądanie to **−46,9% tokenów** w sesjach wywołujących MCP. Paritok: kompresja ~2% prefiksu na turę, kumulująca się do progu ok. 6. tury. |
| [Pasywny Indeks vs Skille](/tokensavemaxxing/articles/passive-vs-active-context/) | Vercel: skill nieużyty w **56%** przypadków; indeks dokumentacji w `AGENTS.md` **100%** vs 53% baseline. |
| [Przeciążenie Instrukcjami](/tokensavemaxxing/articles/instruction-following-decay/) | Poradnik HumanLayer: mniej instrukcji i krótki plik. Budżet 2000 tok to konwencja repo. |
| [Strategie Kontekstu w Monorepo](/tokensavemaxxing/articles/monorepo-context-strategies/) | Ładowanie instrukcji na żądanie i start agenta w podfolderze. |
| [Subagenty, Fan-Out i Izolacja](/tokensavemaxxing/articles/subagents-and-fanout/) | Chronią główny kontekst; łączne zużycie tokenów może rosnąć. |
| [Spotify: Shunt i Portal](/tokensavemaxxing/articles/spotify-shunt-and-portal/) | Ok. 90% mniej tokenów Claude przy masowym czytaniu (4 scenariusze). |
| [Inkling 2 Mini](/tokensavemaxxing/articles/inkling-2-mini-architecture/) | Według producenta: 26,4 mld / 3,4 mld aktywnych parametrów, 48 zastosowań warstw z 24 zapisanych. |
| [FinOps i Benchmarki Narzędzi](/tokensavemaxxing/articles/token-finops-and-benchmarks/) | ChatDev: **59,4%** tokenów w code review; RTK: 48–81% wyjścia CLI w danych jednego autora. |
| [Nawigacja: Grep vs AST vs LSP](/tokensavemaxxing/articles/code-navigation-benchmarks/) | Zarys AST: −35–55% kosztu w trzech repozytoriach; LSP w badaniu zwykle droższy od grep. |
| [Ekosystem Agent Skills 2026](/tokensavemaxxing/articles/agent-skills-ecosystem-2026/) | Format `SKILL.md`, przykładowe paczki i katalogi. |
| [Dynamic Context Pruning (arXiv:2305.15805)](/tokensavemaxxing/articles/dynamic-context-pruning-paper-2305-15805/) | Do 80% kontekstu bez istotnego pogorszenia i do 2× przepustowości — wewnątrz dostrojonego modelu. |
| [Redis: Pruning i Cache Semantyczny](/tokensavemaxxing/articles/redis-context-pruning-guide/) | Przewodnik dostawcy; dla kodu pruning całych jednostek logicznych. |
| [DYCP (arXiv:2601.07994)](/tokensavemaxxing/articles/dycp-dialogue-pruning-2601-07994/) | *KadaneDial* wybiera ciągłe fragmenty dialogu bez dodatkowych wywołań LLM. |

## 🎯 Jak czytać te opracowania

- **Źródła** są na końcu artykułów. Nie wszystkie opracowania opisują metodykę lub próbę, bo nie każde źródło ją podaje.
- Liczby dotyczą konkretnych eksperymentów. **Nie sumuj ich** i nie traktuj jako obietnicy dla swojego projektu.
- Fragmenty oznaczone jako konwencja, propozycja lub ⚠️ niezweryfikowane nie są wynikami badań.
