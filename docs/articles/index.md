---
title: "Baza Wiedzy — Artykuły, Badania i Publikacje"
description: "Zbiór zwięzłych syntez badań empirycznych, benchmarków FinOps i artykułów inżynierskich o optymalizacji kontekstu."
---

Zbiór syntez badań empirycznych oraz postów technicznych twórców harnessów (Cursor, Vercel, Spotify, ETH Zürich, Redis, Emory) dotyczących ekonomii tokenów i inżynierii kontekstu.

## 📚 Indeks Publikacji

| Publikacja | Główny wniosek |
|---|---|
| [Ekonomia Tokenów i Prompt Cache](/tokensavemaxxing/articles/context-and-token-economics/) | Usunięcie nieużywanych MCP tnie stały narzut o **46.9%**; kompresja kumuluje się kwadratowo od 6. tury. |
| [Pasywny Indeks vs Aktywne Skills](/tokensavemaxxing/articles/passive-vs-active-context/) | Modele pomijają **56%** wywołań skills; pasywny indeks 8 KB daje **100%** pass rate vs 53%. |
| [Degradacja Uwagi Instrukcji](/tokensavemaxxing/articles/instruction-following-decay/) | Jakość spada liniowo w całym prompcie, nie tylko w środku — twardy budżet reguł to **<2000 tok**. |
| [Strategie Kontekstu w Monorepo](/tokensavemaxxing/articles/monorepo-context-strategies/) | Izolacja `AGENTS.md` w multi-root workspace i uruchamianie agenta z podkatalogu. |
| [Subagenty, Fan-Out i Izolacja](/tokensavemaxxing/articles/subagents-and-fanout/) | Subagenty `read-only` na tanim modelu redukują zrzut do sesji głównej z 6k do **<500 tok**. |
| [Spotify: Shunt i Portal (90% cięcia)](/tokensavemaxxing/articles/spotify-shunt-and-portal/) | Haki `PreToolUse` kierują ciężkie I/O (>350 linii) do taniego modelu Flash. |
| [Inkling 2 Mini (Looped MoE)](/tokensavemaxxing/articles/inkling-2-mini-architecture/) | 26.4B / 3.4B aktywnych w 3 pętlach (48 warstw logicznych) i okno 1M do pracy lokalnej. |
| [FinOps i Benchmarki Narzędzi](/tokensavemaxxing/articles/token-finops-and-benchmarks/) | RTK tnie **48–81%** spamu CLI; ChatDev pochłania **59.4%** w code review; LOOP tnie replay o **>93%**. |
| [Nawigacja: Grep vs AST vs LSP](/tokensavemaxxing/articles/code-navigation-benchmarks/) | AST tnie **35–55%** kosztów wyszukiwania; LSP jest **5×–1441×** tańsze przy refaktoringu wielu plików. |
| [Ekosystem Agent Skills 2026](/tokensavemaxxing/articles/agent-skills-ecosystem-2026/) | Standard `SKILL.md`, `obra/superpowers`, wzorce Grill Me, Handoff i zasady Karpathy'ego. |
| [Dynamic Context Pruning (ETH Zürich)](/tokensavemaxxing/articles/dynamic-context-pruning-paper-2305-15805/) | Do **80%** tokenów kontekstu można wyciąć w locie bez straty jakości (2× throughput). |
| [Redis: Context Rot i Cache Semantyczny](/tokensavemaxxing/articles/redis-context-pruning-guide/) | Pruning zwalcza zanieczyszczenie uwagi modelu w połączeniu z Semantic Cache. |
| [DYCP: Algorytm Kadane'a (arXiv:2601.07994)](/tokensavemaxxing/articles/dycp-dialogue-pruning-2601-07994/) | *KadaneDial* wycina dygresje w czasie zapytania bez kosztu dodatkowego wywołania LLM. |

## 🎯 Struktura każdego artykułu

1. **Geneza i metodologia** — kto badał i na jakiej próbie.
2. **Liczby i benchmarki** — twarde dane (pass rate, redukcja tokenów).
3. **Implikacje w praktyce** — co zmienić w `.cursor/rules`, `AGENTS.md` lub `mcp.json`.
