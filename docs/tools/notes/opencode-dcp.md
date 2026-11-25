---
title: "Notatka Narzędziowa: Dynamic Context Pruning (`Tarquinen/opencode-dynamic-context-pruning`)"
description: "Notatka Narzędziowa: Dynamic Context Pruning (`Tarquinen/opencode-dynamic-context-pruning`)"
---


# Notatka Narzędziowa: Dynamic Context Pruning (`Tarquinen/opencode-dynamic-context-pruning`)

> **Rola w ekosystemie**: Wtyczka do OpenCode (`@tarquinen/opencode-dcp`), która w locie (w locie przed wysłaniem do LLM) usuwa martwe i powtarzające się fragmenty historii bez niszczenia logów sesji na dysku.

---

## 1. Profil Narzędzia

- **Repozytorium**: `https://github.com/Tarquinen/opencode-dynamic-context-pruning`
- **Paczka npm**: `@tarquinen/opencode-dcp`
- **Typ**: Wtyczka silnika OpenCode (Dynamic Context Pruning — DCP).
- **Główna idea**: Redukcja rozmiaru promptu wysyłanego do modelu w długich sesjach programistycznych bez modyfikacji oryginalnej historii zapisanej na dysku (Non-Destructive Pruning).

---

## 2. Jak Działa Dynamic Context Pruning (DCP)?

W trakcie 20-turowej sesji kodowania w oknie kontekstowym gromadzi się potężny balast:
1. **Identyczne wywołania narzędzi (Repeated Tool Calls)**: Agent wykonuje `read_file` na tym samym pliku w turze 3, 7 i 12.
2. **Duże payloady błędów (Failed Tool Inputs)**: Wklejenie 2 000 linii stack trace'a, z którego agent już wyciągnął wniosek w turze 4, nadal wisi w kontekście w turze 15.
3. **Zamknięte podzadania (Finished Task Spans)**: Krok 1 (np. konfiguracja bazy) został zakończony i przetestowany, ale wciąż zajmuje miejsce w oknie przy pisaniu widoków Reacta.

### Mechanizm DCP:
- **Zastępowanie lekkimi placeholderami**: DCP analizuje strumień wiadomości i zastępuje archiwalne bloki syntetycznymi znacznikami (np. `[Tool Output: file read already analyzed in turn 4]`).
- **Narzędzie `Compress` sterowane przez model**: Wtyczka udostępnia modelowi narzędzie `Compress`. Gdy agent kończy etap zadania, może sam podjąć decyzję o zwinięciu zakończonego fragmentu do zwięzłego podsumowania blokowego.
- **Wsparcie dla zagnieżdżania**: Kompresje mogą być nakładane warstwowo bez utraty kluczowych konkluzji.

---

## 3. Instalacja i Konfiguracja

```bash
# Instalacja lokalna w projekcie przez OpenCode CLI
opencode plugin add @tarquinen/opencode-dcp@latest

# Lub instalacja globalna dla wszystkich projektów
opencode plugin add --global @tarquinen/opencode-dcp@latest
```

---

## 4. Wpływ na Tokensavemaxxing

- Pozwala prowadzić **długie sesje bez degradacji uwagi modelu**.
- Oszczędza **30% do 65% tokenów wejściowych** w sesjach przekraczających 10 tur.
- Zapewnia pełną zgodność z zasadą nienaruszalności logów audytowych — programista w każdej chwili może przejrzeć pełną, nieobciętą historię na dysku.
