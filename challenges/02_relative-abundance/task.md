# 02 Relative abundance

Convert non-negative counts into proportions that sum to 1.

- A list returns a list in the same order.
- A mapping returns a mapping with the same keys.
- A zero count stays zero.
- Raise `ValueError` for an empty vector, a negative count, a non-numeric value, or a total of zero.

```python
relative_abundance([2, 2, 0])
# [0.5, 0.5, 0.0]
relative_abundance({"Firmicutes": 1, "Proteobacteria": 3})
# {"Firmicutes": 0.25, "Proteobacteria": 0.75}
```

The model is a random forest on these proportions, not on raw read counts. Sequencing depth differs across EMP samples, and relative abundance puts them on one scale.

```bash
USE_HIDDEN_SOLUTIONS=0 pytest challenges/02_relative-abundance
```
