---
title: "Serwery MCP (Model Context Protocol) i Zarządzanie Narzutem"
description: "Serwery MCP (Model Context Protocol) i Zarządzanie Narzutem"
---

Kompleksowy przewodnik po konfiguracji serwerów Model Context Protocol (MCP) z zachowaniem ścisłej dyscypliny budżetu tokenowego.

---

## 1. Ukryty Koszt Protokołu MCP

Model Context Protocol (MCP) to potężny standard umożliwiający podłączanie zewnętrznych źródeł danych i narzędzi (bazy SQL, przeglądarka headless, GitHub, system plików, API finansowe).

Jednak z punktu widzenia LLM każde zarejestrowane narzędzie MCP oznacza:
1. **JSON Schema w każdej turze**:
   Każda funkcja serwera MCP posiada schemat opisujący nazwę, parametry, typy i opisy. Rozbudowane serwery potrafią definiować wiele narzędzi naraz; ich liczbę sprawdź w swoim harnessie.
2. **Zużycie tokenów**:
   Rozmiar definicji zależy od schematu i opisu. Przy wielu serwerach ładowanych w całości stały narzut może sięgać tysięcy tokenów — zmierz go w widoku kontekstu. Harnessy z ładowaniem na żądanie zmniejszają ten koszt.
3. **Konflikt z Prompt Caching**:
   Jeśli konfiguracja MCP zmienia się dynamicznie w trakcie sesji, część prompt cache od miejsca zmiany może zostać unieważniona.

---

## 2. Co Zmierzono (Cursor, 2026)

[Cursor: Improved token efficiency](https://cursor.com/blog/improved-token-efficiency): **dynamiczne (na żądanie) ładowanie narzędzi MCP** zmniejszyło łączną liczbę tokenów o **46,9% w sesjach, które wywołały narzędzie MCP**. Mechanizm opisuje też [Dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery).

To **nie jest** pomiar wyłączania serwerów. Wcześniejsza wersja przypisywała tę liczbę wyłączaniu serwerów i dodawała „ponad 35%” mniej błędów wyboru narzędzi; dla tej drugiej liczby nie ma źródła, więc ją usunięto. Wyłączanie zbędnych serwerów pozostaje rozsądnym zaleceniem autorskim.

---

## 3. Strategia Profilowania MCP

Podziel konfigurację serwerów MCP na profile domenowe (np. w plikach konfiguracyjnych lub skryptach przełączających):

### Profil 1: Core Coding (proponowany domyślny)
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
*Narzut*: zmierz w swoim harnessie.

### Profil 2: E2E & Browser Testing (Tylko podczas pisania/debugowania testów przeglądarkowych)
- Dodaje: `playwright-mcp` lub `puppeteer-mcp`.
- Wyłączany natychmiast po ukończeniu scenariuszy testowych.

### Profil 3: Data & SQL Engineering (Tylko podczas migracji schematów baz danych)
- Dodaje: `postgres-mcp` lub `sqlite-mcp`.

---

## 4. Zasady Bezpieczeństwa i Higieny MCP

1. **ReadOnly z założenia**: Jeśli serwer MCP służy do pobierania wiedzy (np. dokumentacja, research, API rynkowe), konfiguruj go w trybie tylko do odczytu (`readonly`), aby zapobiec przypadkowym mutacjom środowiska produkcyjnego.
2. **Krótki output w narzędziach**: Dostosuj serwery MCP tak, aby ich odpowiedzi zwracały zwięzłe podsumowania lub ograniczały paginację (np. `limit: 10`), a nie surowe zrzuty 10 000 wierszy JSON.
3. **Audyt JSON Schema**: Usuwaj nadmiarowe, rozwlekłe opisy z definicji narzędzi we własnych serwerach MCP. Zwięzły opis argumentu (`"id użytkownika"`) często wystarcza i kosztuje mniej; sprawdź, czy model nadal poprawnie wywołuje narzędzie.
