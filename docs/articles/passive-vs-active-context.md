# Pasywny Kontekst vs Dynamiczne Narzędzia (Ewaluacja Vercel)

Analiza oficjalnego badania inżynierów Vercel (styczeń 2026) nad skutecznością agentów AI w projektach z nowym API Next.js 16 oraz powiązanej dyskusji na Hacker News (wątek #46809708).

---

## 1. Konstrukcja Badania

Vercel przeprowadził benchmark porównujący, jak modele językowe radzą sobie z implementacją zadań wymagających wiedzy o najnowszych zmianach w API Next.js 16 (gdzie wiedza bazowa modelu z pre-trainingu zawierała stare lub nieaktualne wzorce).

Przetestowano trzy strategie dostarczania wiedzy:
1. **Baseline**: Brak zewnętrznej dokumentacji (agent korzysta z wiedzy wbudowanej i zgaduje).
2. **Skill / On-Demand Tool**: Agent ma do dyspozycji narzędzie / skill, który potrafi pobrać oficjalną dokumentację Next.js, jeśli agent uzna to za konieczne.
3. **Skill + Jawne Instrukcje Promptu**: Agent ma skill oraz w prompcie systemowym twardy nakaz: *"Przed użyciem API sprawdź dokumentację przez skill"*.
4. **Pasywny, skompresowany indeks (8KB w AGENTS.md)**: Skondensowana mapa zmian w składni załadowana bezpośrednio do kontekstu startowego.

---

## 2. Wyniki Liczbowe

| Konfiguracja | Pass Rate (Sukces zadania) | Różnica vs Baseline | Częstotliwość użycia narzędzia |
|---|---|---|---|
| **1. Baseline** | 53% | — | — |
| **2. Skill (autonomiczna decyzja)** | **53%** | **+0 pp** | Użyty tylko w 44% przypadków! |
| **3. Skill + Wymuszenie w prompcie** | 79% | +26 pp | Użyty w ~88% przypadków |
| **4. Skompresowany indeks w AGENTS.md** | **100%** | **+47 pp** | Zawsze obecny (100%) |

### Krytyczna obserwacja: Awaria mechanizmu agent-decided activation
W konfiguracji nr 2, **w 56% przypadków agent nigdy nie wywołał narzędzia**, mimo że zadanie wprost dotyczyło nowego API, a narzędzie było w pełni dostępne i sprawne.
Co więcej, w rozbiciu na testy jednostkowe, obecność nieużywanego skilla w środowisku **obniżyła wyniki z 63% do 58%**, wprowadzając szum decyzyjny (decision noise).

---

## 3. Dlaczego Pasywny Kontekst Zawsze Wygrywa?

Z dyskusji architektów na Hacker News i wniosków Vercel wynikają trzy fundamentalne mechanizmy poznawcze modeli LLM:

### 1. Eliminacja punktu decyzyjnego (Zero Decision Points)
Gdy agent musi sam zdecydować: *"Czy to, co wiem, jest wystarczające, czy powinienem wykonać tool call?"*, występuje zjawisko **nadmiernej pewności siebie (overconfidence)**. Model przewiduje najbardziej prawdopodobny token na podstawie wag, zakładając, że jego wiedza jest poprawna. Nie ma świadomości własnej niewiedzy. W pasywnym kontekście wiedza już jest w oknie, model po prostu ją widzi.

### 2. Eliminacja problemu kolejności (Sequential Order Conflict)
Wywołanie narzędzia wymaga sekwencyjnego planowania:
`Decyzja o search -> Oczekiwanie na odpowiedź narzędzia -> Parsowanie -> Planowanie kodu -> Zapis pliku`.
Jeśli cokolwiek w tym łańcuchu zostanie zakłócone, model przeskakuje od razu do fazy zapisu, pomijając krok weryfikacji.

### 3. Asynchroniczność i opóźnienia
Pobieranie wiedzy dynamicznie wydłuża czas tury i rozbija spójność pamięci roboczej agenta (working memory).

---

## 4. Wnioski dla Inżynierii Flow

1. **Kluczowa architektura systemu musi być pasywna**: Nie polegaj na skillu do pobierania mapy projektu. Umieść zwięzłą mapę (`REPO-MAP.md` lub `AGENTS.md`) w plikach ładowanych pasywnie.
2. **Kompaktowość jest kluczem**: Vercel skompresował 40KB dokumentacji do **8KB** w formacie pipe-delimited (`folder/plik -> lista symboli / reguł`). Dało to 100% skuteczności bez marnowania tokenów.
3. **Zasada brzytwy Ockhama dla Skills**: Każdy dodany skill zwiększa ryzyko, że model wybierze błędne narzędzie lub ulegnie dekoncentracji. Jeśli coś można dostarczyć w 20 linijkach zwięzłego tekstu — zrób to w tekście, nie w narzędziu.
