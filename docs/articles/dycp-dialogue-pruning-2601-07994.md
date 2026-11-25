---
title: "DYCP: Dynamiczny Pruning Dialogów z Algorytmem Kadane'a (arXiv:2601.07994)"
description: "DYCP: Dynamiczny Pruning Dialogów z Algorytmem Kadane'a (arXiv:2601.07994)"
---


# DYCP: Dynamiczny Pruning Dialogów z Algorytmem Kadane'a (arXiv:2601.07994)

Analiza techniczna publikacji naukowej:
**"DYCP: Dynamic Context Pruning for Long-Form Dialogue with LLMs"**
*Autorzy*: Nayoung Choi, Jonathan Zhang, Jinho D. Choi (Emory University, 2026).
*Źródło*: [arXiv:2601.07994](https://arxiv.org/abs/2601.07994)

---

## 1. Problem: Długie Dialogi Programistyczne i Utrata Spójności

W długich sesjach dialogowych (np. wieloetapowe debugowanie skomplikowanego systemu):
- Historia rozmowy rozrasta się do kilkunastu lub kilkudziesięciu tur.
- Standardowe podejścia (np. usuwanie najstarszych tur lub ślepa kompresja co N kroków) **niszczą spójność wątku**: wycinają kluczowe ustalenia architektoniczne lub rozrywają logiczny ciąg przyczynowo-skutkowy.
- Wcześniejsze metody segmentacji wymagały kosztownych dodatkowych wywołań LLM (np. "podsumuj ten fragment"), co generowało opóźnienia i dodatkowe koszty.

---

## 2. Kluczowa Innowacja DYCP: Algorytm *KadaneDial*

Naukowcy z Emory University zaproponowali metodę **DYCP (Dynamic Context Pruning)** działającą bezpośrednio w czasie zapytania (**Query-Time**, bez dodatkowych wywołań LLM):

```
Tura 1 (Inicjalizacja) [Relevance: +0.2]
Tura 2 (Dyskusja o CSS) [Relevance: -0.8]  ◄── WYCIĘTE (Pruned)
Tura 3 (Dyskusja o CSS) [Relevance: -0.6]  ◄── WYCIĘTE (Pruned)
Tura 4 (Konfiguracja DB) [Relevance: +0.9] ◄── ZACHOWANE (Ciągły span)
Tura 5 (Błąd w SQL)     [Relevance: +1.2] ◄── ZACHOWANE (Ciągły span)
Tura 6 (Nowy prompt usera o SQL)
```

### Jak Działa *KadaneDial*?
1. **Scoring Istotności w Czasie Rzeczywistym**:
   Lekki enkoder lub wbudowane prawdopodobieństwa oceniają relację semantyczną między bieżącym zapytaniem użytkownika a poszczególnymi turami z historii.
2. **Problem Maksymalnej Podtablicy (Maximum Subarray Problem)**:
   Zamiast wybierać losowe, pojedyncze tury (co stworzyłoby poszarpany, niezrozumiały dla LLM dialog), DYCP stosuje adaptację **algorytmu Kadane'a** (*KadaneDial*).
3. **Wykrywanie Ciągłych Spójnych Bloków (Sustained Relevance)**:
   Algorytm lokalizuje **ciągłe, spójne przedziały tur**, w których poziom istotności dla bieżącego problemu utrzymuje się na wysokim poziomie.
4. **Pruning Dygresji**:
   Wszelkie wtrącenia poboczne (np. 5 tur dyskusji o stylach CSS w trakcie debugowania bazy danych) są bezlitośnie odcinane.

---

## 3. Wyniki Benchmarków

- **Zachowanie Spójności Logicznej**: DYCP osiąga wyższy wskaźnik poprawności odpowiedzi niż naiwne obcinanie historii (FIFO) oraz modele RAG bazujące na pojedynczych turach.
- **Zerowy Narzut Opóźnienia**: Algorytm Kadane'a działa w złożoności liniowej $\mathcal{O}(N)$ w ułamku milisekundy — nie wymaga generowania tekstu przez zewnętrzny model.
- **Drastyczna Oszczędność Tokenów**: W długich sesjach eliminuje 40% do 70% historii, zapobiegając dryfowi uwagi modelu.

---

## 4. Wnioski dla Inżynierii tokensavemaxxing

1. **Kontekst to graf ciągłych zdarzeń, a nie zbiór luźnych zdań**: Przy kompresji historii nie wolno wycinać pojedynczych zdań w losowych miejscach. Należy zachowywać spójne bloki dialogowe.
2. **Determinizm algorytmiczny bije LLM**: Użycie klasycznego algorytmu programowania dynamicznego (Kadane) do zarządzania kontekstem jest tańsze, szybsze i bardziej przewidywalne niż zatrudnianie kolejnego modelu AI do "streszczania historii".
