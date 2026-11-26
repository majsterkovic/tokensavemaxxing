---
title: "Notatka Narzędziowa: `obra/superpowers` i Złoty Zestaw Skilli"
description: "Notatka Narzędziowa: `obra/superpowers` i Złoty Zestaw Skilli"
---

> **Rola w ekosystemie**: Kanoniczny zestaw umiejętności agentowych narzucający rygor inżynieryjny (TDD, planowanie, izolacja subagentów, git worktrees) oraz procedury bezpiecznego kodowania.

---

## 1. Zestaw `obra/superpowers` (Jesse Vincent)

[`obra/superpowers`](https://github.com/obra/superpowers) to popularny pakiet skilli dla Claude Code i pokrewnych agentów (według [Agentailor](https://blog.agentailor.com/posts/top-agent-skills-for-agentic-engineering-2026) ponad 225k gwiazdek w czerwcu 2026; pozycja „najczęściej instalowanego” — ⚠️ niezweryfikowane). Jego założenie to **dyscyplina procesu inżynieryjnego**:

1. **Subagent Isolation by Default**:
   Pakiet zawiera skille do delegowania zadań subagentom, co ogranicza kontekst głównego agenta. Delegowanie zależy od użytego skilla, konfiguracji i poleceń użytkownika.
2. **Git Worktree Automation**:
   Skill automatycznie zarządza tworzeniem gałęzi w osobnych katalogach roboczych (`git worktree`), żeby agent nie pracował bezpośrednio na gałęzi `main`.
3. **Wymuszenie TDD**:
   Przed modyfikacją kodu agent musi napisać i uruchomić test sprawdzający (failing test).

---

## 2. Złota Czwórka Skilli Uzupełniających

### A. `Grill Me` (Rygorystyczny Wywiad Przed Implementacją)
- **Problem**: Agent zaczyna pisać kod na podstawie domysłów, po czym okazuje się, że użytkownik miał na myśli inną bibliotekę lub format bazy.
- **Działanie skilla**: według [Firecrawl](https://www.firecrawl.dev/blog/best-claude-code-skills) agent przed pisaniem kodu dopytuje o plan aż do wspólnego zrozumienia.
- **Oszczędność**: Zapobiega wyrzuceniu do kosza setek wygenerowanych linii kodu.

### B. `Handoff` (Kompresja i Przekazanie Pałeczki)
- **Problem**: Czat osiągnął 25 tur, kontekst jest spuchnięty, a każda odpowiedź kosztuje fortunę i trwa 20 sekund.
- **Działanie skilla**: Agent podsumowuje: co zrobiono, jakie decyzje podjęto, jakie pliki zmieniono i co jest następnym krokiem, zapisując to w pliku `docs/HANDOFF.md`.
- **Następny krok**: Zamykasz czat i w nowej, czystej sesji wpisujesz: *"Kontynuuj zgodnie z `docs/HANDOFF.md`"*.

### C. `Andrej Karpathy's Guidelines` (Dyscyplina i Powściągliwość)
Cztery zasady z repozytorium [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (opracowanie innego autora na podstawie obserwacji Karpathy’ego):
1. **Think Before Coding**: nazwij założenia, niejasności i kompromisy, zanim zaczniesz kodować.
2. **Simplicity First**: bez nadmiarowej złożoności i zbędnych abstrakcji.
3. **Surgical Changes**: zmieniaj tylko to, czego wymaga zadanie.
4. **Goal-Driven Execution**: ustal sprawdzalne kryteria sukcesu, np. test, i pracuj do ich spełnienia.

---

## 3. Jak Skonfigurować Skille w Swoim Repozytorium

Przykładowa struktura (katalog skilli zależy od harnessa, sprawdź jego dokumentację):
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
