---
title: "Wzorce Projektowe Subagentów (Subagent Design Patterns)"
description: "Wzorce Projektowe Subagentów (Subagent Design Patterns)"
---


# Wzorce Projektowe Subagentów (Subagent Design Patterns)

Katalog sprawdzonych wzorców koordynacji i delegowania pracy pomiędzy agentem głównym (orkiestratorem) a agentami pomocniczymi.

---

## 1. Wzorzec "Scout & Builder" (Zwiadowca i Budowniczy)

Najbardziej powszechny i efektywny wzorzec w programowaniu:
- **Scout (Zwiadowca)**: Tani, szybki subagent z uprawnieniami read-only (np. Gemini Flash). Jego zadaniem jest przeszukanie kodu, znalezienie zależności i zwrot samych koordynatów (ścieżki i numery linii).
- **Builder (Budowniczy)**: Główny agent na mocnym modelu (np. Sonnet / Pro). Otrzymuje czystą, zwięzłą informację od Scouta i dokonuje precyzyjnej edycji kodu.

---

## 2. Wzorzec "Scatter-Gather" (Równoległy Fan-Out)

Stosowany przy zadaniach powtarzalnych na wielu niezależnych plikach (np. migracja 40 komponentów do nowego API lub audyt bezpieczeństwa wielu modułów):
1. **Scatter**: Orkiestrator dzieli listę plików na niezależne porcje (chunki) i uruchamia równolegle N subagentów.
2. **Execution**: Każdy subagent przetwarza swój podzbiór plików we własnym, odizolowanym kontekście.
3. **Gather**: Wyniki lub diffy spływają z powrotem do orkiestratora, który agreguje raport końcowy.

---

## 3. Wzorzec "Critic / Reviewer" (Niezależny Recenzent)

Stosowany do weryfikacji jakości przed zatwierdzeniem zmian:
- Subagent Reviewer otrzymuje jedynie `git diff` oraz zestaw reguł jakościowych.
- Nie zna historii wcześniejszej dyskusji i wątpliwości z sesji pisania kodu, dzięki czemu nie ulega uprzedzeniom poznawczym (zero confirmation bias).
- Zwraca surową ocenę: błędy logiczne, edge-cases, wycieki zasobów.
