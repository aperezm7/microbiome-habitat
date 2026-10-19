"""Load either a starter or the hidden solution. Starters never import hidden."""

import importlib.util
import os
from pathlib import Path

from challenges.catalog import resolve_slug

ROOT = Path(__file__).resolve().parents[1]


def use_hidden() -> bool:
    return os.environ.get("USE_HIDDEN_SOLUTIONS", "1") != "0"


def implementation_path(slug: str) -> Path:
    if use_hidden():
        return ROOT / "challenges" / "hidden" / f"{slug}.py"
    return ROOT / "challenges" / slug / "starter.py"


def load(key: str):
    slug = resolve_slug(key)
    path = implementation_path(slug)
    module_name = "challenge_" + slug.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
