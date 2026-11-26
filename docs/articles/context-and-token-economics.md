---
title: "Ekonomia Tokenów, Prompt Cache i Cięcie Narzędzi"
description: "Skąd biorą się koszty długich sesji agentowych: dynamiczne ładowanie narzędzi, prompt cache i kompresja kontekstu."
---

Synteza dwóch źródeł: [Cursor: Improved token efficiency](https://cursor.com/blog/improved-token-efficiency) (23.09.2026) oraz pracy o bramce kompresującej Paritok ([arXiv:2609.22114](https://arxiv.org/html/2609.22114)). To różne systemy i różne pomiary.

---

## 1. Skąd bierze się koszt

W pętli agentowej historia, odczytane pliki i definicje narzędzi są wysyłane ponownie w kolejnych turach. Plik odczytany raz kosztuje więc wielokrotnie, choć dzięki prompt cache powtórzony prefiks jest zwykle znacznie tańszy. Według pracy o Paritok o rachunku decyduje suma po wszystkich turach i ceny cache.

| Mechanizm | Na co działa |
|---|---|
| Ładowanie narzędzi na żądanie | Stały narzut definicji narzędzi |
| Wykluczenia indeksu (`.cursorignore`) | To, co może trafić do wyszukiwania; efektu tutaj nie zmierzono |
| Pasywna mapa repozytorium | Może zmniejszyć liczbę odczytów; efektu tutaj nie zmierzono |
| Stabilny prefiks promptu | Cenę ponownie wysyłanego kontekstu |
| Kompresja wcześniejszych odczytów | Ilość ponownie wysyłanej historii |

---

## 2. Pomiary Cursora

### A. Narzędzia MCP ładowane na żądanie
Przeniesienie narzędzi MCP do **dynamicznego kontekstu** (model dostaje definicję dopiero wtedy, gdy jej potrzebuje) zmniejszyło o **46,9% łączną liczbę tokenów w sesjach, które wywołały narzędzie MCP**.

Ważne: to **nie jest pomiar wyłączenia nieużywanych serwerów MCP** i nie dotyczy wszystkich sesji. Szersze omówienie mechanizmu: [Dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery). Wyłączenie zbędnego serwera nadal ma sens, ale tej liczby nie można mu przypisać.

### B. Stabilność prefiksu
Prompt cache dopasowuje prefiks, więc zmiana na początku promptu (np. aktualny czas przed regułami) unieważnia dalszą część. Cursor ujmuje to tak: punkty cache pomagają tylko wtedy, gdy sam prefiks pozostaje stabilny.

Praktyczny wniosek (autorski): `[stałe reguły i narzędzia] → [mapa repo] → [historia] → [nowe zapytanie]`.

### C. Numeracja linii
Numerowanie co dziesiątej linii zamiast każdej zmniejszyło **liczbę tokenów odczytywanych z cache o 1,6%, bez spadku jakości**. Źródło nie twierdzi, że usuwa to błędy lokalizacji edycji.

---

## 3. Kompresja zawartości (Paritok, [arXiv:2609.22114](https://arxiv.org/html/2609.22114))

*An Empirical Cost Attribution of Context-Compression Gateways in Multi-Turn Coding Agents* rozdziela trzy dźwignie w sesjach Claude Code i Codex:

- **Filtrowanie schematów narzędzi** było największą i jedyną jednoznacznie powtarzalną dźwignią; na typowej turze usuwało około 21–57 tys. tokenów.
- **Kompresja odczytanych plików i wyników narzędzi** oszczędzała tylko około **2% prefiksu (rozliczanego w cenie cache) na turę**.
- Ponieważ skompresowana treść jest wysyłana w każdej następnej turze, suma oszczędności rośnie w przybliżeniu **kwadratowo** i w ich pomiarze **około 6. tury** przewyższała stały zysk z filtrowania narzędzi, do granicy narzuconej przez okno kontekstu.
- Gdy agent odzyskuje oryginał, część oszczędności przepada.
- Autorzy zwracają uwagę, że to samo zadanie trwało od 7 do 18 tur, a ta wariancja przesłania efekt rzędu 2%.

To wyniki jednej bramki w opisanej konfiguracji, nie stałe właściwości każdej kompresji.

---

## 4. Działania (zalecenia autorskie)

1. Używaj ładowania narzędzi na żądanie, jeśli harness je obsługuje, i wyłączaj serwery MCP zbędne w danym projekcie. Nie zmieniaj zestawu narzędzi bez potrzeby w trakcie sesji, bo może to unieważnić cache.
2. Nie wczytuj lockfile'ów w całości; wyszukuj w nich konkretny wpis.
3. Duże pliki czytaj zakresami (próg 300 linii to konwencja tego repozytorium).
4. Efekt mierz na własnych zadaniach: liczba tur, tokeny z podziałem na cache oraz wynik testów.

## Źródła

- [Cursor: Improved token efficiency](https://cursor.com/blog/improved-token-efficiency)
- [Cursor: Dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery)
- [arXiv:2609.22114 (Paritok)](https://arxiv.org/html/2609.22114)
