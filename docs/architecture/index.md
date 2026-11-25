---
title: "Wzorce Architektoniczne Kontekstu i Promptów"
description: "Wzorce Architektoniczne Kontekstu i Promptów"
---


# Wzorce Architektoniczne Kontekstu i Promptów

Architektura warstwowa, zarządzanie pamięcią modelu oraz wzorce orkiestracji subagentów.

---

## 🏛️ Dokumenty w Sekcji

| Dokument | Tematyka | Kluczowy wniosek |
|---|---|---|
| [context-hierarchy.md](context-hierarchy.md) | 4-Warstwowy Model Kontekstu | Warstwy 0–3: Od Always-On (<800 tok), przez pasywną mapę AST, reguły warunkowe (`globs`), po odczyt lazy-loaded. |
| [rule-hygiene.md](rule-hygiene.md) | Higiena i Dyscyplina Reguł | 3 Prawa Higieny Reguł (Reaktywność, Determinizm, Budżet <2000 tok) i eliminacja antywzorców ("Rule Bloat"). |
| [subagent-patterns.md](subagent-patterns.md) | Wzorce Projektowe Subagentów | Wzorce Scout & Builder, Scatter-Gather (równoległy fan-out) oraz Critic/Reviewer dla bezstronnej weryfikacji. |
