#!/usr/bin/env python3
"""
gen-repo-map.py — Deterministyczny generator mapy repozytorium bez używania tokenów AI.
Generuje listę nazw dla pasywnego kontekstu agenta (.cursor/REPO-MAP.md):
- Python: publiczne funkcje i klasy najwyższego poziomu (moduł `ast`),
- TypeScript/JavaScript: nazwy eksportów (wyrażenia regularne, to heurystyka, nie parser).
Nie buduje grafu importów i nie wypisuje metod ani sygnatur.
"""

import os
import sys
import re
import ast
from pathlib import Path

IGNORE_DIRS = {
    '.git', 'node_modules', 'dist', 'build', '.next', '.turbo',
    'coverage', '.venv', 'venv', '__pycache__', '.idea', '.vscode'
}

IGNORE_SUFFIXES = (
    '.map', '.min.js', '.min.css', '.png', '.jpg', '.jpeg', '.svg',
    '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz', '.lock'
)

# Komentarze i napisy w TS/JS. Napisy w ' i " nie przechodzą przez koniec linii,
# więc samotny apostrof (np. w JSX) nie pochłonie reszty pliku.
TS_NOISE = re.compile(
    r'''//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|`(?:\\.|[^`\\])*`''',
    re.DOTALL,
)

def should_ignore(rel_path: Path) -> bool:
    for part in rel_path.parts:
        if part in IGNORE_DIRS or (part.startswith('.') and part != '.'):
            return True
    if rel_path.name.lower().endswith(IGNORE_SUFFIXES):
        return True
    if 'generated' in rel_path.name.lower():
        return True
    return False

def parse_python_file(path: Path):
    exports = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(path))
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith('_'):
                    exports.append(f"def {node.name}()")
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith('_'):
                    exports.append(f"class {node.name}")
    except (OSError, SyntaxError, ValueError) as error:
        print(f"Ostrzeżenie: pominięto {path}: {error}", file=sys.stderr)
    return exports

def parse_ts_js_file(path: Path):
    exports = []
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = TS_NOISE.sub(' ', f.read())
        
        # Regex for standard and default exports
        patterns = [
            r'export\s+(?:async\s+)?function\s+([a-zA-Z0-9_$]+)',
            r'export\s+default\s+(?:async\s+)?function\s+([a-zA-Z0-9_$]+)',
            r'export\s+(?:declare\s+)?(?:abstract\s+)?class\s+([a-zA-Z0-9_$]+)',
            r'export\s+declare\s+(?:async\s+)?function\s+([a-zA-Z0-9_$]+)',
            r'export\s+default\s+class\s+([a-zA-Z0-9_$]+)',
            r'export\s+(?:declare\s+)?(?:const|let|var)\s+(?!enum\b)([a-zA-Z0-9_$]+)',
            r'export\s+interface\s+([a-zA-Z0-9_$]+)',
            r'export\s+type\s+([a-zA-Z0-9_$]+)',
            r'export\s+(?:declare\s+)?(?:const\s+)?enum\s+([a-zA-Z0-9_$]+)',
        ]
        for p in patterns:
            for match in re.finditer(p, content):
                exports.append(match.group(1))

        # Handle export { a, b, c as d }
        block_pattern = r'export(?:\s+type)?\s*\{([^}]+)\}'
        for match in re.finditer(block_pattern, content):
            items = match.group(1).split(',')
            for item in items:
                item = item.strip()
                if not item:
                    continue
                parts = item.split()
                if len(parts) > 1 and parts[0] == 'type' and parts[1] != 'as':
                    parts = parts[1:]
                if 'as' in parts:
                    as_idx = parts.index('as')
                    if as_idx + 1 < len(parts):
                        exports.append(parts[as_idx + 1])
                elif parts:
                    exports.append(parts[0])
    except OSError as error:
        print(f"Ostrzeżenie: pominięto {path}: {error}", file=sys.stderr)
    return sorted(list(set(exports)))

def print_help():
    print("""Użycie: python3 scripts/gen-repo-map.py [KATALOG_PROJEKTU]

Generuje listę symboli Pythona (ast) i eksportów TS/JS (regex).
Wynik można umieścić w .cursor/REPO-MAP.md.

Argumenty:
  KATALOG_PROJEKTU    Ścieżka do katalogu głównego projektu (domyślnie: bieżący katalog)
  -h, --help          Wyświetla tę pomoc i kończy działanie
""")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print_help()
        sys.exit(0)

    target_arg = sys.argv[1] if len(sys.argv) > 1 else "."
    root_dir = Path(target_arg).resolve()

    if not root_dir.exists() or not root_dir.is_dir():
        print(f"Błąd: Ścieżka '{target_arg}' nie istnieje lub nie jest katalogiem.", file=sys.stderr)
        sys.exit(1)

    print(f"# REPO-MAP: {root_dir.name}")
    print("# Auto-generated deterministic symbol index. Do not edit manually.\n")

    files_found = 0
    for root, dirs, files in os.walk(root_dir):
        # Filter directories in-place (relative filtering)
        dirs[:] = sorted(
            d for d in dirs
            if d not in IGNORE_DIRS and not (d.startswith('.') and d != '.')
        )
        for file in sorted(files):
            file_path = Path(root) / file
            rel_path = file_path.relative_to(root_dir)

            if should_ignore(rel_path):
                continue

            ext = file_path.suffix.lower()
            symbols = []
            if ext == '.py':
                symbols = parse_python_file(file_path)
            elif ext in ('.ts', '.tsx', '.js', '.jsx'):
                symbols = parse_ts_js_file(file_path)

            if symbols:
                files_found += 1
                symbol_str = ", ".join(symbols[:12])
                if len(symbols) > 12:
                    symbol_str += f" (+{len(symbols) - 12} more)"
                print(f"{rel_path}")
                print(f"  exports: {symbol_str}")

    print(f"\n# Total indexed modules: {files_found}")

if __name__ == '__main__':
    main()
