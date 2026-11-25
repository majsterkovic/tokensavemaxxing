---
title: "Spotify: Jak wtyczka Shunt i Portal obcięły zużycie tokenów w Claude Code o 90%"
description: "Spotify: Jak wtyczka Shunt i Portal obcięły zużycie tokenów w Claude Code o 90%"
---


# Spotify: Jak wtyczka Shunt i Portal obcięły zużycie tokenów w Claude Code o 90%

Analiza studium przypadku Spotify Engineering (*"Portal by Spotify cut my Claude Code token usage by 90%"*, wrzesień 2026).

---

## 1. Problem: Agent to w 80% I/O, a tylko w 20% Rozumowanie

Inżynierowie Spotify zaobserwowali drastyczny wzrost rachunków za tokeny w Claude Code przy pracy nad dużym monorepo w Javie. Analiza telemetryczna wykazała, że:
- Większość zużycia tokenów modelu frontier (Claude 3.7 Sonnet) nie szła na skomplikowane myślenie architektoniczne czy algorytmy.
- **Ponad 80% tokenów pochłaniały rutynowe operacje wejścia/wyjścia (I/O)**: wczytywanie 1000-liniowych plików konfiguracyjnych, przeszukiwanie wielkich katalogów i generowanie powtarzalnego boilerplate'u testowego.
- Wpychanie setek tysięcy tokenów surowego kodu do najdroższego modelu na rynku było ekonomicznym absurdem.

---

## 2. Architektura Rozwiązania: Portal + Wtyczka `shunt`

Spotify wykorzystało swoją wewnętrzną platformę deweloperską **Portal** (komercyjną dystrybucję Backstage) oraz stworzyło oficjalny plugin do Claude Code o nazwie **`shunt`** (`claude plugin install shunt@portal`).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Claude Code (Główny Agent)                      │
│                           Model: Claude 3.7 Sonnet                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  Próba odczytu pliku > 350 linii
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  Hak PreToolUse (Wtyczka `shunt`)                      │
│    Blokada bezpośredniego read_file w oknie kontekstowym Claude        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                Przekierowanie zapytania do klastra Portal
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  Portal AiKA Mode: bulk-reader                         │
│                    Tani model: Gemini 2.5 Flash                        │
│                                                                        │
│   Czyta: 3 000 linii surowego kodu / schematów XML/Java                │
│   Destyluje: Dokładna sygnatura metody i 1-zdaniowy wniosek           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
              Zwrot syntetycznego wyniku do Claude (150 toków)
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Claude Code (Główny Agent)                      │
│        Otrzymuje gotowy wniosek, implementuje rozwiązanie              │
└────────────────────────────────────────────────────────────────────────┘
```

### Kluczowe Elementy Mechanizmu:
1. **PreToolUse Hooks zamiast zaleceń w `CLAUDE.md`**:
   Wcześniejsze próby nakazywania w `CLAUDE.md`: *"nie czytaj dużych plików"* zawodziły w ponad 50% przypadków (model ignorował zalecenie). Hak `PreToolUse` działa na poziomie binarnym silnika — przechwytuje wywołanie narzędzia i fizycznie blokuje odczyt plików powyżej 350 linii.
2. **AiKA Modes w Portalu**:
   Tymczasowe kontenery / bezgłowe agenty (odpowiednik AWS Lambda dla LLM) wyspecjalizowane w dwóch zadaniach:
   - `bulk-reader`: pożeracz surowego tekstu, zwracający jedynie skondensowaną esencję.
   - `code-writer`: generator powtarzalnego boilerplate'u (DTO, gettery/settery, mocki testowe).
3. **Tani silnik wykonawczy**:
   W klastrze Portal zadania I/O wykonuje model **Gemini 2.5 Flash** (ponad 20× tańszy od Sonnet).

---

## 3. Wyniki i Implikacje dla tokensavemaxxing

- **Redukcja o 90%**: Wolumen tokenów wpadających do głównego okna Claude spadł o dziewięć dziesiątych w scenariuszach masowego czytania kodu.
- **Krytyczna uwaga (z dyskusji na Hacker News)**: 90% redukcji dotyczy **kontekstu Claude**, a nie łącznego rachunku infrastrukturalnego (nadal płaci się za tokeny Flash i serwery Portal). Niemniej ze względu na 20-krotną dysproporcję cenową między Sonnet a Flash, całkowity koszt zadania spadł o ~70–75%.
- **Potwierdzenie reguł naszego repozytorium**: Zbieżność 1:1 z naszymi playbookami [03-token-savemaxxing.md](../playbooks/03-token-savemaxxing.md) oraz [subagents-and-fanout.md](subagents-and-fanout.md) — oddzielaj I/O od myślenia architektonicznego.
