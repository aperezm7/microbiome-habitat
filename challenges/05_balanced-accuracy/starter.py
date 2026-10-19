# Complete the functions below, do not change the signatures.

def balanced_accuracy(y_true, y_pred) -> float:
    """Unweighted mean of per-class recall."""
    # Compute balanced accuracy from labels and predictions.
    # It is the unweighted mean of recall for each class that appears in
    # y_true. A class the model never predicts scores recall 0 and still
    # counts. Do not weight the mean by how common the class is.
    # Raise ValueError if the two sequences differ in length or if they are
    # empty.
    # Example:
    #   balanced_accuracy(["a", "a", "b", "b"], ["a", "b", "b", "b"])
    #   returns 0.75
    # Recall of a is 1/2. Recall of b is 2/2. The mean is 0.75.
    # This is the same definition as sklearn.metrics.balanced_accuracy_score
    # with adjusted=False.
    raise NotImplementedError("balanced_accuracy")
