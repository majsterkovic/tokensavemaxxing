# Dynamic Context Pruning (DCP): Fundament Teoretyczny (arXiv:2305.15805)

Szczegółowa analiza przełomowej pracy naukowej:
**"Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers"**
*Autorzy*: Sotiris Anagnostidis, Dario Pavllo, Luca Biggio, Lorenzo Noci, Aurélien Lucchi, Thomas Hofmann (ETH Zürich, CSEM, University of Basel / NeurIPS).
*Źródło*: [arXiv:2305.15805](https://arxiv.org/abs/2305.15805)

---

## 1. Wstęp: Problem Kwadratowego Narzutu Pamięci (KV-Cache Bloat)

W modelach autoregresyjnych (dekoderach typu Transformer) uwaga (self-attention) standardowo liczy relacje między każdą parą tokenów w sekwencji. Rodzi to dwa wąskie gardła:
1. **Złożoność obliczeniowa $\mathcal{O}(N^2)$** względem długości sekwencji $N$.
2. **Pamięć podręczna kluczy i wartości (KV-Cache)**: Wraz ze wzrostem długości czatu rozmiar KV-cache rośnie liniowo, zjadając pamięć VRAM GPU i drastycznie spowalniając generowanie każdego kolejnego tokenu (memory-bound inference).

W programowaniu agentowym, gdzie sesje mają po kilkadziesiąt tysięcy tokenów historii, większość tego kontekstu to martwy balast.

---

## 2. Główna Teza i Wyniki Pracy

Badacze z ETH Zürich udowodnili, że:
> **Aż do 80% tokenów kontekstu w oknie modelu można dynamicznie odrzucić (prune) w trakcie generowania bez mierzalnego spadku jakości (perplexity) czy skuteczności w zadaniach downstream.**

### Kluczowe Wyniki Liczbowe:
- **Redukcja tokenów**: Usunięcie do **80% nieistotnych tokenów** z aktywnego kontekstu.
- **Przepustowość (Throughput)**: Wzrost szybkości generowania do **2×**.
- **Czas wykonania (Wall-time Latency)**: Skrócenie czasu oczekiwania na odpowiedź nawet o **50%** w długich sekwencjach.
- **Interpretowalność**: Praca pozwala dokładnie zobaczyć, które tokeny model uznał za nieistotne na poziomie poszczególnych warstw.

---

## 3. Metodologia: Adaptacyjnie Rzadka Uwaga (Adaptively Sparse Attention)

Tradycyjna funkcja `softmax` w mechanizmie uwagi nigdy nie przypisuje dokładnego zera — każdy token, nawet najbardziej bezużyteczny, otrzymuje znikomą wagę probabilistyczną (np. 0.00001). To zmusza model do trzymania go w pamięci KV-cache.

### Rozwiązanie Autorów:
1. **Funkcje rzadkiej aktywacji (np. `entmax`)**:
   Zastąpienie `softmax` funkcjami aktywacji, które potrafią przypisać **dokładne matematyczne zero** wagom uwagi.
2. **Uczący się mechanizm odrzucania (Learnable Token Dropping)**:
   Dodanie minimalnej liczby uczonych parametrów, które na poziomie poszczególnych warstw oceniają informatywność tokenów.
3. **Fizyczne usunięcie z KV-Cache**:
   Gdy waga uwagi tokenu spada do zera na danym etapie, token jest fizycznie usuwany z pamięci podręcznej KV. Kolejne kroki generowania nie wykonują już na nim mnożenia macierzy.

---

## 4. Most Między Teorią z ETH a Praktyką Programowania Agentowego

Praca Anagnostidisa i zespołu z ETH Zürich to fundament teoretyczny, który wyjaśnia, dlaczego współczesne narzędzia inżynierii kontekstu działają tak skutecznie. 

Zjawisko to obserwujemy na dwóch poziomach:

```
┌────────────────────────────────────────────────────────────────────────┐
│  POZIOM 1: Architektura Silnika LLM (Praca ETH Zürich arXiv:2305.15805) │
│  - Usuwanie wektorów z KV-Cache wewnątrz GPU                           │
│  - Rzadka uwaga (entmax), redukcja O(N²) w warstwach uwagi             │
├────────────────────────────────────────────────────────────────────────┤
│  POZIOM 2: Warstwa Aplikacyjna Agenta (Narzędzia tokensavemaxxing)     │
│  - @tarquinen/opencode-dcp: Zastępowanie powtórzeń placeholderami      │
│  - Spotify shunt: Hak PreToolUse blokujący duże read_file              │
│  - RTK: Kompresja wyjść terminala przed wysłaniem do API               │
│  - Context Mode: Przechowywanie danych w SQLite FTS5 zamiast w oknie   │
└────────────────────────────────────────────────────────────────────────┘
```

Oba poziomy opierają się na tej samej prawdzie empirycznej: **Większość tokenów w długiej sesji programistycznej wnosi dokładnie zero informacji decyzyjnej.** 

Pozostawienie ich w oknie nie tylko kosztuje realne pieniądze w API, ale wręcz pogarsza zdolność modelu do skupienia uwagi na krytycznych regułach architektury.
