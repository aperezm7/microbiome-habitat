"""Stream the mapping file and the subset BIOM into a local cache directory."""

import hashlib
from pathlib import Path

import httpx

from services.data.sources import BIOM_URL, MAPPING_MD5, MAPPING_URL

USER_AGENT = "microbiome-habitat/0.1 (research; phylum habitat model)"


def download_file(url: str, dest: Path, timeout: float = 300.0) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_suffix(dest.suffix + ".partial")
    headers = {"User-Agent": USER_AGENT}
    with httpx.stream("GET", url, headers=headers, follow_redirects=True, timeout=timeout) as response:
        response.raise_for_status()
        with partial.open("wb") as handle:
            for chunk in response.iter_bytes():
                handle.write(chunk)
    partial.replace(dest)
    return dest


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_emp_downloads(cache_dir: Path) -> tuple[Path, Path]:
    """Download the 2k mapping and the matching subset BIOM if they are not cached.

    Files land in ``cache_dir/downloads``. Callers cache the collapsed parquet
    and do not commit these downloads.
    """
    folder = cache_dir / "downloads"
    mapping = folder / "emp_qiime_mapping_subset_2k_20170912.tsv"
    biom = folder / "emp_cr_gg_13_8.subset_2k.biom"
    if not mapping.is_file():
        download_file(MAPPING_URL, mapping)
    digest = md5_file(mapping)
    if digest != MAPPING_MD5:
        mapping.unlink(missing_ok=True)
        raise ValueError(f"mapping md5 {digest} does not match {MAPPING_MD5}")
    if not biom.is_file():
        download_file(BIOM_URL, biom)
    if biom.stat().st_size < 1_000_000:
        raise ValueError(f"subset BIOM at {biom} is unexpectedly small")
    return mapping, biom
