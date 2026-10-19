"""Three-class EMPO habitat used as the model target."""

HABITATS = (
    "free-living saline",
    "free-living non-saline",
    "host-associated",
)

_NON_SALINE = {"non-saline", "nonsaline", "non saline"}


def habitat_from_empo(empo_1: object, empo_2: object) -> str | None:
    """Map EMPO level 1 and level 2 onto the three habitats.

    Host-associated samples stay one class whether the host is an animal or a
    plant. Free-living samples split on saline versus non-saline. Controls and
    unlabeled rows return None and are left out of the table.
    """
    if empo_1 is None:
        return None
    primary = str(empo_1).strip().lower()
    if primary in {"", "nan", "none", "control"}:
        return None
    secondary = "" if empo_2 is None else str(empo_2).strip().lower()
    if secondary in {"nan", "none"}:
        secondary = ""
    if primary == "host-associated":
        return "host-associated"
    if primary == "free-living" and secondary == "saline":
        return "free-living saline"
    if primary == "free-living" and secondary in _NON_SALINE:
        return "free-living non-saline"
    return None
