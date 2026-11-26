---
title: "DYCP: Dynamiczny Pruning Dialogów z Algorytmem Kadane'a (arXiv:2601.07994)"
description: "KadaneDial: wybór ciągłych fragmentów historii dialogu w czasie zapytania."
---

**"DYCP: Dynamic Context Pruning for Long-Form Dialogue with LLMs"**
*Autorzy:* Nayoung Choi, Jonathan Zhang, Jinho D. Choi (Emory University).
*Źródło:* [arXiv:2601.07994](https://arxiv.org/abs/2601.07994)

---

## 1. Problem

Długa historia dialogu kosztuje i może rozpraszać model, a usuwanie najstarszych tur albo wybieranie pojedynczych wypowiedzi może rozerwać wątek.

---

## 2. Metoda: *KadaneDial*

```
Tura 1  [istotność niska]
Tura 2  [niska]   ← pominięta
Tura 3  [niska]   ← pominięta
Tura 4  [wysoka]  ← zachowany ciągły fragment
Tura 5  [wysoka]  ← zachowany ciągły fragment
Nowe pytanie
```
(schemat ilustracyjny)

1. Enkoder wyszukiwawczy (bi-encoder, w pracy **Contriever**) ocenia istotność tur względem bieżącego zapytania.
2. Adaptacja **algorytmu Kadane'a** (problem maksymalnej podtablicy) wybiera **ciągłe fragmenty** o wysokiej istotności.
3. Selekcja działa w czasie zapytania i nie wymaga streszczania historii przez dodatkowe wywołania LLM. Enkoder i obliczenie ocen nadal mają swój koszt.

---

## 3. Wyniki

Autorzy raportują zachowanie jakości odpowiedzi przy znacznie krótszym wejściu na swoich benchmarkach dialogowych. Dokładne wartości zależą od modelu i zbioru, dlatego sprawdź je w tabelach pracy. Wcześniej podany przedział „40–70%” **nie został w niej znaleziony** i został usunięty.

---

## 4. Wnioski dla tokensavemaxxing (autorskie)

1. Przy przycinaniu historii warto zachowywać spójne bloki, a nie losowe zdania.
2. Prosta selekcja algorytmiczna może być alternatywą dla streszczania przez LLM. Praca dotyczy dialogów, więc **nie mierzy sesji agentów programistycznych** i nie pokazuje, że determinizm zawsze wygrywa z LLM.

## Źródła

- [arXiv:2601.07994](https://arxiv.org/abs/2601.07994)
