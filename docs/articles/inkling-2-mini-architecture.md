---
title: "Analiza Architektury: Inkling 2 Mini (Thinking Machines Lab)"
description: "Analiza Architektury: Inkling 2 Mini (Thinking Machines Lab)"
---

Analiza techniczna przełomowego modelu otwartego **Inkling 2 Mini**, wydanego 20 listopada 2026 r. przez laboratorium **Thinking Machines Lab** (założone przez byłą CTO OpenAI, Mirę Murati).

---

## 1. Dlaczego Inkling 2 Mini to Przełom dla Modeli Lokalnych?

Do tej pory modele lokalne zmuszały do kompromisu:
- Albo mały model 7B/8B (mieszczący się w VRAM, ale o ograniczonej głębokości rozumowania),
- Albo potężny model 70B+ (wymagający klastra GPU za dziesiątki tysięcy dolarów).

**Inkling 2 Mini** rozwiązuje ten problem dzięki nowatorskiej architekturze **Looped Mixture-of-Experts (MoE)** pod licencją **Apache 2.0**.

---

## 2. Architektura "Looped Transformer" — Pętla Myślenia bez Rozrostu Wag

```
Wejście (Prompt)
       │
       ▼
┌───────────────────────────────────────────┐
│  Prelude: Warstwy 0 – 5 (1 przejście)     │  Wstępna ekstrakcja cech
└──────────────────────┬────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────┐ ◄──┐
│  Middle MoE: Warstwy 6 – 17               │    │  PĘTLA 3-KROTNA
│  Współdzielone wagi (Shared Weights)      │    │  (3 iterations)
│  Aktywacja: ~3.4B wag per token           │    │  48 logicznych warstw
└──────────────────────┬────────────────────┘ ───┘
                       │
                       ▼
┌───────────────────────────────────────────┐
│  Postlude: Warstwy 18 – 23 (1 przejście)  │  Finalna projekcja tokenu
└──────────────────────┬────────────────────┘
                       │
                       ▼
Wyjście (Odpowiedź)
```

### Parametry Modelu:
- **Całkowita liczba parametrów**: ~26.4 miliarda (26.4B).
- **Aktywne parametry na token**: zaledwie **~3.4B** unikalnych wag (~5.4B efektywnych parametrów przy pętli).
- **24 fizyczne warstwy dekodera**:
  - Warstwy 0–5 (preludium) wykonują się 1 raz.
  - Warstwy 18–23 (postludium) wykonują się 1 raz.
  - **12 warstw środkowych (6–17) wykonuje się 3-krotnie w pętli** z użyciem tych samych wag.
- **Efekt**: Model wykonuje **48 logicznych przejść warstwowych per token**, co daje mu głębię rozumowania odpowiadającą modelom o wielokrotnie większej liczbie fizycznych wag, przy zachowaniu minimalnego narzutu pamięciowego!

---

## 3. Zdolności i Zastosowanie Deweloperskie

1. **Okno kontekstowe do 1 miliona tokenów (1M Context)**:
   Niezwykle rzadka cecha wśród modeli otwartych zoptymalizowanych pod lokalny sprzęt.
2. **Natywna multimodalność**:
   Przyjmuje na wejściu zarówno tekst, jak i obrazy (zrzuty ekranu UI, diagramy architektoniczne).
3. **Wydajność w zadaniach agentowych (DeepSWE / Tool-use)**:
   W testach inżynierii oprogramowania i benchmarkach Artificial Analysis model dorównuje modelom stacjonarnym klasy Qwen 3.8 27B, zużywając ułamek zasobów obliczeniowych.

---

## 4. Inkling 2 Mini na Sprzęcie z 12 GB VRAM

Dystrybuowany jest w formacie ~20 GB (wagi w formatach NVFP4 / MXFP8).
- **Wsparcie Day-Zero**: Dostępny od pierwszego dnia w `llama.cpp`, vLLM, SGLang oraz MLX (`thinkingmachines/Inkling-2-Mini`).
- **Praca na 12 GB VRAM**:
  - Ponieważ aktywnych jest tylko ~3.4B parametrów, w kwantyzacji 4-bitowej (GGUF / NVFP4) z częściowym offloadingiem do RAM komputera model działa płynnie na domowych stacjach roboczych.
  - Stanowi doskonałą alternatywę dla standardowych modeli gęstych (dense 7B/14B) jako lokalny mózg agentowy.
