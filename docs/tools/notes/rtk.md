---
title: "Notatka Narzędziowa: RTK (Rust Token Killer — `rtk-ai/rtk`)"
description: "Notatka Narzędziowa: RTK (Rust Token Killer — `rtk-ai/rtk`)"
---

> **Rola w ekosystemie**: Wysokowydajny proxy CLI w języku Rust, redukujący liczbę tokenów w wyjściu poleceń przed wysłaniem do kontekstu agenta. Autorzy deklarują **do 90% mniej wyjścia poleceń** ([README](https://github.com/rtk-ai/rtk), odczyt 26.11.2026; nie zweryfikowano niezależnie). Sami zastrzegają, że to nie jest taka sama redukcja rachunku.

---

## 1. Profil Narzędzia

- **Repozytorium**: `https://github.com/rtk-ai/rtk`
- **Język**: Rust.
- **Narzut czasowy**: według autorów poniżej 25 ms na polecenie (nie mierzono tutaj).
- **Zasada działania**: Działa jako transparentny filtr/pośrednik (proxy) między poleceniami powłoki uruchamianymi przez agenta (`git`, `cargo`, `pytest`, `npm`, `docker`, `kubectl`) a oknem kontekstowym LLM.

---

## 2. Jaki Problem Rozwiązuje RTK?

Gdy agent kodujący uruchamia polecenia w terminalu:
- `npm test` lub `cargo test` wypisuje 500 linii zielonych testów, które przeszły pomyślnie.
- `git status` wypisuje listę 80 plików nieśledzonych z instrukcjami pomocy gita.
- `docker build` wypisuje setki linii logów pobierania warstw i pasków postępu ANSI.

**Rezultat bez RTK**:
Agent wczytuje do historii 4 000 – 10 000 tokenów bezużytecznych logów. W kolejnych turach płacisz za te logi wielokrotnie.

**Rezultat z RTK**:
RTK przechwytuje strumień `stdout` / `stderr` i poddaje go inteligentnej kompresji deterministycznej:
1. **Wycinanie ANSI i pasków postępu**: Usuwa kody kolorów terminala, paski ładowania i powtarzające się białe znaki.
2. **Kondensacja testów jednostkowych**: Zbija 400 linii przechodzących testów do jednej linijki (`✅ 412 passed in 1.4s`), a na wierzch wyciąga **wyłącznie testy, które oblały (failures)** wraz ze zwięzłym stack trace.
3. **Grupowanie błędów kompilacji**: Grupuje błędy `tsc` / `cargo` per plik, eliminując duplikaty.
4. **Zwijanie drzewa gita**: Zastępuje rozwlekły listing skróconą matrycą zmodyfikowanych katalogów.

---

## 3. Instalacja i Integracja

### A. Instalacja binarnej wersji
```bash
# macOS / Linux (Homebrew)
brew install rtk

# Windows
winget install rtk-ai.rtk

# Lub oficjalny skrypt (przeczytaj go przed uruchomieniem)
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# Sprawdzenie, że to właściwy program: w crates.io istnieje inne narzędzie o nazwie "rtk"
rtk gain
```

### B. Integracja z agentem
```bash
rtk init -g
```
Aktualne polecenia i opcje dla poszczególnych agentów: [README RTK](https://github.com/rtk-ai/rtk).

### C. Podpięcie pod Claude Code / OpenCode / Antigravity
W Claude Code lub OpenCode RTK może być wywoływany automatycznie poprzez wrapper powłoki lub hak `PreToolUse`:
- Zamiast `pytest` agent wywołuje wariant przez `rtk` (np. `rtk pytest`).
- Wtyczka może aliasować domyślne polecenia powłoki: `git`, `npm`, `cargo`, `pytest`, `docker`.

---

## 4. Śledzenie Oszczędności: `rtk gain`

RTK posiada wbudowany licznik zaoszczędzonych tokenów:

```bash
rtk gain
```
Wyświetla estymację:
- Liczbę przetworzonych komend CLI.
- Wolumen surowych tokenów wejściowych vs tokenów po kompresji.
- Z flagą `--quota` szacunek względem miesięcznego limitu subskrypcji (opcje: `rtk gain --help`, sprawdzone w wersji 0.51.0).

---

## 5. Zastosowanie w Metodologii Tokensavemaxxing

> Przykłady **ilustracyjne** (⚠️ niezweryfikowane, bez metodyki pomiaru). Rzeczywisty zysk sprawdź przez `rtk gain`.

| Bez RTK | Z RTK | Zysk |
|---|---|---|
| `git status` + `git diff` (~2 500 tokenów) | Skondensowany diff bez szumu (~400 tokenów) | **−84%** |
| `pytest` z 50 testami (~3 800 tokenów) | Tylko błąd w `test_auth.py:42` (~250 tokenów) | **−93%** |
| `npm run build` z ostrzeżeniami (~1 800 tokenów) | Raport błędów w 5 liniach (~120 tokenów) | **−93%** |

RTK stanowi pierwszą linię obrony w terminalu — zapobiega zanieczyszczaniu historii czatu śmieciami z procesów systemowych.
