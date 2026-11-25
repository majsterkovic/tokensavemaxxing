---
title: "Notatka Narzędziowa: Herdr (`herdrdev`)"
description: "Notatka Narzędziowa: Herdr (`herdrdev`)"
---


# Notatka Narzędziowa: Herdr (`herdrdev`)

> **Rola w ekosystemie**: Multiplekser terminalowy i demon tła ("tmux dla agentów AI"), gwarantujący nieprzerwaną pracę procesów agentowych przy zerwaniu połączenia, uśpieniu systemu lub restarcie okna.

---

## 1. Profil Narzędzia

- **Organizacja**: `https://github.com/herdrdev`
- **Rdzeń**: `herdr-core` (`hc`) — bezgłowy demon systemowy zarządzający procesami w tle.
- **Interfejsy**: `herdr-app` (aplikacja desktopowa) oraz interfejs terminalowy (TUI).
- **Protokół stanu**: OSC 7501 (natywne śledzenie stanu agenta: *working*, *idle*, *blocked*, *done*).

---

## 2. Dlaczego Herdr Rozwiązuje Największy Problem Terminala?

W standardowym terminalu (bash/zsh):
- Zamykasz okno edytora -> proces agenta ginie.
- Usypiasz laptopa na 15 minut -> agent w trakcie pisania testów zostaje przerwany.
- Tracisz połączenie SSH z serwerem -> cały stan sesji przepada.

**W Herdr:**
- Agenci (Claude Code, OpenCode, skrypty Pythona) działają wewnątrz demona `herdr-core`.
- Możesz zamknąć laptopa, przejść do innego pokoju, otworzyć `herdr-app` i wznowić sesję dokładnie w miejscu, w którym została zostawiona.
- Widzisz od razu w panelu bocznym, który agent czeka na Twoją decyzję (*blocked*), a który zakończył zadanie (*done*).

---

## 3. Typowy Workflow z Herdr

```bash
# Uruchomienie sesji wewnątrz Herdr Core
hc new --name "billing-refactor" -- claude

# Lista aktywnych agentów i ich stanów
hc list

# Dołączenie do sesji (attach)
hc attach billing-refactor
```

---

## 4. Rola w Architekturze Tokensavemaxxing

1. **Ochrona przed powtarzaniem pracy**: Przerwany agent w tradycyjnym terminalu wymaga uruchomienia od nowa, co oznacza ponowne przesłanie całego kontekstu i zapłacenie za te same tokeny dwukrotnie.
2. **Rozdzielenie zadań długodystansowych**: Długi refaktoring lub generowanie raportów puszczasz w tle w Herdrze, pracując równolegle nad innym zadaniem w głównym oknie.
