"""Unweighted mean of per-class recall."""

EXPLANATION = """
Balanced accuracy is the unweighted mean of per-class recall. Only classes
present in y_true are averaged. A model that always predicts the common habitat
can have high ordinary accuracy and a low balanced accuracy, because the rare
class contributes the same as the common one. The test-set report uses this score.
""".strip()


def balanced_accuracy(y_true, y_pred) -> float:
    truth = list(y_true)
    pred = list(y_pred)
    if len(truth) != len(pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not truth:
        raise ValueError("y_true must not be empty")
    labels = sorted(set(truth), key=str)
    recalls: list[float] = []
    for label in labels:
        index = [i for i, value in enumerate(truth) if value == label]
        hits = sum(1 for i in index if pred[i] == label)
        recalls.append(hits / len(index))
    return sum(recalls) / len(recalls)
