"""Testy skryptów. Uruchom: python3 -m unittest discover -s scripts"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def run_on(files, command):
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in files.items():
            path = Path(tmp) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        return subprocess.run(command + [tmp], capture_output=True, text=True, check=True)


def repo_map(files):
    return run_on(files, [sys.executable, str(SCRIPTS / 'gen-repo-map.py')])


def audit(files):
    return run_on(files, ['bash', str(SCRIPTS / 'audit-context.sh')]).stdout


def exports_of(source):
    for line in repo_map({'a.ts': source}).stdout.splitlines():
        if line.startswith('  exports: '):
            return set(line.removeprefix('  exports: ').split(', '))
    return set()


class RepoMapTest(unittest.TestCase):
    def test_ignores_exports_in_comments_and_strings(self):
        source = (
            '// export function ghost() {}\n'
            '/* export class Phantom {} */\n'
            'const s = "export class Fake {}";\n'
            "const t = 'export const Quoted = 1';\n"
            'const u = `\nexport function Templated() {}\n`;\n'
            "const url = 'http://example.test'; export const real = 1;\n"
        )
        self.assertEqual(exports_of(source), {'real'})

    def test_const_enum_uses_enum_name(self):
        self.assertEqual(exports_of('export const enum Color { Red }\n'), {'Color'})

    def test_type_only_export_block(self):
        self.assertEqual(
            exports_of('export type { Foo, Bar as Baz } from "./x";\nexport { type Qux };\n'),
            {'Foo', 'Baz', 'Qux'},
        )

    def test_abstract_and_declare(self):
        self.assertEqual(
            exports_of('export abstract class Base {}\nexport declare function load(): void;\n'),
            {'Base', 'load'},
        )

    def test_skips_minified_files(self):
        out = repo_map({'v.min.js': 'export const a = 1;\n'}).stdout
        self.assertNotIn('v.min.js', out)

    def test_reports_unparsable_file_on_stderr(self):
        result = repo_map({'broken.py': 'def (:\n'})
        self.assertIn('broken.py', result.stderr)
        self.assertNotIn('broken.py', result.stdout)

    def test_directories_are_listed_in_sorted_order(self):
        out = repo_map({f'{d}/m.py': 'def f(): pass\n' for d in 'dbeac'}).stdout
        listed = [line for line in out.splitlines() if line.endswith('m.py')]
        self.assertEqual(listed, sorted(listed))


class AuditTest(unittest.TestCase):
    RULE = '---\nalwaysApply: true\n---\njeden dwa trzy\n'

    def test_counts_nested_rules(self):
        self.assertIn('sub/deep.mdc', audit({'.cursor/rules/sub/deep.mdc': self.RULE}))

    def test_counts_agents_and_claude_files_without_cursor_rules(self):
        out = audit({'AGENTS.md': 'a' * 400, 'CLAUDE.md': 'b' * 400})
        self.assertIn('AGENTS.md', out)
        self.assertIn('CLAUDE.md', out)
        self.assertIn('od ~2 do ~200', out)

    def test_large_budget_warning_does_not_cite_humanlayer(self):
        out = audit({'AGENTS.md': 'slowo ' * 3000})
        self.assertIn('umowny budżet', out)
        self.assertNotIn('HumanLayer', out)


if __name__ == '__main__':
    unittest.main()
