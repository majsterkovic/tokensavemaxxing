# Subagenty, Fan-Out i Izolacja Kontekstu Badawczego

Analiza wzorców architektonicznych orkiestracji subagentów w nowoczesnych harnessach deweloperskich (Claude Code 2.1+, Google Antigravity Swarm, Cursor Subagents).

---

## 1. Dlaczego Główny Agent Nie Powinien Eksplorować Samodzielnie?

W typowym flow deweloperskim zadanie składa się z dwóch faz:
1. **Faza badawcza (Exploration & Triage)**: Przeszukiwanie bazy kodu, grep po symbolach, odczytywanie 10-30 plików, lokalizacja definicji i miejsc użycia.
2. **Faza implementacji i testów (Execution & Verification)**: Precyzyjna edycja 2-3 plików, uruchomienie testów, formatowanie.

### Problem monoseptycznego agenta (Single Context Pollution):
Gdy jeden agent wykonuje obie fazy w tym samym wątku:
- Treść wszystkich 30 odczytanych w fazie badawczej plików (często 8 000 - 25 000 tokenów) pozostaje na zawsze w historii rozmowy.
- Każde kolejne pytanie użytkownika, każda poprawka linijki i każde wywołanie komendy w fazie implementacji musi re-transmitować cały ten historyczny zrzut.
- Model w fazie edycji jest rozproszony niepotrzebnymi szczegółami z plików pobocznych, co drastycznie zwiększa prawdopodobieństwo regresji kodu.

---

## 2. Kanoniczny Wzorzec: Subagent Badawczy (Read-Only Scout)

Subagent działa w odrębnym, izolowanym procesie z własnym, czystym oknem kontekstowym. Po zakończeniu pracy zwraca do agenta głównego jedynie syntetyczną konkluzję.

```
                  ┌───────────────────────────────┐
                  │         Agent Główny          │
                  │   (Orkiestrator / Builder)    │
                  └──────────────┬────────────────┘
                                 │
                   Zlecenie: "Znajdź powiązania X"
                   (Wymóg: tylko wnioski i ścieżki)
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │       Subagent Badawczy       │
                  │ (Model: Flash / Haiku / Pro)  │
                  │      Tryb: Read-Only          │
                  │                               │
                  │ Czyta: 35 plików (15k toków)  │
                  │ Analizuje relacje w kodzie    │
                  └──────────────┬────────────────┘
                                 │
                 Zwrot: Tylko wniosek (350 toków):
                 - Pliki do zmiany: src/a.ts, src/b.ts
                 - Uwaga na edge-case w linii 42
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │         Agent Główny          │
                  │  (Czysty kontekst, zero szumu,│
                  │   natychmiastowa implementacja│
                  └───────────────────────────────┘
```

### Wyniki w liczbach:
- **Tradycyjne podejście**: 6 100 tokenów wczytanych do historii głównej sesji.
- **Z subagentem badawczym**: **420 tokenów** wstrzykniętych do głównej sesji (oszczędność >93% miejsca w oknie kontekstowym orkiestratora).

---

## 3. Żelazna Reguła Komunikacji z Subagentem

> ⚠️ **ZAKAZ ZRZUCANIA EKSCERPTÓW KODU**
> Subagent badawczy **nigdy nie może kopiować i wklejać fragmentów kodu** do swojej odpowiedzi końcowej.

Jeśli subagent wklei 40 wyciętych bloków kodu, mechanizm oszczędzania zawodzi — płacisz za czytanie dwukrotnie, a historia sesji głównej zostaje zanieczyszczona.

### Prawidłowy kontrakt zadania subagenta:
```text
ZADANIE: Znajdź wszystkie wystąpienia funkcji validateSession() w serwisach backendowych.
WYMÓG ODPOWIEDZI:
1. Podaj listę dokładnych ścieżek z numerami linii (np. src/auth/guard.ts:84).
2. Podaj 1-zdaniowe podsumowanie, jak wynik walidacji jest przetwarzany w danym miejscu.
3. Kategoryczny zakaz wklejania bloków kodu i cytatów z plików.
```

---

## 4. Wybór Modeli: Arbitraż Kosztowy

Eksploracja kodu i przeszukiwanie plików to zadania o niskiej złożoności rozumowania (pattern matching i wyszukiwanie referencji).
- Do roli subagenta badawczego idealnie nadają się modele szybkie i tanie: **Gemini 2.0 Flash**, **Claude 3.5 Haiku**.
- Są od **10× do 25× tańsze** od modeli frontier (Sonnet, Pro, Opus, o3), a wykonują zadanie w ułamku sekundy.
- Model klasy frontier (Sonnet, Opus, Pro) rezerwujesz wyłącznie dla **agenta głównego** na czas podejmowania decyzji architektonicznych i precyzyjnej modyfikacji kodu.
