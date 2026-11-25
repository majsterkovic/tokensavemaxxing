---
title: "Notatka Narzędziowa: OpenAI Codex / Reasoning Models (o3-mini, GPT-4o)"
description: "Notatka Narzędziowa: OpenAI Codex / Reasoning Models (o3-mini, GPT-4o)"
---

> **Rola w ekosystemie**: Rozwiązywanie trudnych zagadek algorytmicznych, zawiłych maszyn stanów, parsowania AST oraz audyt matematyczno-logiczny kodu.

---

## 1. Profil Narzędzia

- **Twórca**: OpenAI.
- **Modele kluczowe**: `o3-mini` (wysoka wydajność rozumowania), `o1` / `o1-pro`, `gpt-4o` (wszechstronny).
- **Format**: Integracja przez oficjalne CLI, rozszerzenia IDE lub API wewnątrz narzędzi orkiestrujących (T3 Code, OpenCode).

---

## 2. Cechy Szczególne: Ukryte Tokeny Rozumowania (Reasoning Tokens)

Modele z rodziny "o" (np. `o3-mini`, `o1`) działają w oparciu o wewnętrzne łańcuchy myślowe (Chain of Thought):
- Przed wygenerowaniem odpowiedzi model generuje od kilkuset do kilkunastu tysięcy niewidocznych tokenów rozumowania.
- **Wpływ na koszt**: Choć tokeny te nie zawsze są widoczne w oknie czatu, są w pełni rozliczane na poziomie API.
- **Wpływ na jakość**: Bezbłędna eliminacja błędów typu off-by-one, znakomite operacje na grafach i weryfikacja logiki typów.

---

## 3. Konfiguracja pod Tokensavemaxxing

1. **Ustawienie poziomu rozumowania (`reasoning_effort`)**:
   - Dla standardowego kodu ustawiaj `low` lub `medium`.
   - Wartość `high` rezerwuj wyłącznie dla zadań kryptograficznych, zawiłych algorytmów optymalizacyjnych lub trudnych reguł biznesowych.
2. **Kategoryczny zakaz używania do błahego wyszukiwania**:
   - Nigdy nie używaj modeli rozumujących jako "wyszukiwarki plików" czy "skanera składni". To marnotrawstwo budżetu tokenów.
3. **Precyzyjny prompt wejściowy**:
   - Podawaj modelowi wyłącznie izolowaną funkcję + wejście/wyjście + przypadek brzegowy, który powoduje błąd.

---

## 4. Kiedy Używać
- Złożona logika biznesowa (np. kalkulatory prowizji, transakcje finansowe, rozliczenia walutowe).
- Parsery, kompilatory, zaawansowane reguły regex lub drzewa AST.
- Weryfikacja współbieżności i unikanie zakleszczeń (deadlocks/race conditions).

## 5. Kiedy NIE Używać
- Generowanie standardowego kodu CRUD / szablonów HTML/CSS.
- Przeszukiwanie bazy kodu (zastąp modelem lokalnym lub Flash).
