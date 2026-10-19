"""Keep every sample from a study on one side of the split."""

EXPLANATION = """
Samples from one study share a lab, a protocol, and a site. If those rows are
in both train and test, the accuracy is partly 'which study is this?'. This
split assigns every sample from a study to one side. Study ids are sorted, then
shuffled with a fixed linear congruential generator so the split repeats.
""".strip()

_MOD = 2**32
_MULT = 1664525
_INC = 1013904223


def _rng(seed: int):
    state = int(seed) % _MOD

    def random() -> float:
        nonlocal state
        state = (_MULT * state + _INC) % _MOD
        return state / _MOD

    return random


def _shuffle(items: list[str], seed: int) -> list[str]:
    random = _rng(seed)
    ordered = list(items)
    for i in range(len(ordered) - 1, 0, -1):
        j = int(random() * (i + 1))
        ordered[i], ordered[j] = ordered[j], ordered[i]
    return ordered


def split_by_study(study_ids, test_size=0.25, seed=0):
    if not 0 < float(test_size) < 1:
        raise ValueError("test_size must be between 0 and 1")
    labels = [str(study) for study in study_ids]
    if not labels:
        raise ValueError("study_ids must not be empty")
    groups: dict[str, list[int]] = {}
    for index, study in enumerate(labels):
        groups.setdefault(study, []).append(index)
    if len(groups) < 2:
        raise ValueError("need at least two studies to split")
    shuffled = _shuffle(sorted(groups), int(seed))
    target = max(1, int(round(len(labels) * float(test_size))))
    test_studies: list[str] = []
    test_count = 0
    for study in shuffled:
        studies_left_for_train = len(shuffled) - len(test_studies) - 1
        if studies_left_for_train == 0:
            break
        if test_studies and test_count >= target:
            break
        test_studies.append(study)
        test_count += len(groups[study])
        if test_count >= target:
            break
    held_out = set(test_studies)
    if not held_out or held_out == set(groups):
        raise ValueError("split left one side empty")
    test_index = sorted(index for index, study in enumerate(labels) if study in held_out)
    train_index = sorted(index for index, study in enumerate(labels) if study not in held_out)
    return train_index, test_index
