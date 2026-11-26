---
title: "FinOps i Benchmarki Tokenowe w Programowaniu Agentowym"
description: "Zestawienie publikacji o kosztach tokenowych agentów: co mierzono, na czym i czego z tego nie wolno uogólniać."
---

Zestawienie publikacji o kosztach tokenowych agentów. Przy każdej liczbie podano, gdzie ją znaleziono. Liczby pochodzą z różnych zadań, modeli i metryk, więc **nie wolno ich sumować ani porównywać wprost**.

---

## 1. Gdzie uciekają tokeny (przykład ChatDev)

[Glean](https://www.glean.com/perspectives/how-to-optimize-token-efficiency-in-agentic-systems) omawia badanie z Concordia University: 30 zadań w wieloagentowym systemie ChatDev. Ta sama praca jest w [katalogu Bruniaux](https://cc.bruniaux.com/token-savings) jako arXiv:2601.14470 (model GPT-5).

| Pomiar | Wynik |
|---|---|
| Udział etapu code review w zużyciu tokenów | **59,4%** |
| Udział tokenów wejściowych | **53,9%** |

To wynik dla jednego systemu wieloagentowego. Nie opisuje typowej sesji z jednym agentem w IDE.

---

## 2. Katalog narzędzi Floriana Bruniaux

[Token-saving tools for coding agents](https://cc.bruniaux.com/token-savings) (stan na 30.09.2026) zestawia deklaracje 43 narzędzi z 8 publicznymi benchmarkami i 15 preprintami. Autor zaznacza, że współtworzył RTK.

- **RTK:** w prywatnych miesięcznych raportach autora (lipiec–wrzesień 2026) zaoszczędzone było **48–81% tokenów wyjścia CLI**. Autor zastrzega, że to **nie jest procent całego rachunku**.
- **Pruning a prompt cache:** przytoczone w katalogu README jednego z narzędzi do pruningu ostrzega, że zmiana wcześniejszych wiadomości unieważnia zapisany prefiks i może zwiększyć liczbę *cache miss*.
- Każde narzędzie ma w katalogu inną metrykę (tokeny, koszt, własny licznik). Przed użyciem liczby sprawdź, co dokładnie mierzono.

---

## 3. Przewodnik Idy Silfverskiold i prompt caching

[Agentic AI: How to Save on Tokens](https://towardsdatascience.com/agentic-ai-how-to-save-on-tokens) (Towards Data Science, kwiecień 2026) omawia m.in.:

1. **Prompt caching:** statyczna część promptu na początku. Według artykułu dostawcy usuwają cache zwykle po **około 5–10 minutach** bezczynności (u części można ten czas wydłużyć).
2. **Lazy-loading** narzędzi i serwerów MCP.
3. **Routing i kaskady:** najpierw tańszy model, eskalacja przy niskiej pewności.
4. **Subagentów i kompakcję**, czyli utrzymywanie czystego kontekstu.

Spotykana liczba **41–80% niższych kosztów API dzięki cache** pochodzi z innej pracy: *Don't Break the Cache: Prompt Caching for Long-Horizon Agentic Tasks*, przytoczonej w [katalogu Bruniaux](https://cc.bruniaux.com/token-savings).

---

## 4. LOOP Skill Engine: deterministyczny replay

[From Prototype to Profit](https://towardsdatascience.com/from-prototype-to-profit-solving-the-agentic-token-burn-problem) (Rahul Vir) opisuje za pracą o LOOP Skill Engine nagrywanie udanego przebiegu i odtwarzanie go bez LLM.

- Podawane oszczędności to **ponad 93,3% dla zadań codziennych i do 99,98% dla bardzo częstych**.
- Dotyczy to **powtarzalnych, ustalonych przepływów** (w artykule m.in. procesy w przychodni). Nie jest to pomiar pracy programistycznej, a samej pracy źródłowej tutaj nie weryfikowano.

---

## 5. Qt: porady dla środowisk enterprise

[Artykuł Qt](https://www.qt.io/software-insights/how-to-reduce-ai-token-usage-in-enterprise-agentic-development-workflows) (tekst producenta, opisujący także własne narzędzia) zaleca:

- dostęp do dokumentacji przez MCP zwracający wycinki zamiast całych stron HTML,
- **deterministyczne narzędzia przed inferencją**, np. linter uruchamiany przed code review przez agenta,
- skille domenowe. W benchmarku QML100 skill Qt podniósł skuteczność jednego modelu z 64% do 75%.

---

## Usunięte twierdzenia

Wcześniejsza wersja podawała też: przedziały 53,9–92% i 15–35% dla struktury kosztów, spadek `read_file` o 75% przy 95%+ skuteczności dzięki repo-mapom, eliminację 80% tur naprawczych przez linter oraz „analizę 87 000 wywołań”. **Nie znaleziono ich w sprawdzonych źródłach**, więc zostały usunięte.

## Źródła

- [Glean: How to optimize token efficiency in agentic systems](https://www.glean.com/perspectives/how-to-optimize-token-efficiency-in-agentic-systems)
- [Florian Bruniaux: Token-saving tools for coding agents](https://cc.bruniaux.com/token-savings)
- [Ida Silfverskiold: Agentic AI: How to Save on Tokens](https://towardsdatascience.com/agentic-ai-how-to-save-on-tokens)
- [Rahul Vir: From Prototype to Profit](https://towardsdatascience.com/from-prototype-to-profit-solving-the-agentic-token-burn-problem)
- [Qt: How to reduce AI token usage in enterprise workflows](https://www.qt.io/software-insights/how-to-reduce-ai-token-usage-in-enterprise-agentic-development-workflows)
