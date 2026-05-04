#!/usr/bin/env python
"""Provides simple way to run formatter/linter/static analysis/tests on the project."""

import sys
from subprocess import CalledProcessError, check_call
from pathlib import Path

def do_process(args: list[str], cwd: str = ".") -> bool:
    """Run program provided by args.

    Returns ``True`` upon success.

    Output failed message on non-zero exit and return False.

    Exit if command is not found.

    """
    print(f"Running: {' '.join(args)}")
    try:
        check_call(args, shell=False, cwd=cwd)
    except CalledProcessError:
        print(f"\nFailed: {' '.join(args)}")
        return False
    except Exception as exc:
        print(f"{exc!s}\n", file=sys.stderr)
        raise SystemExit(1) from exc
    return True


def run_static_and_lint() -> bool:
    """Runs the static analysis and linting.

    :returns: False if everything ran correctly. Otherwise, it will return True

    """
    success = True
    success &= do_process(["ruff", "format", "home/.chezmoiscripts/"])
    success &= do_process(["docstrfmt", "home/.chezmoiscripts/*.py", "-v"])
    return success


def main() -> int:
    """Runs the main function."""
    success = True
    try:
        success &= run_static_and_lint()
    except KeyboardInterrupt:
        return int(not False)
    return int(not success)


if __name__ == "__main__":
    exit_code = main()
    print("\npre_push.py: Success!" if not exit_code else "\npre_push.py: Fail")
    sys.exit(exit_code)
