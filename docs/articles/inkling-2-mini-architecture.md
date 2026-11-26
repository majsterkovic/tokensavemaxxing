---
title: "Analiza Architektury: Inkling 2 Mini (Thinking Machines Lab)"
description: "Inkling 2 Mini jako transformer z pętlą: parametry, pamięć i wyniki według ogłoszenia producenta."
---

Opracowanie ogłoszenia [Introducing Inkling 2 Mini](https://thinkingmachines.ai/news/inkling-2-mini) (Thinking Machines Lab, 20.11.2026). Wszystkie liczby pochodzą **od producenta**. To strona o modelu lokalnym; sama nie dowodzi oszczędności tokenów.

---

## 1. Architektura „looped transformer”

Model typu Mixture-of-Experts, którego środkowe bloki wykonują się **trzy razy dla każdego tokenu**.

```
Prelude (1×) → bloki 2 i 3 (3×, te same wagi) → blok końcowy (1×)
```

- Przejścia 2 i 3 otrzymują dodatkowo wyniki poprzedniego przejścia („message”); każde przejście dostaje wyjście prelude.
- **24 zapisane warstwy dają 48 zastosowań warstw na token.**

| Parametr | Wartość |
|---|---|
| Parametry łącznie | 26,4 mld |
| Parametry aktywne | 3,4 mld |
| Aktywacje wag na token (z uwzględnieniem pętli) | 5,4 mld |
| Łączne zużycie pamięci (NVFP4, ostatnie cztery warstwy MXFP8) | ok. 20 GB |

---

## 2. Dostępność i wyniki

- Model ma **otwarte wagi**, dostępne na Hugging Face.
- Inferencja według ogłoszenia: SGLang, vLLM, Ollama, Unsloth, NVIDIA Dynamo, TokenSpeed i Llama App. Skwantyzowane GGUF są dostępne przez Unsloth i llama.cpp.
- Producent mówi o uruchamianiu na laptopach i stacjach typu DGX Spark.
- W benchmarkach agentowego kodowania (np. DeepSWE v1.1: 48,2%) producent stawia model przed porównywalnymi modelami; w niektórych innych ustępuje tylko Qwen3.8-27B. Konfiguracje ewaluacji różnią się między modelami.

---

## 3. Czego ogłoszenie nie potwierdza

Wcześniejsza wersja podawała okno 1M tokenów, licencję Apache 2.0, informacje o założycielce firmy, płynne działanie na 12 GB VRAM, obsługę MLX i podział na numerowane warstwy. **Na tej stronie ich nie znaleziono**, więc zostały usunięte. Przy ~20 GB zużycia pamięci działanie na 12 GB VRAM wymagałoby innej kwantyzacji lub przeniesienia części modelu do RAM; sprawdź to na własnym sprzęcie. Licencję sprawdź na karcie modelu.

## Źródła

- [Thinking Machines Lab: Introducing Inkling 2 Mini](https://thinkingmachines.ai/news/inkling-2-mini)
