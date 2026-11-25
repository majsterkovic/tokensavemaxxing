# Baza Wiedzy — Artykuły, Badania i Publikacje

Zbiór syntez najważniejszych badań empirycznych, postów technicznych twórców harnessów (Cursor, Anthropic, Google, Vercel) oraz analiz inżynierii kontekstu w programowaniu agentowym.

---

## 📚 Indeks Publikacji i Tematów

| Dokument | Tematyka | Kluczowe źródła | Główny wniosek |
|---|---|---|---|
| [context-and-token-economics.md](context-and-token-economics.md) | Ekonomia tokenów, prompt cache, tool definition pruning | Cursor Engineering Blog (2026), Paritok (arXiv:2609.22114) | Usunięcie nieużywanych MCP redukuje stały narzut o 46.9%; kompresja kontekstu kumuluje się kwadratowo od 6. tury. |
| [passive-vs-active-context.md](passive-vs-active-context.md) | Porównanie: pasywny indeks vs dynamiczne skills | Vercel Engineering (2026), HN Discussion #46809708 | 56% wywołań skills jest pomijanych przez model; skondensowany indeks 8KB daje 100% pass rate vs 53% dla skills. |
| [instruction-following-decay.md](instruction-following-decay.md) | Degradacja jakości instrukcji wraz z długością promptu | HumanLayer Research (2026) | Spadek jakości podążania za regułami jest liniowo-równomierny w całym pliku, a nie skoncentrowany w środku ("lost in the middle"). Budżet <2000 tok. |
| [monorepo-context-strategies.md](monorepo-context-strategies.md) | Architektura kontekstu w monorepo i multi-repo | Ivan Magda, Matthew Wong, StartDebugging (2026) | Rozwiązanie problemu wycieku `AGENTS.md` w multi-root workspace; technika uruchamiania agenta z poziomu podkatalogu. |
| [subagents-and-fanout.md](subagents-and-fanout.md) | Wzorce subagentów i delegowania zadań | Claude Code Docs, Google Antigravity Swarm Architecture | Subagenty typu read-only z tanim modelem (Flash/Haiku) redukują zrzut kontekstu z 6000+ tokenów do <500 tokenów syntetycznej konkluzji. |
| [spotify-shunt-and-portal.md](spotify-shunt-and-portal.md) | Spotify: 90% redukcji tokenów w Claude Code | Spotify Engineering (2026), wtyczka `shunt`, AiKA Modes | Wymuszenie przez haki `PreToolUse` oddelegowania ciężkiego I/O (>350 linii) do taniego modelu Gemini Flash. |
| [inkling-2-mini-architecture.md](inkling-2-mini-architecture.md) | Architektura Looped MoE: Inkling 2 Mini | Thinking Machines Lab, Mira Murati (2026) | 26.4B total / 3.4B active w pętli 3-krotnej (48 warstw logicznych), 1M context, wysoka jakość lokalnego kodu. |

---

## 🎯 Jak Korzystać z Bazy Wiedzy

Każdy dokument w tym katalogu ma spójną strukturę:
1. **Kontekst i geneza badania**: Kto badał, na jakiej populacji sesji/kodu, jaka wersja narzędzi.
2. **Kluczowe dane liczbowe**: Wykresy, tabele z pass rate, oszczędności procentowe.
3. **Praktyczne implikacje dla programisty**: Co to bezpośrednio zmienia w Twojej konfiguracji (`.cursor/rules`, `AGENTS.md`, `mcp.json`).
4. **Wskazówki implementacyjne i pułapki**: Czego nie robić, na jakie błędy uważać.
