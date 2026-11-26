---
title: "Inwentarz Narzędzi — Kompletny Stos Technologiczny"
description: "Kompletny przegląd stosu technologicznego (T3 Code, Herdr, Claude Code, Codex, Antigravity, OpenCode, WSL, Local LLM) i routing zadań."
---

Szczegółowy przegląd i charakterystyka wszystkich narzędzi dostępnych w Twoim środowisku deweloperskim, wraz z przypisaniem ról w architekturze **tokensavemaxxing**.

---

## 🏗️ Warstwowa Architektura Twojego Stosu

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1. WARSTWA ZARZĄDZANIA SESJAMI & MULTIPLEKSERY (Control Plane)         │
│  - T3 Code (ADE): Centralny cockpit GUI, inbox zadań, multi-agent inbox │
│  - Herdr (Core/App): "tmux dla agentów", demony w tle, tracking statusu │
├─────────────────────────────────────────────────────────────────────────┤
│  2. AGENCI WYKONAWCZY & CLI HARNESSY (Execution Engines)                │
│  - Claude Code: Szybkie zadania terminalowe, zaawansowane subagenty     │
│  - Codex (OpenAI): Precyzyjne operacje kodujące                         │
│  - Antigravity (AGY): Orkiestracja Python workflows, swarmy, skills     │
│  - OpenCode: Otwarty TUI agent, 75+ modeli, LSP, natywne modele lokalne │
├─────────────────────────────────────────────────────────────────────────┤
│  3. SILNIKI WNIOSKOWANIA (Inference Tier)                               │
│  - Cloud Frontier: modele klasy Opus/Sonnet i Pro (Architektura)        │
│  - Cloud Scout: modele klasy Flash / Haiku (Szybki research)            │
│  - Local Models (12 GB VRAM): Qwen 2.5 Coder 7B/14B, DeepSeek-R1-Distill│
├─────────────────────────────────────────────────────────────────────────┤
│  4. PODŁOŻE SYSTEMOWE (System Substrate)                                │
│  - WSL (Linux): Wydajne środowisko POSIX, ripgrep, Git, I/O w /home/... │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Warstwa Kontrolna i Multipleksery (Control Planes)

### A. T3 Code (`t3code`)
- **Czym jest**: Otwarty (MIT) graficzny panel kontrolny (Agentic Development Environment — ADE) stworzony przez Theo Browne'a (`t3dotgg`) i zespół Ping Labs.
- **Rola w systemie**: Główny interfejs (cockpit) łączący pod jednym dachem Claude Code, Codex, Antigravity, Cursor i OpenCode.
- **Kluczowe mechanizmy**:
  - **Model skrzynki odbiorczej (Inbox-Style)**: Zadania i wątki agentów są zarządzane jak maile (pinowanie, odkładanie na później, "god thread" do masowych aktualizacji).
  - **BYOK (Bring Your Own Key)**: Bezpośrednie połączenie z Twoimi subskrypcjami i kluczami API (brak prowizji i narzutów pośredników).
  - **Git Worktrees & Diffs**: Wbudowany podgląd diffów i równoległa praca na gałęziach bez konfliktów w drzewie roboczym.
  - **Dostęp zdalny**: Lekki serwer umożliwiający sterowanie agentami z poziomu przeglądarki lub telefonu.
- **Uwaga bezpieczeństwa**: Pamiętaj o wyłączeniu telemetrii (np. PostHog), która budziła dyskusje w społeczności open-source.

### B. Herdr (`herdr-core` / `hc`, `herdr-app`)
- **Czym jest**: Zaawansowany multiplekser terminalowy i demon tła stworzony z myślą o agentach AI ("tmux built for coding agents", organizacja `herdrdev`).
- **Rola w systemie**: Zapewnia **ciągłość pracy agentów (persistence)**. Gdy zamykasz terminal, usypiasz laptopa lub restartujesz aplikację, agenci uruchomieni wewnątrz demona `herdr-core` kontynuują pracę.
- **Kluczowe mechanizmy**:
  - **Śledzenie statusu (OSC 7501)**: W przeciwieństwie do tradycyjnego tmuksa, Herdr rozumie stan agenta: *working*, *idle*, *blocked* (oczekiwanie na input usera), *done*.
  - **Multi-Machine Management**: Agregacja procesów lokalnych i zdalnych (przez SSH) w jednym bocznym pasku stanu.
  - **Interfejsy**: Zarówno TUI terminalowe, jak i lekka aplikacja desktopowa (`herdr-app`).

