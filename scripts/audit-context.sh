#!/usr/bin/env bash
# audit-context.sh — Szybki audyt budżetu reguł i higieny kontekstu projektu

set -e

PROJECT_DIR="${1:-.}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Błąd: Katalog '$PROJECT_DIR' nie istnieje." >&2
    exit 1
fi
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
echo "=== INSTRUKCJE ZAWSZE ŁADOWANE ==="
echo "(dwa szacunki bez tokenizera: słowa*4/3 i bajty/4; wynik zależy od języka i modelu)"

# Umowny próg ostrzegawczy, nie wynik badań.
BUDGET=2000
TOTAL_WORDS=0
TOTAL_BYTES=0
SEEN=()

add_always_on() {
    local file="$1" label="$2" other words bytes
    for other in "${SEEN[@]}"; do
        # CLAUDE.md bywa dowiązaniem do AGENTS.md: nie licz dwa razy
        if [ "$file" -ef "$other" ]; then return 0; fi
    done
    SEEN+=("$file")
    words=$(( $(wc -w < "$file") ))
    bytes=$(( $(wc -c < "$file") ))
    echo "🔴 [ALWAYS-ON] $label: ~$(( words * 4 / 3 )) / ~$(( bytes / 4 )) tokenów ($words słów, $bytes bajtów)"
    TOTAL_WORDS=$(( TOTAL_WORDS + words ))
    TOTAL_BYTES=$(( TOTAL_BYTES + bytes ))
}

for file in AGENTS.md CLAUDE.md .claude/CLAUDE.md; do
    if [ -f "$file" ]; then add_always_on "$file" "$file"; fi
done

if [ -d ".cursor/rules" ]; then
    while IFS= read -r rule; do
        NAME="${rule#.cursor/rules/}"
        if grep -qiE "^alwaysApply:[[:space:]]*true" "$rule"; then
            add_always_on "$rule" "$NAME"
        else
            GLOBS=$(grep -iE "^globs:" "$rule" || true)
            echo "🟢 [CONDITIONAL] $NAME ($GLOBS): ładowana warunkowo (opis może nadal zajmować kontekst)"
        fi
    done < <(find .cursor/rules -type f -name '*.mdc' | LC_ALL=C sort)
else
    echo "ℹ️  Katalog .cursor/rules/ nie istnieje."
fi

LOW=$(( TOTAL_WORDS * 4 / 3 ))
HIGH=$(( TOTAL_BYTES / 4 ))
if [ "$LOW" -gt "$HIGH" ]; then SWAP=$LOW; LOW=$HIGH; HIGH=$SWAP; fi

echo ""
echo "Łączny stały narzut: od ~$LOW do ~$HIGH tokenów"
if [ "$HIGH" -gt "$BUDGET" ]; then
    echo "🚨 Górny szacunek przekracza umowny budżet $BUDGET tokenów. Sprawdź, co jest potrzebne w każdej sesji."
else
    echo "✅ Mieści się w umownym budżecie $BUDGET tokenów."
fi

echo ""
echo "Nie są liczone: pliki importowane przez @, instrukcje z katalogu domowego i schematy narzędzi MCP."
echo "Audyt zakończony."
