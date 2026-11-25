#!/usr/bin/env python3
"""
gen-repo-map.py — Deterministyczny generator mapy repozytorium bez używania tokenów AI.
Skanuje pliki źródłowe (Python, TypeScript, JavaScript) i generuje zwięzłą mapę symboli
oraz eksportów, idealną do pasywnego kontekstu agenta (.cursor/REPO-MAP.md).
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

IGNORE_EXTENSIONS = {
    '.map', '.min.js', '.min.css', '.png', '.jpg', '.jpeg', '.svg',
    '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz', '.lock'
}

def should_ignore(path: Path) -> bool:
    for part in path.parts:
        if part in IGNORE_DIRS or part.startswith('.'):
            if part not in {'.'}:
                return True
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return True
    if 'generated' in path.name.lower():
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
    except Exception:
        pass
    return exports

def parse_ts_js_file(path: Path):
    exports = []
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Regex for export function, export class, export const, export interface, export type
        patterns = [
            r'export\s+(?:async\s+)?function\s+([a-zA-Z0-9_$]+)',
            r'export\s+class\s+([a-zA-Z0-9_$]+)',
            r'export\s+const\s+([a-zA-Z0-9_$]+)',
            r'export\s+interface\s+([a-zA-Z0-9_$]+)',
            r'export\s+type\s+([a-zA-Z0-9_$]+)',
        ]
        for p in patterns:
            for match in re.finditer(p, content):
                exports.append(match.group(1))
    except Exception:
        pass
    return sorted(list(set(exports)))

def main():
    root_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(f"# REPO-MAP: {root_dir.name}")
    print("# Auto-generated deterministic symbol index. Do not edit manually.\n")

    files_found = 0
    for root, dirs, files in os.walk(root_dir):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        for file in sorted(files):
            file_path = Path(root) / file
            if should_ignore(file_path):
                continue

            rel_path = file_path.relative_to(root_dir)
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
