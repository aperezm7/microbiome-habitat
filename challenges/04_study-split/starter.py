# Complete the functions below, do not change the signatures.

def split_by_study(study_ids, test_size=0.25, seed=0):
    """Return (train_indices, test_indices) with no study on both sides."""
    # Split sample indices so a study is not in both train and test.
    # 1. Cast every study id to a string.
    # 2. Group indices by study, in input order.
    # 3. Raise ValueError if there are fewer than two distinct studies.
    # 4. Raise ValueError unless 0 < test_size < 1.
    # 5. Sort the study ids lexicographically, then shuffle them with the
    #    generator below.
    # 6. Let n be the number of samples and
    #    target = max(1, int(round(n * test_size))) using Python's round.
    # 7. Walk the shuffled studies and add a whole study to the test set
    #    until the test sample count is at least target. Always leave at
    #    least one study in train. Always put at least one study in test.
    # 8. Return (train_indices, test_indices), each sorted ascending.
    # Generator, so two implementations can match without sharing a random
    # stream from NumPy:
    #   state = seed mod 2**32
    #   next: state = (1664525 * state + 1013904223) mod 2**32
    #         return state / 2**32
    # Fisher-Yates, from the last index down to 1: swap i with
    # j = int(random() * (i + 1)).
    # Golden example:
    #   split_by_study(["b", "a", "b", "c", "a"], test_size=0.4, seed=0)
    #   returns ([1, 3, 4], [0, 2])
    raise NotImplementedError("split_by_study")
