SLUGS = (
    "01_read-fasta",
    "02_relative-abundance",
    "03_shannon-diversity",
    "04_study-split",
    "05_balanced-accuracy",
)


def resolve_slug(key: str) -> str:
    text = key.strip()
    if text in SLUGS:
        return text
    if text.isdigit():
        prefix = f"{int(text):02d}_"
        matches = [slug for slug in SLUGS if slug.startswith(prefix)]
        if len(matches) == 1:
            return matches[0]
    raise KeyError(f"unknown challenge {key}")
