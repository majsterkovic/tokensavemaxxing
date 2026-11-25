---
title: "Notatka Narzędziowa: Claude Code (Anthropic CLI)"
description: "Notatka Narzędziowa: Claude Code (Anthropic CLI)"
---


# Notatka Narzędziowa: Claude Code (Anthropic CLI)

> **Rola w ekosystemie**: Wykonawca zaawansowanego refaktoringu, trudnych zmian architektonicznych i precyzyjnych subagentów badawczych w terminalu.

---

## 1. Profil Narzędzia

- **Twórca**: Anthropic.
- **Model bazowy**: Claude 3.7 Sonnet (domyślnie), Claude 3.5 Haiku (opcja szybka/tania).
- **Format konfiguracji**: `CLAUDE.md` w roocie repozytorium (lub w podkatalogach) oraz plik `.claudeignore`.
- **Typ**: Terminal CLI (interaktywny czat z bezpośrednim dostępem do powłoki, plików i gita).

---

## 2. Instalacja i Pierwsze Uruchomienie

```bash
# Instalacja globalna przez npm
npm install -g @anthropic-ai/claude-code

# Autoryzacja przez konto Anthropic / konsolę
claude login

# Uruchomienie w roocie projektu
cd /home/mariusz/projekty/moj-projekt
claude
```

---

## 3. Konfiguracja pod Tokensavemaxxing

### A. Kompaktowy `CLAUDE.md` (< 150 linii)
Unikaj błędu *"40k CLAUDE.md warning"*. `CLAUDE.md` powinien zawierać wyłącznie zwięzłe fakty:
- Jak budować i testować projekt (`pnpm build`, `pnpm test`).
- Ścisłe konwencje (np. zakaz `any`, użycie Zod).
- **Zero wklejonego kodu przykładowego** — tylko linki/wskaźniki do istniejących plików.

### B. Izolacja Subagentów
Claude Code wspiera delegowanie podzadań do niezależnych subagentów.
- **Złota zasada**: W zleceniu dla subagenta zawsze wymagaj **zwięzłego wniosku i numerów linii**, zabraniając wklejania bloków kodu.

### C. Zarządzanie Historią (`/compact`)
- Sesje w Claude Code akumulują historię komend i odczytów.
- Gdy sesja przekracza 15–20 tur, użyj komendy `/compact`, aby zredukować rozmiar kontekstu.
- Najlepsza praktyka: **Nowe zadanie = nowa sesja** (zakończ obecną przez `Ctrl+C` lub `/exit` i uruchom świeże `claude`).

---

## 4. Kiedy Używać
- Skomplikowany refaktoring algorytmów wieloplikowych.
- Precyzyjne zadania wymagające wysokiej klasy rozumowania (Claude 3.7 Sonnet).
- Bezpośrednie operacje gita, testy TDD i rozwiązywanie konfliktów.

## 5. Kiedy NIE Używać
- Skanowanie całego repozytorium na oślep (do tego użyj lokalnego `gen-repo-map.py` lub taniego modelu Flash).
- Długie sesje-tasiemce obejmujące 10 różnych problemów jednocześnie.
