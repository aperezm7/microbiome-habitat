# 05 Balanced accuracy

Compute balanced accuracy from labels and predictions.

It is the unweighted mean of recall for each class that appears in `y_true`. A class the model never predicts scores recall 0 and still counts. Do not weight the mean by how common the class is. That is the point: a model that always predicts the largest EMPO class can look accurate and still score poorly here.

```python
balanced_accuracy(["a", "a", "b", "b"], ["a", "b", "b", "b"])
# 0.75
```

Recall of `a` is 1/2. Recall of `b` is 2/2. The mean is 0.75.

Raise `ValueError` if the two sequences differ in length or if they are empty.

This is the same definition as `sklearn.metrics.balanced_accuracy_score` with `adjusted=False`. The training report uses that score on the study-held-out test set.

```bash
USE_HIDDEN_SOLUTIONS=0 pytest challenges/05_balanced-accuracy
```
