# Notatka Narzędziowa: OpenBot

> **Rola w ekosystemie**: Otwarta, lokalna platforma robocza (Agent Workspace) do koordynowania autonomicznych agentów w izolowanych środowiskach (sandboxes).

---

## 1. Profil Narzędzia

- **Typ**: Local-first / Self-hosted Agent Platform.
- **Kluczowa idea**: Przełącznik (Switchboard) i przestrzeń robocza dla zespołów agentów AI wykonujących równolegle zadania z przypisanymi rolami.
- **Wspierane protokoły**: Integracja z Claude Code, Codex, Gemini, Grok oraz frameworkami LangChain i protokołem AG-UI.

---

## 2. Główne Mechanizmy

1. **Izolowane Piaskownice (Sandboxed Execution)**:
   - Każdy uruchomiony agent w OpenBot działa w dedykowanym, odizolowanym środowisku z kontrolowanym dostępem do systemu plików i sieci.
   - Zapobiega to przypadkowym mutacjom systemu operacyjnego gospodarza.
2. **Persistent Teammates**:
   - Agenci posiadają trwałą tożsamość, stan i historię zadań, co pozwala na delegowanie im długoterminowych ról (np. "automatyczny tester regresji" czy "researcher dokumentacji").
3. **Wielodostawczość**:
   - Możliwość przypisania różnych modeli do różnych ról w zespole (np. model lokalny Ollama do wstępnego filtrowania, Claude Sonnet do kodu).

---

## 3. Zastosowanie w tokensavemaxxing

- OpenBot może działać jako lokalny zarządca piaskownic dla zadań wymagających wykonania niebezpiecznego kodu.
- Pozwala na bezpłatną orkiestrację agentów opartych o modele lokalne (Ollama / Inkling 2 Mini / Qwen 2.5 Coder) bez narzutu komercyjnych platform chmurowych.
