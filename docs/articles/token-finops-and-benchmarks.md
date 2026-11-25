# FinOps i Niezależne Benchmarki Tokenowe w Programowaniu Agentowym

Wielka synteza najnowszych badań empirycznych, analiz FinOps (Glean, Concordia, Stevens Institute, Bruniaux, Silfverskiöld) oraz pomiarów telemetrycznych z 2026 roku.

---

## 1. Gdzie Naprawdę Uciekają Tokeny? Badania Empiryczne (Glean, Concordia & Stevens)

Badania laboratoryjne nad wieloagentowymi systemami deweloperskimi (m.in. ChatDev) obaliły powszechne mity na temat struktury kosztów:

| Kategoria zużycia | Udział w łącznym wolumenie tokenów | Wniosek inżynierski |
|---|---|---|
| **Samo Code Review i weryfikacja** | **59.4%** | Agenci recenzujący i dyskutujący o poprawkach spalają więcej tokenów niż agent piszący kod! |
| **Tokeny Wejściowe (Input Context)** | **53.9% – 92%** | Koszt sesji zależy niemal wyłącznie od wielkości przesyłanego kontekstu, a nie od wygenerowanego kodu. |
| **Pasywne logi i terminal** | **15% – 35%** | Wyniki komend powłoki (passing testy, paski pobierania) to czysty narzut bezwartościowy dla modelu. |

---

## 2. Krytyczna Ewaluacja Narzędzi: Raport Floriana Bruniaux (`cc.bruniaux.com`)

Florian Bruniaux zestawił deklaracje marketingowe **43 komercyjnych i otwartoźródłowych narzędzi** z **8 niezależnymi benchmarkami** oraz 15 pracami z arXiv:

### A. Narzędzia, które FAKTYCZNIE działają:
1. **Filtry wyjścia CLI (np. RTK — Rust Token Killer)**:
   - **Wynik**: Realna, powtarzalna redukcja **48% do 81% (w porywach do 90%)** tokenów wyjściowych z terminala.
   - **Dlaczego działa**: Działa na zewnątrz modelu, w sposób czysto deterministyczny. Nie zniekształca promptu i nie wprowadza halucynacji.
2. **Pasywne mapy symboli i repo-maps (AST)**:
   - **Wynik**: Spadek liczby operacji `read_file` o ponad 75% przy skoku skuteczności za pierwszym razem do 95%+.

### B. Ostrzeżenie przed "Magicznymi Kompresorami Promptu":
Bruniaux przestrzega przed narzędziami w locie kompresującymi prompt systemowy lub usuwającymi "zbędne słowa" z zapytania programisty:
- **Rozbijanie Prompt Cache**: Dynamiczna kompresja tekstu w każdej turze powoduje ciągły *cache miss* u dostawcy API (Anthropic/OpenAI), przez co płacisz pełną stawkę za każdą turę.
- **Degradacja rozumowania**: Usunięcie pozornie nieistotnych słów z kodu (np. kwalifikatorów typów czy nazw argumentów) drastycznie obniża precyzję modelu w zadaniach debugowania.

---

## 3. Cztery Filary Oszczędzania Tokenów (Ida Silfverskiöld)

W głośnym przewodniku dla Towards Data Science Ida Silfverskiöld definiuje 4 filary architektury FinOps:

1. **Strategic Prompt Caching (Zysk: 41% – 80% kosztów API)**:
   - Kluczem jest **niezmienność prefiksu**. Statyczne reguły i definicje narzędzi muszą znajdować się na samym początku promptu.
   - **Zegar TTL Cache'a (5 minut)**: Dostawcy chmurowi trzymają cache w pamięci przez około 5 minut. Koordynacja pętli agentowych w tym oknie czasowym zamienia drogie zapytania w groszowe hity cache.
2. **Leniwe Ładowanie Narzędzi (Lazy-Loading)**:
   - Kategoryczny zakaz pre-ładowania 40 definicji funkcji MCP do każdej sesji.
3. **Kaskady Spekulatywne (Speculative Cascades)**:
   - Tani, mały model próbuje wykonać zadanie jako pierwszy. Dopiero w przypadku niskiej pewności (mierzonej logprobs / entropią) zapytanie jest eskalowane do drogiego modelu frontier.
4. **Kompakcja Kontekstu (Context Compaction)**:
   - Agresywne usuwanie śmieci z historii czatu po zakończeniu fazy eksploracji.

---

## 4. LOOP Skill Engine i Deterministyczny Replay (Oszczędność > 93%)

Artykuł *From Prototype to Profit* analizuje powtarzalne eksploracje agentów:
- W powtarzalnych procesach deweloperskich (np. codzienne sprawdzanie zgłoszeń, generowanie raportów, aktualizacja zależności) agent za każdym razem "odkrywa Amerykę na nowo", paląc tysiące tokenów na błądzenie.
- **Podejście LOOP / Hybrydowe `SKILL.md`**:
  - Pierwsze przejście zadania jest rejestrowane jako deterministyczny graf kroków.
  - Kolejne wywołania tego samego zadania korzystają z deterministycznego odtworzenia ścieżki (Replay).
  - **Efekt**: Spadek zużycia tokenów o **93.3% do 99.98%** przy jednoczesnym braku ryzyka halucynacji.

---

## 5. Doświadczenia Korporacyjne (Qt.io & 87 000 Wywołań Claude Code)

### A. Wnioski Qt.io dla Środowisk Enterprise
- **Wycinki dokumentacji przez MCP**: Zamiast pozwalać agentowi na scrapowanie całych stron HTML z dokumentacją, serwer MCP serwuje chirurgicznie wycięte fragmenty Markdown zawierające wyłącznie sygnaturę szukanej klasy/metody.
- **Determinizm Przed Inferencją**: Uruchomienie lintera, kompilatora i formatowania *przed* wysłaniem kodu do LLM eliminuje 80% zbędnych tur naprawczych.

### B. Analiza 87 000 Wywołań (Shakib Uzzaman & Mykhailo Medved)
- Dodawanie do środowiska "skilli oszczędzających tokeny" potrafi paradoksalnie **podnieść łączny koszt sesji**.
- Jeśli skill wprowadza szum decyzyjny (agent waha się, czy go użyć, wykonuje niepotrzebne tool calle, a potem i tak czyta pliki), bilans tokenowy wychodzi na minus.
- **Wniosek**: Tylko pasywne, deterministyczne mechanizmy (twarde filtry CLI, `.cursorignore`, statyczna mapa repo) dają gwarantowany zwrot z inwestycji (ROI).