---

## 2. Agenci Wykonawczy i CLI (Execution Engines)

### A. Claude Code
- **Cechy**: Oficjalne narzędzie CLI firmy Anthropic.
- **Mocna strona**: Znakomite rozumowanie przy skomplikowanym kodzie, bezpośrednia integracja z narzędziami terminala i sprawna obsługa subagentów badawczych.
- **Zastosowanie w tokensavemaxxing**: Idealny do implementacji krytycznych algorytmów i refaktoringu.

### B. Codex (OpenAI CLI / Assistant)
- **Cechy**: Ekosystem agentowy OpenAI.
- **Mocna strona**: Potężna logika matematyczna i algorytmiczna modeli rozumujących (reasoning tokens).
- **Zastosowanie**: Rozwiązywanie zawiłych problemów logiki biznesowej i audyt bezpieczeństwa.

### C. Antigravity CLI (`agy`)
- **Cechy**: Środowisko agentowe Google DeepMind z natywną obsługą dynamicznych workflow w Pythonie (`run_workflow`), subagentów oraz rojów (`swarm`).
- **Mocna strona**: Swobodny arbitraż między modelami `flash` (tani i szybki) a `pro` (złożone planowanie), system skills i zarządzanie zadaniami w tle bez aktywnego odpytywania (reactive wakeup).
- **Zastosowanie**: Wielofazowe potoki deweloperskie, badania bazy kodu na dużą skalę i koordynacja zadań.

### D. OpenCode (`anomalyco/opencode`)
- **Cechy**: W pełni otwartoźródłowy terminalowy agent AI (TUI) łączący się z ponad 75 dostawcami modeli.
- **Mocna strona**:
  - **Tryb dwuagentowy**: Natywny podział na tryb `plan` (tylko do odczytu, analiza architektury) oraz `build` (pełne uprawnienia do edycji kodu).
  - **LSP Diagnostics**: Automatyczna integracja z Language Server Protocol projektu — agent widzi błędy składniowe i definicje typów wprost z kompilatora.
  - **Wsparcie modeli lokalnych**: Prosta integracja z Ollama i serwerami kompatybilnymi z OpenAI API.

---

## 3. Środowisko Uruchomieniowe: WSL (Windows Subsystem for Linux)

Twoim fundamentem wykonawczym jest **WSL** (Linux na Windowsie).

### Żelazna Zasada Wydajności I/O w WSL:
> ⚠️ **NIGDY NIE TRZYMAJ PROJEKTÓW W `/mnt/c/...`**
> Dostęp do plików systemu Windows z poziomu WSL przez mostek `/mnt/c/` generuje potężny narzut na operacjach I/O (operacje gita, ripgrepa i testów bywają wielokrotnie wolniejsze).

- **Zawsze pracuj w linuksowym systemie plików**: `/home/mariusz/projekty/...`.
- **Dostęp z Windowsa**: W eksploratorze plików Windows wpisuj ścieżkę sieciową `\\wsl$\Ubuntu\home\mariusz\...`.
- **Zaleta dla tokensavemaxxing**: Błyskawiczny czas reakcji `ripgrep`, natywne skrypty bashowe, narzędzia `ast-grep` i skrypty Pythonowe bez emulacji windowsowej.

---

## 4. Warstwa Modeli Lokalnych (Local Models — 12 GB VRAM)

Dysponujesz kartą z **12 GB pamięci VRAM** (np. RTX 3060 12GB lub RTX 4070 12GB). W architekturze **tokensavemaxxing** modele lokalne mogą przejąć część zadań **bez opłat za API** (nadal kosztują prąd, sprzęt i czas).

