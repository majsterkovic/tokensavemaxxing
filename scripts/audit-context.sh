#!/usr/bin/env bash
# audit-context.sh — Szybki audyt budżetu reguł i higieny kontekstu projektu

set -e

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "=== AUDYT KONTEKSTU AGENTOWEGO: $PROJECT_DIR ==="
echo ""

# 1. Sprawdzenie .cursorignore
if [ -f ".cursorignore" ]; then
    LINES=$(wc -l < .cursorignore)
    echo "✅ .cursorignore istnieje ($LINES linii reguł wykluczeń)"
else
    echo "⚠️  BRAK .cursorignore! AI będzie indeksować node_modules / dist!"
fi

# 2. Sprawdzenie .ignore
if [ -f ".ignore" ]; then
    echo "✅ .ignore istnieje (ochrona ripgrep w multi-root)"
else
    echo "ℹ️  Brak .ignore — zalecane w środowiskach multi-root"
fi

# 3. Sprawdzenie REPO-MAP.md
if [ -f ".cursor/REPO-MAP.md" ] || [ -f "REPO-MAP.md" ]; then
    echo "✅ REPO-MAP.md istnieje"
else
    echo "ℹ️  Brak REPO-MAP.md. Wygeneruj przez: python3 scripts/gen-repo-map.py ."
fi

echo ""
echo "=== ANALIZA REGUŁ .cursor/rules/ ==="

TOTAL_ALWAYS_WORDS=0
if [ -d ".cursor/rules" ]; then
    for rule in .cursor/rules/*.mdc; do
        if [ -f "$rule" ]; then
            NAME=$(basename "$rule")
            WORDS=$(wc -w < "$rule")
            # Proste oszacowanie: 1 słowo ~= 1.33 tokena
            TOKENS=$(( WORDS * 4 / 3 ))
            
            IS_ALWAYS=$(grep -i "alwaysApply:\s*true" "$rule" || true)
            if [ -n "$IS_ALWAYS" ]; then
                echo "🔴 [ALWAYS-ON] $NAME: ~$TOKENS tokenów ($WORDS słów)"
                TOTAL_ALWAYS_WORDS=$(( TOTAL_ALWAYS_WORDS + WORDS ))
            else
                GLOBS=$(grep -i "globs:" "$rule" || true)
                echo "🟢 [CONDITIONAL] $NAME ($GLOBS): ~$TOKENS tokenów (koszt startowy: 0)"
            fi
        fi
    done
    
    TOTAL_ALWAYS_TOKENS=$(( TOTAL_ALWAYS_WORDS * 4 / 3 ))
    echo ""
    echo "Łączny stały narzut Always-On reguł: ~$TOTAL_ALWAYS_TOKENS tokenów"
    if [ "$TOTAL_ALWAYS_TOKENS" -gt 2000 ]; then
        echo "🚨 ALARM: Przekroczono bezpieczny limit 2000 tokenów dla reguł Always-On!"
        echo "   Jakość wykonywania instrukcji ulegnie mierzalnej degradacji (HumanLayer)."
    else
        echo "✅ Budżet reguł Always-On w normie (< 2000 tokenów)."
    fi
else
    echo "ℹ️  Katalog .cursor/rules/ nie istnieje."
fi

echo ""
echo "Audyt zakończony."
