---
title: "Dynamic Context Pruning (DCP): Praca arXiv:2305.15805"
description: "Uczona selekcja tokenów wewnątrz transformera: co pokazuje praca i dlaczego nie opisuje narzędzi agentowych."
---

**"Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers"**
*Autorzy:* Sotiris Anagnostidis, Dario Pavllo, Luca Biggio, Lorenzo Noci, Aurélien Lucchi, Thomas Hofmann.
*Źródło:* [arXiv:2305.15805](https://arxiv.org/abs/2305.15805)

---

## 1. Problem

W autoregresyjnym transformerze KV-cache rośnie wraz z długością sekwencji i obciąża pamięć oraz obliczenia podczas generowania.

---

## 2. Wyniki z pracy

Autorzy raportują, że ich model może odrzucać **do 80% kontekstu bez istotnego pogorszenia wyników w zadaniach downstream**, uzyskując **do 2× większą przepustowość** inferencji. To górne wartości z ich eksperymentów, nie gwarancja dla dowolnego modelu.

---

## 3. Metoda

- Do każdej warstwy dodany jest **uczony mechanizm bramkujący (α-sigmoid)**, który decyduje, które tokeny pominąć. Działa razem ze **zwykłym softmaxem**.
- Wymaga to **dostrojenia modelu** (w pracy m.in. modeli klasy GPT-2) i dostępu do jego wnętrza.
- Tokeny odrzucone w warstwie nie biorą udziału w dalszych obliczeniach uwagi.
- Wybory bramki można analizować, co daje częściową interpretowalność.

---

## 4. Czego z tej pracy nie wolno wnioskować

Narzędzia po stronie aplikacji (np. [opencode-dynamic-context-pruning](https://github.com/Tarquinen/opencode-dynamic-context-pruning), hak [Spotify `shunt`](/tokensavemaxxing/articles/spotify-shunt-and-portal/), RTK) skracają **tekst wysyłany do modelu przez API**. DCP z tej pracy działa **wewnątrz wytrenowanego modelu**. To różne techniki ze zbliżoną nazwą lub celem. Praca **nie mierzy ich skuteczności**, kosztów API ani zadań agentowych.

## Źródła

- [arXiv:2305.15805](https://arxiv.org/abs/2305.15805)
