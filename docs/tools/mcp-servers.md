---
title: "Serwery MCP (Model Context Protocol) i Zarządzanie Narzutem"
description: "Serwery MCP (Model Context Protocol) i Zarządzanie Narzutem"
---


# Serwery MCP (Model Context Protocol) i Zarządzanie Narzutem

Kompleksowy przewodnik po konfiguracji serwerów Model Context Protocol (MCP) z zachowaniem ścisłej dyscypliny budżetu tokenowego.

---

## 1. Ukryty Koszt Protokołu MCP

Model Context Protocol (MCP) to potężny standard umożliwiający podłączanie zewnętrznych źródeł danych i narzędzi (bazy SQL, przeglądarka headless, GitHub, system plików, API finansowe).

Jednak z punktu widzenia LLM każde zarejestrowane narzędzie MCP oznacza:
1. **JSON Schema w każdej turze**:
   Każda funkcja serwera MCP posiada schemat opisujący nazwę, parametry, typy i opisy. Złożony serwer (np. GitHub MCP lub Playwright MCP) potrafi definiować 20-40 narzędzi.
2. **Zużycie tokenów**:
   Średnio jedna definicja narzędzia to 150-300 tokenów. Zestaw 5 serwerów MCP potrafi wstrzykiwać **5 000 - 12 000 tokenów definicji do każdego pojedynczego zapytania**!
3. **Konflikt z Prompt Caching**:
   Jeśli konfiguracja MCP zmienia się dynamicznie w trakcie sesji, cały prefiks Prompt Cache zostaje zniszczony, powodując pełne przeliczenie kosztu tury po stawkach bez cache.

---

## 2. Pomiary Empiryczne (Cursor Engineering, 2026)

- **Do −46.9% tokenów w sesji**: Wyłączenie serwerów MCP, które nie są niezbędne do aktualnie wykonywanego zadania, przynosi natychmiastową redukcję zużycia tokenów niemal o połowę.
- **Wzrost precyzji wyboru narzędzi**: Gdy agent ma do wyboru 8 narzędzi zamiast 60, prawdopodobieństwo halucynacji lub błędnego doboru parametrów spada o ponad 35%.

---

## 3. Strategia Profilowania MCP

Podziel konfigurację serwerów MCP na profile domenowe (np. w plikach konfiguracyjnych lub skryptach przełączających):

### Profil 1: Core Coding (Domyślny dla 90% zadań programistycznych)
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    }
  }
}
```
*Narzut*: ~400 tokenów.

### Profil 2: E2E & Browser Testing (Tylko podczas pisania/debugowania testów przeglądarkowych)
- Dodaje: `playwright-mcp` lub `puppeteer-mcp`.
- Wyłączany natychmiast po ukończeniu scenariuszy testowych.

### Profil 3: Data & SQL Engineering (Tylko podczas migracji schematów baz danych)
- Dodaje: `postgres-mcp` lub `sqlite-mcp`.

---

## 4. Zasady Bezpieczeństwa i Higieny MCP

1. **ReadOnly z założenia**: Jeśli serwer MCP służy do pobierania wiedzy (np. dokumentacja, research, API rynkowe), konfiguruj go w trybie tylko do odczytu (`readonly`), aby zapobiec przypadkowym mutacjom środowiska produkcyjnego.
2. **Krótki output w narzędziach**: Dostosuj serwery MCP tak, aby ich odpowiedzi zwracały zwięzłe podsumowania lub ograniczały paginację (np. `limit: 10`), a nie surowe zrzuty 10 000 wierszy JSON.
3. **Audyt JSON Schema**: Usuwaj nadmiarowe, rozwlekłe opisy z definicji narzędzi we własnych serwerach MCP. Zwięzły opis argumentu (`"id użytkownika"`) działa równie dobrze jak 3 akapity prozy, zużywając 5× mniej tokenów.