### A. Co mieści się w 12 GB VRAM?

| Model | Rozmiar / Kwantyzacja | Wymagany VRAM | Rola w workflow |
|---|---|---|---|
| **Qwen 2.5 Coder 7B** | Q8_0 / FP16 | ~8–9 GB | Znakomity lokalny generator kodu, szybkie refaktory, testy jednostkowe |
| **Qwen 2.5 Coder 14B** | Q4_K_M | ~9–10.5 GB | Zaawansowane wnioskowanie, świetna znajomość TS/Python/Go |
| **DeepSeek-R1-Distill-Qwen-7B** | Q5_K_M / Q6_K | ~6–8 GB | Lokalny model rozumujący ("Thinking Mini") do planowania i RCA |
| **Phi-4 (14B)** | Q4_K_M | ~10 GB | Znakomita logika i analiza matematyczna |
| **SmolLM2 1.7B / Qwen 1.5B** | Q8_0 | ~2 GB | Błyskawiczny routing, klasyfikacja plików, ekstrakcja metadanych |

### B. Jak Wykorzystać Modele Lokalne w tokensavemaxxing:
1. **Darmowy Pre-Screening i Klasyfikacja**: Zamiast pytać płatny model o to, które pliki w katalogu odpowiadają za routing, lokalny Qwen 7B może to wstępnie przejrzeć (czas i jakość sprawdź u siebie).
2. **Generowanie Testów Jednostkowych**: Proste testy funkcji czystych (pure functions) lokalny model 14B często potrafi wygenerować; wynik trzeba uruchomić i przejrzeć.
3. **Audyt Bezpieczeństwa Prywatnych Danych**: Kod zawierający wrażliwe schematy baz lub wewnętrzne algorytmy nie musi opuszczać Twojego komputera.
4. **Backend dla OpenCode**: W OpenCode możesz wskazać `http://localhost:11434/v1` (Ollama) jako providera dla trybu `plan` lub `build`.

---

## 5. Podsumowanie Ról w Ekosystemie

| Rola | Rekomendowane Narzędzie | Model | Koszt | Dedykowana notatka |
|---|---|---|---|---|
| **Zarządzanie sesjami i wątkami** | T3 Code / Herdr | — | 0 | [T3 Code](/tokensavemaxxing/tools/notes/t3-code/), [Herdr](/tokensavemaxxing/tools/notes/herdr/) |
| **Eksploracja i Scout (czytanie)** | Antigravity / OpenCode | Gemini Flash / Haiku / Qwen 7B | Bardzo niski / 0 | [Antigravity CLI](/tokensavemaxxing/tools/notes/antigravity-cli/), [OpenCode](/tokensavemaxxing/tools/notes/opencode/) |
| **Architektura i Planowanie** | Claude Code / T3 Code / Antigravity | Mocny model chmurowy | Płatny (inwestycja) | [Claude Code](/tokensavemaxxing/tools/notes/claude-code/), [Codex](/tokensavemaxxing/tools/notes/codex/) |
| **Trudna Implementacja & RCA** | Claude Code / Codex | Mocny model chmurowy | Płatny | [Claude Code](/tokensavemaxxing/tools/notes/claude-code/), [Codex](/tokensavemaxxing/tools/notes/codex/) |
| **Masowy Refaktoring w tle** | Herdr + OpenCode | Qwen 2.5 Coder 14B / Flash | 0 / Minimalny | [Herdr](/tokensavemaxxing/tools/notes/herdr/), [OpenCode](/tokensavemaxxing/tools/notes/opencode/) |
| **Modele Lokalne (0 zł / 0 tokenów)**| Ollama / WSL | Qwen 2.5 Coder, DeepSeek R1 7B | **0 zł** | [Modele Lokalne 12 GB](/tokensavemaxxing/tools/notes/local-models-12gb/) |
| **Środowisko Uruchomieniowe**| WSL (Ubuntu/Linux) | — | — | [WSL](/tokensavemaxxing/tools/notes/wsl/) |
