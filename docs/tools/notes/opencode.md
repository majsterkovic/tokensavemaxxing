---
title: "Notatka Narzędziowa: OpenCode (`anomalyco/opencode`)"
description: "Notatka Narzędziowa: OpenCode (`anomalyco/opencode`)"
---

> **Rola w ekosystemie**: Wszechstronny, otwartoźródłowy agent TUI/CLI integrujący ponad 75 dostawców LLM, z natywnym wsparciem dla modeli lokalnych i Language Server Protocol (LSP).

---

## 1. Profil Narzędzia

- **Repozytorium**: `https://github.com/anomalyco/opencode`
- **Typ**: Terminal TUI / CLI / Desktop App.
- **Licencja**: Open-source.
- **Kluczowe właściwości**:
  - Dwa wbudowane tryby pracy: **`plan`** (analiza i architektura tylko do odczytu) oraz **`build`** (pełny coding).
  - Natywna integracja z serwerami językowymi (LSP) — pobiera diagnostykę i definicje typów wprost z kompilatora.
  - Elastyczne podłączanie modeli: Anthropic, OpenAI, Groq, Ollama / vLLM (modele lokalne).

---

## 2. Instalacja i Konfiguracja

```bash
# Instalacja przez oficjalny skrypt
curl -fsSL https://opencode.ai/v2/install | bash

# Lub przez npm
npm i -g @opencode/cli@latest

# Logowanie i konfiguracja kluczy API / endpointów
opencode auth login

# Uruchomienie w projekcie
opencode
```

---

## 3. Integracja z Modelami Lokalnymi (0 Tokenów API)

OpenCode pozwala na skonfigurowanie lokalnego backendu kompatybilnego z OpenAI API (np. Ollama działająca na WSL). Poniższy JSON to przykład ⚠️ niezweryfikowane — właściwy schemat sprawdź w dokumentacji OpenCode:

```json
{
  "provider": "ollama",
  "endpoint": "http://localhost:11434/v1",
  "models": {
    "plan": "deepseek-r1:7b",
    "build": "qwen2.5-coder:14b"
  }
}
```

Dzięki temu możesz prowadzić całą fazę planowania i generowania kodu **w 100% lokalnie i bezpłatnie**, nie zużywając limitów tokenów API.

---

## 4. Konfiguracja pod Tokensavemaxxing

1. **Praca w trybie `plan` przed `build`**:
   - Przełącz się w tryb `plan`, aby agent przeanalizował zależności bez ryzyka zepsucia plików.
   - W trybie `plan` odczyty są ograniczone i nakierowane na diagnostykę architektoniczną.
2. **Plik `.opencodeignore`**:
   - Skonfiguruj wykluczenia dla buildów, lockfile'ów i folderów generowanych, aby nie obciążać okna kontekstowego agenta.

---

## 5. Kiedy Używać
- Praca w terminalu z możliwością płynnego przełączania się między modelami chmurowymi a lokalnym Qwenem w Ollamie.
- Projekty o ścisłych wymaganiach prywatności (przełączenie w całości na silnik lokalny).
- Zautomatyzowane pipeline'y w GitHub Actions (`opencode github run`).
