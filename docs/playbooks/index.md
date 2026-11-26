---
title: "Receptury Operacyjne i Playbooki (Flows)"
description: "Ustandaryzowane procedury pracy z agentami AI: feature dev, debugging RCA, tokensavemaxxing, multi-repo i code review."
---

Zbiór powtarzalnych procedur pracy z agentami AI dla typowych scenariuszy inżynierii oprogramowania.

## 📋 Spis Receptur Operacyjnych

| Playbook | Scenariusz zastosowania | Kluczowa technika |
|---|---|---|
| [01: Feature Development](/tokensavemaxxing/playbooks/01-feature-development/) | Implementacja nowej funkcji od zera | Pętla Spec-First, subagent badawczy, weryfikacja TDD |
| [02: Debugging i RCA](/tokensavemaxxing/playbooks/02-debugging-and-rca/) | Diagnoza błędu i Root Cause Analysis | Hipoteza → Minimalny odczyt logów → Test reprodukcyjny |
| [03: tokensavemaxxing](/tokensavemaxxing/playbooks/03-token-savemaxxing/) | Optymalizacja kosztów tokenów (3 repo) | Pomiary, 4 warstwy redukcji, repo-map, prompt cache |
| [04: Multi-Repo Coordination](/tokensavemaxxing/playbooks/04-multi-repo-coordination/) | Praca w układzie frontend + backend + e2e | Folder-scoped workspaces, zapobieganie kolizji reguł |
| [05: Code Review & Refactor](/tokensavemaxxing/playbooks/05-code-review-and-refactor/) | Bezpieczny refaktoring i audyt PR | Subagent w roli niezależnego recenzenta, kontrola typów |

## 🎯 Jak korzystać

Playbooki to procedury autorskie. Nie wszystkie mają tę samą budowę, a podane progi (liczby linii, tur, tokenów) to konwencje do dostosowania.
