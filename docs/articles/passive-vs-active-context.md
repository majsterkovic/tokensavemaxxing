---
title: "Pasywny Kontekst vs Skille (Ewaluacja Vercel)"
description: "Ewaluacja Vercel: indeks dokumentacji Next.js w AGENTS.md kontra skill ładowany na żądanie."
---

Analiza wpisu Vercel [AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) (styczeń 2026). Dyskusja: [Hacker News #46809708](https://news.ycombinator.com/item?id=46809708).

---

## 1. Konstrukcja ewaluacji

Zadania wymagały znajomości nowych API Next.js 16, których model mógł nie znać z treningu. Porównano cztery konfiguracje:

1. **Baseline:** bez dodatkowej dokumentacji.
2. **Skill:** agent sam decyduje, czy go uruchomić.
3. **Skill + jawna instrukcja** w `AGENTS.md`, żeby go używać.
4. **Skompresowany indeks dokumentacji w `AGENTS.md`** (z około 40 KB do 8 KB).

---

## 2. Wyniki

| Konfiguracja | Pass rate | Względem baseline |
|---|---|---|
| Baseline | 53% | — |
| Skill (decyzja agenta) | 53% | +0 pp |
| Skill + jawna instrukcja | 79% | +26 pp |
| Indeks dokumentacji w `AGENTS.md` | **100%** | +47 pp |

- W konfiguracji ze skillem bez instrukcji **w 56% przypadków skill nie został w ogóle użyty**.
- Z jawną instrukcją skill uruchamiał się w **ponad 95%** przypadków.
- W części testów nieużywany skill wypadł gorzej niż baseline (**58% vs 63%**).

---

## 3. Czego ten wynik nie dowodzi

- Indeks wskazywał **pliki dokumentacji Next.js**. **Nie była to mapa kodu** ani mapa eksportów. Wynik nie dowodzi, że `REPO-MAP.md` z tego repozytorium daje 100%.
- Wpis nie podaje liczby przypadków testowych ani modeli, więc nie da się ocenić niepewności.
- To jeden framework i jeden rodzaj zadań. Nie wynika z tego, że pasywny kontekst zawsze wygrywa. Autorzy sami wskazują, że skille nadają się do konkretnych, wywoływanych przez użytkownika procedur.

---

## 4. Prawdopodobne mechanizmy

Vercel wskazuje jako możliwe wyjaśnienia:

1. **Brak punktu decyzyjnego:** informacja jest w kontekście, agent nie musi uznać, że czegoś nie wie.
2. **Stała dostępność:** indeks jest obecny w każdej turze, a skill ładuje się asynchronicznie.
3. **Brak problemu kolejności:** nie trzeba wybierać, czy najpierw czytać dokumentację, czy eksplorować projekt.

To interpretacje autorów, a nie osobno zmierzone przyczyny.

---

## 5. Wnioski praktyczne (autorskie)

1. Wiedzę potrzebną w większości zadań dawaj jako **krótki indeks** w `AGENTS.md`, a szczegóły w plikach czytanych na żądanie.
2. Pasywny kontekst też kosztuje: jest wysyłany w każdej sesji, więc pilnuj jego rozmiaru.
3. Jeśli polegasz na skillu, sprawdź na własnych zadaniach, czy faktycznie się uruchamia.

## Źródła

- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [Hacker News #46809708](https://news.ycombinator.com/item?id=46809708)
