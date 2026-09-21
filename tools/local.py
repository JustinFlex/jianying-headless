#!/usr/bin/env python3
"""Use the locally installed, upstream-compatible Jianying toolchain.

This launcher leaves the engine, source pins and system xcode-select unchanged.
Draft operations go through the project's pinned entrypoint.
"""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
ENTRY = ROOT / 'skills/yichen-jianying-edit/scripts/headless_draft.py'


def local_environment():
    env = dict(os.environ)
    env['JIANYING_HEADLESS_ROOT'] = str(ROOT)
    developer = Path.home() / '.local/share/jianying-headless/toolchains/26.5/CommandLineTools'
    if not env.get('DEVELOPER_DIR') and developer.is_dir():
        env['DEVELOPER_DIR'] = str(developer)
    env['PATH'] = str(Path.home() / '.local/bin') + os.pathsep + env.get('PATH', os.defpath)
    return env


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv) or ['doctor']
    utilities = {
        'build-codec': ROOT / 'tools/build_native_codec.py',
        'smoke-test': ROOT / 'tools/smoke_test.py',
        'source-check': ROOT / 'tools/check_package.py',
    }
    if args[0] in utilities:
        script = utilities[args.pop(0)]
    else:
        script = ENTRY
    return subprocess.run([sys.executable, str(script), *args],
                          cwd=ROOT, env=local_environment()).returncode


if __name__ == '__main__':
    raise SystemExit(main())
