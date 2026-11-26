---
title: "Ekosystem Agent Skills w 2026: Standard `SKILL.md`, Superpowers i Katalogi"
description: "Przegląd formatu Agent Skills, popularnych paczek i ich wpływu na kontekst."
---

Przegląd otwartego formatu **Agent Skills** ([agentskills.io](https://agentskills.io/home)), wybranych paczek i ich wpływu na budżet tokenowy.

---

## 1. Czym jest `SKILL.md`

Skill to folder zawierający:
- `SKILL.md`: instrukcję z frontmatterem YAML (co najmniej nazwa i opis),
- `scripts/` (opcjonalnie): skrypty pomocnicze,
- `references/` (opcjonalnie): dokumentację czytaną na żądanie.

Format obsługuje wiele harnessów, ale obsługiwane pola i sposób aktywacji mogą się różnić. Sprawdź dokumentację swojego narzędzia.

---

## 2. Przykładowe skille

Zestawienie orientacyjne na podstawie przeglądów [Agentailor](https://blog.agentailor.com/posts/top-agent-skills-for-agentic-engineering-2026) i [Firecrawl](https://www.firecrawl.dev/blog/best-claude-code-skills). Kolumna o kontekście to **przypuszczenia autora repo**, nie pomiary.

| Skill / paczka | Zastosowanie | Możliwy wpływ na kontekst |
|---|---|---|
| **`obra/superpowers`** (wg Agentailor 225 tys.+ ⭐) | Workflow: planowanie, TDD, subagenty, worktrees | Subagenty izolują kontekst, ale workflow sam też zużywa tokeny |
| **`spec-driven-development`** | Specyfikacja przed kodem | Może ograniczyć poprawki po błędnych założeniach |
| **Grill Me** | Pytania doprecyzowujące przed kodowaniem | Jak wyżej |
| **Handoff** | Zapis stanu sesji do pliku | Pozwala zacząć nową sesję z krótkim streszczeniem (część szczegółów przepada) |
| **Karpathy's Guidelines** | Zasady ograniczające zbędne zmiany | Może ograniczyć niepotrzebne refaktory |
| **Frontend / React (Vercel Labs)** | Wzorce frontendowe | Zależy od zadania |

---

## 3. Katalogi

- [agentskills.io](https://agentskills.io/home) — specyfikacja formatu.
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)
- [Temat `agent-skills` na GitHubie](https://github.com/topics/agent-skills)
- [agenticskills.io](https://agenticskills.io/skills)

Skill to cudze instrukcje, a czasem także skrypty. Przed instalacją przeczytaj jego zawartość.

---

## 4. Wpływ na tokeny

### Możliwe korzyści
Pełna instrukcja skilla ładuje się dopiero po aktywacji. Na stałe w kontekście zostają zwykle nazwy i opisy.

### Możliwe koszty
- Każdy zainstalowany skill dokłada opis do stałego kontekstu.
- Agent może nie uruchomić potrzebnego skilla. W [ewaluacji Vercel](/tokensavemaxxing/articles/passive-vs-active-context/) **w 56% przypadków skill nie został użyty** (jeden skill, zadania z Next.js 16).

Wcześniejsza wersja przypisywała „analizie 87 000 sesji” liczbę 56% błędnych wywołań i wniosek o szkodliwości 30 skilli. **Nie znaleziono dla tego źródła**, więc usunięto. Zalecenie **3–5 skilli na projekt** to konwencja tego repozytorium, niezmierzony próg.

## Źródła

- [agentskills.io](https://agentskills.io/home)
- [Agentailor: Top agent skills for agentic engineering](https://blog.agentailor.com/posts/top-agent-skills-for-agentic-engineering-2026)
- [Firecrawl: Best Claude Code skills](https://www.firecrawl.dev/blog/best-claude-code-skills)
- [Vercel: AGENTS.md outperforms skills](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
