"""``python -m challenges reveal 03`` prints that solution and a short explanation."""

import sys
from pathlib import Path

from challenges.catalog import resolve_slug

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2 or args[0] != "reveal":
        print("usage: python -m challenges reveal 03", file=sys.stderr)
        return 2
    try:
        slug = resolve_slug(args[1])
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    path = ROOT / "challenges" / "hidden" / f"{slug}.py"
    source = path.read_text()
    namespace: dict = {}
    exec(compile(source, str(path), "exec"), namespace)
    explanation = namespace.get("EXPLANATION", "").strip()
    if explanation:
        print(explanation)
        print("---")
    print(source, end="" if source.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
