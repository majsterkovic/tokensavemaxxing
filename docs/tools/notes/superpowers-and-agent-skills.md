# Notatka Narzędziowa: `obra/superpowers` i Złoty Zestaw Skilli

> **Rola w ekosystemie**: Kanoniczny zestaw umiejętności agentowych narzucający rygor inżynieryjny (TDD, planowanie, izolacja subagentów, git worktrees) oraz procedury bezpiecznego kodowania.

---

## 1. Zestaw `obra/superpowers` (Jesse Vincent — 225k+ ⭐)

`obra/superpowers` to najczęściej instalowany pakiet skilli w środowisku Claude Code i pokrewnych agentów. Jego fenomen wynika z faktu, że **zastępuje chaos dyscypliną procesu inżynieryjnego**:

1. **Subagent Isolation by Default**:
   Każde podzadanie analityczne lub poszukiwawcze jest automatycznie delegowane do subagenta. Agent główny nie gromadzi śmieci w kontekście.
2. **Git Worktree Automation**:
   Skill automatycznie zarządza tworzeniem gałęzi w osobnych katalogach roboczych (`git worktree`), uniemożliwiając agentowi zabrudzenie głównej gałęzi `main`.
3. **Wymuszenie TDD**:
   Przed modyfikacją kodu agent musi napisać i uruchomić test sprawdzający (failing test).

---

## 2. Złota Czwórka Skilli Uzupełniających

### A. `Grill Me` (Rygorystyczny Wywiad Przed Implementacją)
- **Problem**: Agent zaczyna pisać kod na podstawie domysłów, po czym okazuje się, że użytkownik miał na myśli inną bibliotekę lub format bazy.
- **Działanie skilla**: Agent blokuje pisanie kodu i zadaje programiście 3–5 precyzyjnych pytań wielokrotnego wyboru lub pytań o przypadki brzegowe.
- **Oszczędność**: Zapobiega wyrzuceniu do kosza setek wygenerowanych linii kodu.

### B. `Handoff` (Kompresja i Przekazanie Pałeczki)
- **Problem**: Czat osiągnął 25 tur, kontekst jest spuchnięty, a każda odpowiedź kosztuje fortunę i trwa 20 sekund.
- **Działanie skilla**: Agent podsumowuje: co zrobiono, jakie decyzje podjęto, jakie pliki zmieniono i co jest następnym krokiem, zapisując to w pliku `docs/HANDOFF.md`.
- **Następny krok**: Zamykasz czat i w nowej, czystej sesji wpisujesz: *"Kontynuuj zgodnie z `docs/HANDOFF.md`"*.

### C. `Andrej Karpathy's Guidelines` (Dyscyplina i Powściągliwość)
Cztery kardynalne zasady kodowania z LLM:
1. **Nie ruszaj działającego kodu**: Zakaz "ulepszania przy okazji" sąsiednich funkcji.
2. **Minimalny diff**: Zmiana ma dotykać wyłącznie linijek niezbędnych do usunięcia błędu.
3. **Nie dodawaj zależności**: Jeśli problem można rozwiązać kilkunastoma linijkami standardowego kodu, nie instaluj nowej paczki.
4. **Weryfikacja empiryczna**: Każda zmiana musi być potwierdzona uruchomieniem testu.

---

## 3. Jak Skonfigurować Skille w Swoim Repozytorium

Struktura folderu `.agents/skills` lub `skills/`:
```
moj-projekt/
├── .agents/
│   └── skills/
│       ├── superpowers/
│       │   └── SKILL.md
│       ├── grill-me/
│       │   └── SKILL.md
│       └── handoff/
│           └── SKILL.md
```

Agent automatycznie wykrywa pliki `SKILL.md` i aktywuje je wyłącznie w momencie, gdy prompt użytkownika wskazuje na potrzebę ich użycia (Lazy Loading).
