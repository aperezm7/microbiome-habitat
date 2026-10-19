"""Balanced accuracy without calling into scikit-learn."""


def balanced_accuracy(y_true: list[object], y_pred: list[object]) -> float:
    """Unweighted mean of per-class recall.

    Only labels that appear in ``y_true`` are included. A class the model
    never predicts contributes a recall of 0. This matches
    ``sklearn.metrics.balanced_accuracy_score`` with ``adjusted=False``.
    """
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
