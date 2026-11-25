---
title: "Notatka Narzędziowa: Google Antigravity CLI (`agy`)"
description: "Notatka Narzędziowa: Google Antigravity CLI (`agy`)"
---

> **Rola w ekosystemie**: Silnik orkiestracji zaawansowanych potoków (workflows), rojów agentów (`swarm`), rozbudowanych subagentów i arbitrażu modeli Flash vs Pro.

---

## 1. Profil Narzędzia

- **Twórca**: Google DeepMind.
- **Kluczowe mechanizmy**:
  - `invoke_subagent`: Asynchroniczne uruchamianie subagentów z własnym oknem kontekstowym.
  - `run_workflow`: Uruchamianie skryptów orkiestracyjnych w czystym Pythonie (kroki `agent`, `parallel`, `pipeline`, `phase`).
  - `swarm`: Koordynacja roju agentów na wspólnej tablicy zadań.
  - `skills`: Modularne pakiety wiedzy i narzędzi (`SKILL.md`).

---

## 2. Kluczowe Zasady Efektywności w Antigravity

### A. Arbitraż Modeli (Flash vs Pro)
Antigravity pozwala na przypisanie modelu per-subagent:
- **`flash` / `flash_lite`**: Zlecasz research, skanowanie repozytorium, przeglądanie dokumentacji i odpytywanie logów. Koszt jest symboliczny, a prędkość natychmiastowa.
- **`pro` / `inherit`**: Zlecasz architekturę, audyt bezpieczeństwa i finalne scalanie kodu.

### B. Reaktywny Model Zdarzeń (Zero Polling)
W Antigravity agenty nie muszą odpytywać środowiska w pętli `while True`:
- Po zleceniu zadania subagentowi lub procesowi tła, agent główny natychmiast kończy turę.
- System automatycznie wznawia agenta, gdy zadanie zakończy się sukcesem lub nadejdzie powiadomienie.

### C. Wymóg Wsadowości (Batching)
Każda tura wysyła całą dotychczasową historię. Dlatego Antigravity nakazuje:
- Wykonywanie wszystkich niezależnych odczytów i edycji **równolegle w jednej turze**.
- Łączenie poleceń powłoki za pomocą `&&` i `;` zamiast pojedynczych wywołań.

---

## 3. Kiedy Używać
- Zadania badawcze i analityczne wymagające przeczesania wielu źródeł (np. research rynkowy, analiza zależności).
- Złożone migracje kodu wymagające równoległego uruchomienia N agentów na różnych katalogach (`run_workflow`).
- Zarządzanie skomplikowanymi projektami przy pomocy interaktywnego roju (`swarm`).

## 4. Kiedy NIE Używać
- Prosta poprawka pojedynczej literówki w pliku (do tego wystarczy lokalny edytor lub szybki prompt).
- Pozostawianie aktywnych zbędnych narzędzi MCP w konfiguracji.
