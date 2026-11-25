---
title: "Notatka Narzędziowa: Modele Lokalne w Środowisku 12 GB VRAM"
description: "Notatka Narzędziowa: Modele Lokalne w Środowisku 12 GB VRAM"
---

> **Rola w ekosystemie**: Zerowy koszt tokenowy (0 zł / 0 limitów API). Idealna warstwa do wstępnego planowania ("Thinking Mini"), generowania testów jednostkowych, lokalnego formatowania oraz asystowania w OpenCode.

---

## 1. Ograniczenia i Potencjał Sprzętowy 12 GB VRAM

Karta graficzna z 12 GB VRAM (np. RTX 3060 12GB lub RTX 4070 12GB) to idealny punkt wejścia do lokalnej inżynierii AI:
- Zapewnia wystarczającą pamięć dla modeli do **14 miliardów parametrów (14B)** w kwantyzacji 4-bitowej (`Q4_K_M`).
- Zapewnia pełną przepustowość dla modeli **7B/8B** w wysokiej kwantyzacji (`Q8_0` lub `Q5_K_M`), generując 40–80 tokenów na sekundę.

---

## 2. Zestawienie Rekomendowanych Modeli dla 12 GB VRAM

| Model | Rozmiar / Kwantyzacja | Użycie VRAM | Główna rola w Tokensavemaxxing |
|---|---|---|---|
| **Inkling 2 Mini** (Thinking Machines) | Looped MoE (26.4B tot / 3.4B act, NVFP4/Q4) | ~9–11 GB (GGUF/offload) | **Przełomowy Looped MoE**: 48 przejść logicznych, multimodalny, 1M kontekstu. Głębokie rozumowanie bez rozmiaru 70B! Szczegóły: [Architektura Inkling 2 Mini](/tokensavemaxxing/articles/inkling-2-mini-architecture/) |
| **DeepSeek-R1-Distill-Qwen-7B** | `Q5_K_M` lub `Q6_K` | ~7.2 GB | **"Thinking Mini"**: Lokalne rozumowanie, analiza edge-case'ów, planowanie kroków przed wysłaniem do API |
| **Qwen 2.5 Coder 14B** | `Q4_K_M` | ~9.8 GB | **Lokalny Programista**: Najsilniejszy model 14B na rynku, rozumie TypeScript/Python, generuje złożone funkcje |
| **Qwen 2.5 Coder 7B** | `Q8_0` | ~8.4 GB | **Błyskawiczny Asystent**: Niezwykle szybki, bezbłędny w prostych funkcjach i testach jednostkowych |
| **Phi-4 (14B)** | `Q4_K_M` | ~10.1 GB | **Logika Matematyczna**: Świetny w precyzyjnych kalkulacjach i weryfikacji algorytmów |
| **SmolLM2 1.7B / Qwen 1.5B** | `FP16` / `Q8_0` | ~2.5 GB | **Lokalny Triage**: Błyskawiczny routing, klasyfikacja plików i tagowanie bez obciążania GPU |

---

## 3. Konfiguracja Serwera: Ollama na WSL

Najprostszym i najbardziej wydajnym sposobem serwowania modeli na WSL jest Ollama:

```bash
# Instalacja Ollama w WSL
curl -fsSL https://ollama.com/install.sh | sh

# Uruchomienie modelu rozumującego DeepSeek R1 7B
ollama run deepseek-r1:7b

# Uruchomienie wyspecjalizowanego kodera Qwen 2.5 Coder 14B
ollama run qwen2.5-coder:14b-instruct-q4_K_M

# Sprawdzenie zużycia VRAM
nvidia-smi
```

---

## 4. Połączenie z OpenCode

Ollama udostępnia endpoint kompatybilny z OpenAI API pod adresem:
`http://localhost:11434/v1`

W konfiguracji OpenCode (`~/.config/opencode/config.json`):
```json
{
  "provider": "ollama",
  "endpoint": "http://localhost:11434/v1",
  "model": "qwen2.5-coder:14b"
}
```
Możesz pisać kod w terminalu OpenCode z zerowym zużyciem tokenów chmurowych!

---

## 5. Zastosowanie w Metodologii Tokensavemaxxing

1. **Faza 0 (Planowanie bez opłat)**:
   Zamiast płacić za 5 tur planowania w Claude 3.7 Sonnet, puszczasz brief przez lokalny `DeepSeek-R1-Distill-Qwen-7B`. Model myśli lokalnie, generuje precyzyjny 4-punktowy plan.
2. **Generowanie Danych Testowych i Mocków**:
   Tworzenie 50 rekordów testowych lub mocków API nie wymaga modelu za $20/miesiąc — lokalny `Qwen 7B` zrobi to w 3 sekundy.
3. **Prywatność Danych Wrażliwych**:
   Logi produkcyjne z tokenami sesji, kluczami czy danymi osobowymi możesz analizować wyłącznie lokalnie, nie ryzykując wycieku do chmury.
