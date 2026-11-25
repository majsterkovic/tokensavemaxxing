---
title: "Notatka Narzędziowa: T3 Code (`t3code`)"
description: "Notatka Narzędziowa: T3 Code (`t3code`)"
---

> **Rola w ekosystemie**: Centralny panel graficzny (Control Plane GUI / ADE) integrujący wielu agentów, zarządzający wątkami w modelu skrzynki odbiorczej (Inbox) oraz izolujący gałęzie przez Git Worktrees.

---

## 1. Profil Narzędzia

- **Autor**: Theo Browne (`t3dotgg`) & Ping Labs.
- **Licencja**: Open Source (MIT).
- **Strona**: `https://t3.codes`
- **Typ**: Agentic Development Environment (ADE) — graficzny cockpit łączący Claude Code, Codex, Antigravity i OpenCode.

---

## 2. Kluczowe Właściwości i Architektura

### A. Model Skrzynki Odbiorczej (Inbox Thread Model)
Zamiast bałaganu dziesiątek otwartych kart w przeglądarce i terminali:
- Zadania agentów są prezentowane jak wątki e-mailowe.
- Możesz wątek:
  - **Przypiąć (Pin)** — aktywne zadanie o wysokim priorytecie.
  - **Uśpić (Snooze)** — czeka na odpowiedź serwera CI lub długi test.
  - **Zarchiwizować (Settle)** — zadanie wykonane, pull request otwarty.
- Dostępny jest tryb **"God Thread"** — wysyłanie poleceń koordynujących do wielu agentów jednocześnie.

### B. Praca Równoległa na Git Worktrees
Tradycyjnie nie możesz uruchomić dwóch agentów w jednym folderze gita na dwóch różnych branchach (jeden nadpisuje pliki drugiego).
T3 Code natywnie tworzy **Git Worktrees**:
- Agent A pracuje nad featurem na gałęzi `feature/stripe` w osobnym katalogu roboczym.
- Agent B naprawia błąd w CSS na gałęzi `fix/navbar` w drugim katalogu roboczym.
- Żaden agent nie blokuje Twojego głównego drzewa plików.

### C. Zasada BYOK (Bring Your Own Key)
T3 Code łączy się bezpośrednio z Twoimi kluczami API (Anthropic, OpenAI, Google) lub subskrypcjami CLI bez dodatkowych marż.

---

## 3. Higiena i Bezpieczeństwo (Telemetria)

Podczas szybkiego rozwoju projektu społeczność zwróciła uwagę na domyślnie włączone moduły telemetryczne (PostHog).
- **Rekomendacja**: W ustawieniach konfiguracyjnych upewnij się, że opcja raportowania telemetrii jest wyłączona (`telemetry: false`), a wrażliwe klucze API są przechowywane w zmiennych środowiskowych systemowego pęku kluczy.

---

## 4. Kiedy Używać
- Prowadzenie 2–4 równoległych zadań programistycznych jednocześnie.
- Wygodny podgląd diffów i zatwierdzanie zmian bez konieczności ciągłego przełączania okien terminala.
- Zdalny nadzór nad pracą agentów z poziomu telefonu lub przeglądarki.
