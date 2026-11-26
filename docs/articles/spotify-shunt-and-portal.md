---
title: "Spotify: Wtyczka Shunt i Portal Obniżają Zużycie Tokenów w Claude Code"
description: "Studium przypadku Spotify: delegowanie masowego czytania i boilerplate'u do tańszego modelu przez haki PreToolUse."
---

Analiza artykułu [Portal by Spotify cut my Claude Code token usage by 90%](https://engineering.atspotify.com/2026/09/portal-by-spotify-cut-my-claude-code-token-usage-by-90) (Dimitri Mazmanov, Principal PM, 3.09.2026).

---

## 1. Problem

Dużą część zużycia w Claude Code stanowiła praca, która nie wymaga najmocniejszego modelu: czytanie wielu plików i generowanie przewidywalnego kodu. Całe pliki trafiały do kontekstu głównej sesji.

---

## 2. Rozwiązanie: Portal i wtyczka `shunt`

- **Tryby AiKA w Portalu:** `bulk-reader` (czytanie i streszczanie) oraz `code-writer` (testy, szkielety konfiguracji, stuby typów). W przykładach działa na nich Gemini 2.5 Flash z temperaturą 0,2.
- **Haki `PreToolUse` we wtyczce `shunt`:**
  - `check-file-size` blokuje odczyt całego dużego pliku. Domyślny próg to **350 linii** (zmienna `SHUNT_MIN_LINES`). Odczyty zakresowe przechodzą.
  - `check-bash-read` przechwytuje czytanie przez `cat`, `head`, `tail`, `less` i `more`. Polecenia z potokiem przechodzą.
- **Skrypty:** `bulk-read --question --paths` oraz `code-write --spec --reference [--target]`, a do tego dwa skille.

```
Claude Code próbuje przeczytać duży plik
              │
              ▼
Hak PreToolUse (shunt) blokuje pełny odczyt
              │
              ▼
Tryb bulk-reader w Portalu (tańszy model) czyta pliki i odpowiada na pytanie
              │
              ▼
Do kontekstu Claude trafia tylko odpowiedź
```

---

## 3. Wynik i jego zakres

- **Około 90% to średnia oszczędność przy masowym czytaniu w czterech scenariuszach** na monorepo w Javie.
- Liczba opisuje **tokeny Claude**, a nie łączny rachunek. Tokeny tańszego modelu i infrastrukturę trzeba doliczyć; artykuł nie podaje łącznej oszczędności kosztu.
- Oszczędności z `code-writer` **nie zostały określone liczbowo**.
- **Edycji i trudnego rozumowania nie da się w ten sposób delegować**, bo wymagają dokładnej treści w głównym modelu.
- Artykuł opisuje też ograniczenie czasu wywołania do 30 sekund.

---

## 4. Wnioski dla tokensavemaxxing (autorskie)

- Hak wymusza zachowanie mechanicznie, a instrukcja w pliku reguł jest tylko prośbą do modelu. Skuteczności obu podejść artykuł tu nie porównuje liczbowo.
- Idea jest zbieżna z [subagentami](/tokensavemaxxing/articles/subagents-and-fanout/): masowy odczyt trzymaj poza głównym kontekstem. Nie jest to niezależne potwierdzenie liczb z [Playbooka 03](/tokensavemaxxing/playbooks/03-token-savemaxxing/).
- Streszczenie może coś pominąć. Przed edycją przeczytaj właściwy fragment bezpośrednio.

## Źródła

- [Spotify Engineering: Portal by Spotify cut my Claude Code token usage by 90%](https://engineering.atspotify.com/2026/09/portal-by-spotify-cut-my-claude-code-token-usage-by-90)
