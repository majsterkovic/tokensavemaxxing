---
title: "Wzorce Architektoniczne Kontekstu i Promptów"
description: "Architektura warstwowa kontekstu, higiena reguł (<2000 tokenów) oraz wzorce projektowe subagentów."
---

Architektura warstwowa, zarządzanie pamięcią modelu oraz wzorce orkiestracji subagentów.

## 🏛️ Dokumenty w Sekcji

| Dokument | Tematyka | Kluczowy wniosek |
|---|---|---|
| [Hierarchia Kontekstu](/tokensavemaxxing/architecture/context-hierarchy/) | 4-Warstwowy Model Kontekstu | Warstwy 0–3: od Always-On (`<800 tok`), przez mapę AST i `globs`, po lazy-loading. |
| [Higiena Reguł](/tokensavemaxxing/architecture/rule-hygiene/) | Dyscyplina `.cursor/rules` | 3 Prawa Higieny Reguł (Reaktywność, Determinizm, Budżet `<2000 tok`). |
| [Wzorce Subagentów](/tokensavemaxxing/architecture/subagent-patterns/) | Orkiestracja Subagentów | Scout & Builder, Scatter-Gather (fan-out) oraz Critic/Reviewer. |
