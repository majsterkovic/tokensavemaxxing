---
title: "Receptury Operacyjne i Playbooki (Flows)"
description: "Receptury Operacyjne i Playbooki (Flows)"
---


# Receptury Operacyjne i Playbooki (Flows)

Zbiór ustandaryzowanych, powtarzalnych procedur pracy z agentami AI dla typowych scenariuszy inżynierii oprogramowania.

---

## 📋 Spis Receptur Operacyjnych

| Playbook | Scenariusz zastosowania | Kluczowa technika |
|---|---|---|
| [01-feature-development.md](01-feature-development.md) | Implementacja nowej funkcjonalności od zera | Pętla Spec-First, subagent badawczy, kontrakt API, weryfikacja TDD |
| [02-debugging-and-rca.md](02-debugging-and-rca.md) | Diagnoza błędu produkcyjnego i Root Cause Analysis | Hipoteza -> Minimalny odczyt logów -> Test reprodukcyjny -> Naprawa |
| [03-token-savemaxxing.md](03-token-savemaxxing.md) | Kompleksowy program optymalizacji kosztów tokenów (3 repo) | Pomiary, 4 warstwy redukcji, repo-map, prompt cache, pułapki |
| [04-multi-repo-coordination.md](04-multi-repo-coordination.md) | Praca w architekturach frontend + backend + e2e | Folder-scoped workspaces, zapobieganie kolizji reguł, symlinki |
| [05-code-review-and-refactor.md](05-code-review-and-refactor.md) | Bezpieczny refaktoring i automatyczny audyt PR | Subagent w roli bezstronnego recenzenta, kontrola regresji typów |

---

## 🎯 Jak Korzystać z Playbooków

Każdy playbook definiuje:
1. **Wstępne wymagania (Prerequisites)**: Co musi być przygotowane przed uruchomieniem czatu.
2. **Kroki tura po turze (Turn-by-Turn Flow)**: Dokładne instrukcje, co pisze człowiek, a co wykonuje agent.
3. **Kryteria ukończenia (Definition of Done)**: Kiedy bezwzględnie należy zamknąć sesję i nie dopuścić do "dopytywania dla pewności".
4. **Gotowe szablony promptów do wklejenia**.
