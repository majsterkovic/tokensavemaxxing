---
title: "Subagenty, Fan-Out i Izolacja Kontekstu Badawczego"
description: "Wzorce izolacji kontekstu badawczego: subagenty Scout/Builder, równoległy fan-out i ich koszty."
---

Opis wzorca orkiestracji subagentów. To **opracowanie autorskie**, nie wynik badania. O tym, że odczyty subagenta nie trafiają do głównego okna Claude Code, piszą też [Matthews Wong](https://www.matthewswong.com/en/blog/context-engineering-monorepo-ai-agents) i [Start Debugging](https://startdebugging.net/2026/05/how-to-structure-a-monorepo-so-claude-codes-context-stays-small).

---

## 1. Problem: eksploracja zostaje w historii

Zadanie zwykle ma dwie fazy:
1. **Badawczą:** grep po symbolach, odczyt wielu plików, szukanie użyć.
2. **Implementacyjną:** edycja kilku plików i testy.

Gdy wykonuje je jeden wątek, odczytane pliki zostają w historii (do czasu kompakcji) i są wysyłane w kolejnych turach.

---

## 2. Wzorzec: badawczy subagent tylko do odczytu

Subagent pracuje w osobnym oknie kontekstowym i zwraca głównemu agentowi wnioski.

```
Agent główny ──zlecenie: „znajdź powiązania X”──→ Subagent (read-only)
Agent główny ←── ścieżki, numery linii, wnioski ── czyta i analizuje pliki
```

### Co faktycznie oszczędza
- Przykładowo (**liczby ilustracyjne, bez zapisanej metodyki**) zamiast 6100 tokenów odczytów do głównej sesji może trafić około 420 tokenów raportu.
- To dotyczy **tylko głównego kontekstu**. Subagent sam zużywa tokeny: wczytuje własny prompt, narzędzia i te same pliki. **Łączne zużycie może być wyższe.**
- Opłaca się, gdy eksploracja jest duża, a główna sesja długa. Przy małym zadaniu zwykle nie.

---

## 3. Kontrakt komunikacji (konwencja)

Domyślnie subagent zwraca **ścieżki z numerami linii i wnioski**, bez dużych zrzutów kodu. Krótki cytat jest uzasadniony, gdy od dokładnej treści zależy decyzja. Przed edycją agent główny czyta właściwy fragment sam.

```text
ZADANIE: Znajdź wszystkie wywołania validateSession() w serwisach backendowych.
WYMÓG ODPOWIEDZI:
1. Dokładne ścieżki z numerami linii (np. src/auth/guard.ts:84).
2. Jedno zdanie o tym, jak wynik walidacji jest używany w danym miejscu.
3. Bez dużych bloków kodu; zaznacz, czego nie udało się sprawdzić.
```

---

## 4. Wybór modelu

Proste wyszukiwanie można zlecić tańszemu modelowi (np. klasy Haiku lub Flash). Różnicę ceny sprawdź w aktualnym cenniku. Tańszy model może coś przeoczyć, więc przy zadaniach wymagających rozumowania nie oszczędzaj na modelu. Przykład delegacji masowego czytania opisuje [studium Spotify](/tokensavemaxxing/articles/spotify-shunt-and-portal/).

## Źródła

- [Matthews Wong: Context engineering for AI coding agents in a monorepo](https://www.matthewswong.com/en/blog/context-engineering-monorepo-ai-agents)
- [Start Debugging: How to structure a monorepo](https://startdebugging.net/2026/05/how-to-structure-a-monorepo-so-claude-codes-context-stays-small)
- [Spotify Engineering: Portal by Spotify](https://engineering.atspotify.com/2026/09/portal-by-spotify-cut-my-claude-code-token-usage-by-90)
