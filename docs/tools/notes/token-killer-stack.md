# Kompendium: Ekosystem 4 Narzędzi Redukcji Tokenów (RTK, Context Mode, Ponytail, Caveman)

Szczegółowy przegląd nowoczesnego stosu FinOps dla programowania agentowego (opisanego m.in. w DataCamp i analizach Floriana Bruniaux).

---

## 🏗️ Matryca 4 Warstw Pętli Agenta

Tokeny w pętli agenta uciekają w 4 różnych punktach. Każde z poniższych narzędzi zabezpiecza inny odcinek pętli, dzięki czemu wzajemnie się nie dublują:

```
                      ┌─────────────────────────────────┐
                      │    Polecenie w terminalu CLI    │
                      └────────────────┬────────────────┘
                                       │
                    [WARSTWA 1: Wejście z CLI] ──► RTK (Rust Token Killer)
                    Cięcie logów, testów i gita o 60–90%
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │       Ciężkie pliki i MCP       │
                      └────────────────┬────────────────┘
                                       │
                    [WARSTWA 2: Pamięć sesji]  ──► Context Mode
                    Indeksacja w SQLite FTS5, tylko esencja do LLM
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │      Model Językowy (LLM)       │
                      └────────────────┬────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
 [WARSTWA 3: Generowany Kod]                            [WARSTWA 4: Komunikacja]
        Ponytail                                                Caveman
 Zwalczanie over-engineeringu,                          Eliminacja lania wody,
 wymuszenie reguły YAGNI                                zwięzły, telegraficzny styl
```

---

## 1. RTK (Rust Token Killer) — Warstwa Terminala
- **Co optymalizuje**: To, co agent **odczytuje z procesów powłoki**.
- **Mechanizm**: Przechwytuje wywołania `git`, `cargo`, `npm`, `pytest`, `docker`. Zamiast 500 linii przechodzących testów przekazuje jedną linijkę podsumowania i wyciąga wyłącznie błędy.
- **Zysk**: 60% – 90% redukcji tokenów wyjściowych z komend.
- **Więcej**: [rtk.md](rtk.md).

---

## 2. Context Mode — Warstwa Ciężkich Narzędzi i Sesji
- **Co optymalizuje**: To, co agent **przechowuje w pamięci roboczej sesji**.
- **Mechanizm**:
  - Działa jako lokalny serwer MCP lub warstwa indeksująca.
  - Zamiast wpychać całe 500-stronicowe dokumentacje lub wielkie pliki JSON do aktywnego okna kontekstowego, zapisuje je lokalnie w bazie **SQLite FTS5** (Full-Text Search).
  - Do LLM trafia wyłącznie skrót i identyfikator zapytania. Gdy agent potrzebuje szczegółów, wykonuje precyzyjną kwerendę SQL/FTS zamiast czytać cały zrzut.
- **Zysk**: Zapobiega eksplozji okna kontekstowego przy skanowaniu dużych źródeł danych.

---

## 3. Ponytail (`DietrichGebert/ponytail`) — Warstwa Kodu
- **Co optymalizuje**: To, co agent **generuje w plikach źródłowych**.
- **Problem**: Modele LLM mają wbudowaną tendencję do over-engineeringu — piszą dziesiątki klas pomocniczych, tworzą zbędne abstrakcje i instalują nowe pakiety npm dla prostych operacji.
- **Mechanizm**: Wymusza ścisłą drabinę decyzyjną **YAGNI (You Aren't Gonna Need It)**:
  1. Czy da się to zrobić standardowymi funkcjami języka bez nowych klas?
  2. Czy funkcja istnieje już w projekcie?
  3. Kategoryczny zakaz dodawania zależności, jeśli funkcjonalność wymaga mniej niż 30 linii kodu.
- **Zysk**: Zmniejsza rozmiar generowanych diffów o 40–60%, ułatwiając code review i eliminując dług technologiczny.

---

## 4. Caveman (`getcaveman.dev`) — Warstwa Komunikacji
- **Co optymalizuje**: To, co agent **mówi do programisty (Output Tokens)**.
- **Problem**: Modele marnują tokeny na uprzejme formułki: *"Oczywiście! Chętnie Ci pomogę. Oto szczegółowe wyjaśnienie krok po kroku, dlaczego ten kod działa..."*.
- **Mechanizm**: Modyfikator zachowania narzucający surowy, zwięzły styl komunikacji (*"why use many token when few token do trick"*):
  - Zero grzecznościowych wstępów.
  - Zero powtarzania pytania użytkownika.
  - Odpowiedź składa się wyłącznie z gotowego kodu lub listy zmienionych linii.
- **Zysk**: Skraca output konwersacyjny o 50–70%, przyspieszając czas odpowiedzi o kilka sekund per tura.
