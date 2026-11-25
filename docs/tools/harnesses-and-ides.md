# Środowiska Wykonawcze i Harnessy

Szczegółowy przegląd najpopularniejszych harnessów i platform agentowych pod kątem zarządzania kontekstem, zachowania pamięci podręcznej i integracji w ekosystemie deweloperskim.

---

## 1. T3 Code (`t3code`) — Unified Agentic Development Environment

- **Twórca**: Theo Browne (`t3dotgg`) / Ping Labs.
- **Rola**: Centralna warstwa kontrolna (Control Plane GUI) integrująca pod jednym dachem Claude Code, Codex, Antigravity, Cursor i OpenCode.
- **Kluczowe właściwości**:
  - Zarządzanie zadaniami w modelu skrzynki pocztowej (Inbox).
  - Wbudowane wsparcie dla Git Worktrees — możliwość równoległego uruchamiania 3 agentów na 3 różnych gałęziach bez kolizji w jednym repozytorium.
  - BYOK (Bring Your Own Key) — brak pośredników w rozliczaniu tokenów.
  - Lekki backend serwerowy umożliwiający kontrolę procesów z poziomu przeglądarki lub aplikacji mobilnej.

---

## 2. Herdr (`herdr-core`, `herdr-app`) — Multiplexer z Demonem w Tle

- **Organizacja**: `herdrdev`.
- **Rola**: Odpowiednik `tmux` zaprojektowany od podstaw dla agentów AI ("tmux built for coding agents").
- **Kluczowe właściwości**:
  - **Trwałość sesji (Session Persistence)**: Procesy agentów żyją w tle w demonie `herdr-core` (`hc`). Odłączenie SSH, restart GUI lub uśpienie systemu nie przerywa pracy agenta.
  - **Protokół OSC 7501**: Śledzenie stanów agenta (*working*, *idle*, *blocked*, *done*).
  - **Praca rozproszona**: Zarządzanie agentami działającymi lokalnie na maszynie oraz zdalnie na serwerach/VPS.

---

## 3. OpenCode (`anomalyco/opencode`) — Elastyczny Agent TUI

- **Rola**: Otwarty terminalowy agent programistyczny wspierający ponad 75 dostawców LLM (w tym modele lokalne przez Ollama/LM Studio).
- **Kluczowe właściwości**:
  - **Tryb `plan` vs `build`**: Pozwala precyzyjnie rozdzielić fazę architektoniczną (read-only) od fazy modyfikacji kodu.
  - **LSP Diagnostics**: Bezpośredni odczyt błędów i sygnatur typów z serwerów językowych (Language Server Protocol), eliminujący konieczność zgadywania przez model.
  - **GitHub Actions Integration**: Komendy `opencode github install / run` do automatyzacji CI/CD.

---

## 4. Antigravity CLI (`agy`) — Orkiestracja Rojów i Dynamiczne Skrypty

- **Twórca**: Google DeepMind.
- **Rola**: Zaawansowany harness agentowy wspierający pojedyncze agenty, wyspecjalizowane subagenty oraz dynamiczne skrypty workflow w Pythonie (`run_workflow`) i roje (`swarm`).
- **Kluczowe właściwości**:
  - **Arbitraż Flash vs Pro**: Skanowanie kodu i ekstrakcja wiedzy przez tanie subagenty Flash, decyzje architektoniczne przez modele Pro.
  - **Reactive Wakeup**: Reaktywny system komunikatów bez marnowania zasobów na pętle odpytywania (no polling).

---

## 5. Claude Code — Terminal CLI od Anthropic

- **Rola**: Oficjalne narzędzie konsolowe Anthropic zintegrowane z modelami Claude 3.7 Sonnet i Claude 3.5 Haiku.
- **Kluczowe właściwości**:
  - Znakomite rozumowanie przy skomplikowanym refaktoringu.
  - Wbudowana obsługa subagentów badawczych z odrębnym oknem kontekstowym.
  - Konfiguracja przez zwięzły plik `CLAUDE.md`.

---

## 6. OpenAI Codex / CLI — Narzędzia Rozumujące

- **Rola**: Dedykowane interfejsy i modele rozumujące OpenAI (o3-mini, GPT-4o).
- **Kluczowe właściwości**:
  - Znakomita precyzja w skomplikowanych algorytmach, logice biznesowej i analizie matematycznej.
  - Modele serii "o" generują ukryte łańcuchy myślowe (reasoning tokens), co podnosi skuteczność w trudnych zadaniach architektonicznych.

---

## 7. Środowisko WSL i Modele Lokalne (12 GB VRAM)

- **WSL (Windows Subsystem for Linux)**:
  - Zapewnia natywne środowisko POSIX dla wszystkich agentów CLI (ripgrep, git, Python, bash).
  - **Zasada wydajności**: Projekty muszą znajdować się w systemie linuksowym (`/home/mariusz/...`), a nie pod montowaniem `/mnt/c/`.
- **Modele Lokalne (Ollama / vLLM w WSL)**:
  - Karta 12 GB VRAM pozwala na lokalne uruchomienie modeli:
    - **Qwen 2.5 Coder 7B (Q8)** / **14B (Q4_K_M)** — kodowanie bez opłat API.
    - **DeepSeek-R1-Distill-Qwen-7B** — lokalne planowanie ("Thinking Mini").
  - Zapewniają **zerowy koszt tokenowy** w fazie wstępnej analizy, generowania testów jednostkowych i lokalnego formatowania.
