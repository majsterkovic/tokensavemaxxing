---
title: "Notatka Narzędziowa: Claude Code (Anthropic CLI)"
description: "Notatka Narzędziowa: Claude Code (Anthropic CLI)"
---

> **Rola w ekosystemie**: Wykonawca zaawansowanego refaktoringu, trudnych zmian architektonicznych i precyzyjnych subagentów badawczych w terminalu.

---

## 1. Profil Narzędzia

- **Twórca**: Anthropic.
- **Modele**: rodzina Claude (Opus / Sonnet / Haiku); model domyślny i dostępne wersje sprawdzisz komendą `/model`.
- **Format konfiguracji**: `CLAUDE.md` w roocie repozytorium (lub w podkatalogach) oraz `.claude/settings.json` (uprawnienia). [Dokumentacja ustawień](https://code.claude.com/docs/en/settings) nie opisuje pliku `.claudeignore`; dostęp do plików blokuj przez `permissions.deny`, np. `"Read(./.env)"`.
- **Typ**: Terminal CLI (interaktywny czat z bezpośrednim dostępem do powłoki, plików i gita).

---

## 2. Instalacja i Pierwsze Uruchomienie

```bash
# Instalacja globalna przez npm
npm install -g @anthropic-ai/claude-code

# Uruchomienie w roocie projektu (logowanie: komenda /login wewnątrz sesji)
cd /home/mariusz/projekty/moj-projekt
claude
```

---

## 3. Konfiguracja pod Tokensavemaxxing

### A. Kompaktowy `CLAUDE.md` (np. < 150 linii; [dokumentacja](https://code.claude.com/docs/en/memory) zaleca mniej niż 200)
Unikaj błędu *"40k CLAUDE.md warning"*. `CLAUDE.md` powinien zawierać wyłącznie zwięzłe fakty:
- Jak budować i testować projekt (`pnpm build`, `pnpm test`).
- Ścisłe konwencje (np. zakaz `any`, użycie Zod).
- **Zero wklejonego kodu przykładowego** — tylko linki/wskaźniki do istniejących plików.

### B. Izolacja Subagentów
Claude Code wspiera delegowanie podzadań do niezależnych subagentów.
- **Złota zasada**: W zleceniu dla subagenta zawsze wymagaj **zwięzłego wniosku i numerów linii**, domyślnie bez dużych bloków kodu (krótki cytat, gdy od treści zależy decyzja).

### C. Zarządzanie Historią (`/compact`)
- Sesje w Claude Code akumulują historię komend i odczytów.
- Gdy sesja robi się długa (np. 15–20 tur, próg umowny), użyj komendy `/compact`, aby zredukować rozmiar kontekstu.
- Najlepsza praktyka: **Nowe zadanie = nowa sesja** (zakończ obecną przez `Ctrl+C` lub `/exit` i uruchom świeże `claude`).

---

## 4. Kiedy Używać
- Skomplikowany refaktoring algorytmów wieloplikowych.
- Precyzyjne zadania wymagające wysokiej klasy rozumowania.
- Bezpośrednie operacje gita, testy TDD i rozwiązywanie konfliktów.

## 5. Kiedy NIE Używać
- Skanowanie całego repozytorium na oślep (do tego użyj lokalnego `gen-repo-map.py` lub taniego modelu Flash).
- Długie sesje-tasiemce obejmujące 10 różnych problemów jednocześnie.
