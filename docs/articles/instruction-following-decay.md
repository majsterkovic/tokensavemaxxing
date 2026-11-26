---
title: "Przeciążenie Instrukcjami: Jak Pisać Krótkie Reguły"
description: "Co o długości CLAUDE.md i liczbie instrukcji pisze HumanLayer oraz które zasady są konwencją tego repozytorium."
---

Punktem wyjścia jest post [HumanLayer: Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md). To **poradnik, nie własne badanie** autorów.

:::caution[Korekta]
Wcześniejsza wersja tej strony przypisywała HumanLayer badania laboratoryjne, tabelę „Compliance Rate” zależną od liczby tokenów i twardy limit 2000 tokenów. **Poradnik ich nie zawiera.** Zostały usunięte.
:::

---

## 1. Co mówi źródło

- Wraz ze wzrostem **liczby instrukcji** modele gorzej ich przestrzegają. Według posta spadek jest **równomierny**, czyli nie dotyczy tylko nowszych instrukcji. HumanLayer opiera się tu na zewnętrznej pracy [arXiv:2507.11538](https://arxiv.org/abs/2507.11538).
- Plik instrukcji powinien być **krótki i zawierać to, co dotyczy większości zadań**. Autorzy zalecają mniej niż 300 linii.

### Co pokazuje sama praca (IFScale)

- **Test:** od 10 do 500 instrukcji typu „użyj tego słowa” w zadaniu pisania raportu biznesowego; 20 modeli od siedmiu dostawców.
- **Wynik:** przy 500 instrukcjach najlepsze modele osiągnęły **68%**.
- **Kształt spadku zależy od modelu:** progowy (m.in. `gemini-2.5-pro` i `o3` utrzymywały niemal pełną skuteczność do co najmniej 150 instrukcji), liniowy albo wykładniczy.
- **Kolejność ma znaczenie:** późniejsze instrukcje były częściej łamane. Ta przewaga wcześniejszych była zwykle największa przy **150–200** instrukcjach, a przy 300+ malała i błędy rozkładały się bardziej równomiernie.

Streszczenie „spada równomiernie” jest więc **uproszczeniem**. Praca nie bada też agentów programistycznych ani plików `CLAUDE.md`.

Twierdzenia dotyczą liczby instrukcji. Nie wynika z nich próg wyrażony w tokenach.

---

## 2. Budżet tego repozytorium (konwencja)

Skrypt `scripts/audit-context.sh` ostrzega powyżej **2000 tokenów** stałych instrukcji, a za wygodny cel przyjmujemy mniej niż 800. To **umowne progi**, które mają wymuszać zwięzłość, a nie zmierzone granice jakości. Skrypt podaje przybliżony przedział, nie wynik tokenizera.

---

## 3. Przykłady kodu w regułach

Długie bloki kodu w stale ładowanych regułach (to zalecenie praktyczne):

1. zajmują kontekst w każdej sesji,
2. łatwo się dezaktualizują.

Zamiast kopii kodu wskaż istniejący plik:

```markdown
❌ ZŁE:
Oto jak pisać endpoint:
import { z } from 'zod';
export async function POST(req: Request) { ...80 linii kodu... }

✅ DOBRE (ścieżka przykładowa, podaj plik istniejący w projekcie):
Wzorce endpointów API: wzoruj się na `src/api/auth/route.ts`.
```

Wskazaną ścieżkę trzeba utrzymywać. Reguła z nieistniejącym plikiem wprowadza agenta w błąd.

---

## 4. Reaktywne dodawanie reguł (konwencja)

Dodaj regułę, gdy:
1. agent powtórzył błąd w co najmniej dwóch niezależnych sesjach,
2. nie wymusi tego linter, kompilator ani formatter,
3. da się ją zapisać konkretnie.
   - Źle: *„Dbaj o czystość architektury.”*
   - Dobrze: *„Nie używaj `any`. W plikach mutacji zwracaj `Result<T, AppError>`.”*

Reguły dotyczące bezpieczeństwa i nieodwracalnych działań warto dodać od razu, bez czekania na powtórkę.

## Źródła

- [HumanLayer: Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [arXiv:2507.11538](https://arxiv.org/abs/2507.11538) — *How Many Instructions Can LLMs Follow at Once?* (Jaroslawicz i in., 2025), praca przywoływana przez HumanLayer
