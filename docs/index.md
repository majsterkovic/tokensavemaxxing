---
title: "tokensavemaxxing"
description: "The Agentic Coding & Context Engineering Vault"
template: splash
hero:
  tagline: Maksymalna efektywność kodu agentowego przy minimalnym zużyciu tokenów i zerowym szumie kontekstowym.
  actions:
    - text: Przeglądaj Artykuły i Badania
      link: /tokensavemaxxing/articles/
      icon: right-arrow
      variant: primary
    - text: Katalog Narzędzi
      link: /tokensavemaxxing/tools/
      icon: external
      variant: secondary
    - text: Playbook Tokensavemaxxing
      link: /tokensavemaxxing/playbooks/03-token-savemaxxing/
      variant: minimal
---


## ⚡ 5 Filarów Tokensavemaxxing

| Filar | Działanie | Rezultat |
|---|---|---|
| **1. Warstwa Zerowa (`.cursorignore`)** | Wycięcie generowanego kodu, map źródeł, lockfile'ów, assetów | Indeksowanie 12 min → 4 min; koszt sesji −20% |
| **2. Pasywna Mapa Symboli (`REPO-MAP.md`)** | Deterministyczny graf eksportów i importów przez AST (~2k tok) | Zastępuje setki `read_file`, pass rate skacze do 100% |
| **3. Czystka MCP (Tool Pruning)** | Wyłączenie nieużywanych serwerów protokołu MCP z workspace | Natychmiastowe obcięcie stałego narzutu tury o do **46.9%** |
| **4. Dyscyplina Reguł (`<2000 tok`)** | Przejście z `alwaysApply: true` na reguły z maskami `globs` | Zapobieganie równomiernej degradacji uwagi modelu |
| **5. Subagenty Badawcze (Scouts)** | Tani model (Flash/Haiku) z zakazem cytowania kodu (tylko wniosek + linie) | Redukcja zanieczyszczenia sesji głównej z 6k do <450 tok |
