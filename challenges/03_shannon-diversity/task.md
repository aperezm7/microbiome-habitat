# 03 Shannon diversity

Compute Shannon diversity from a **count** vector. Normalize the counts yourself.

```text
H = -sum(p * ln(p))
```

for each proportion `p > 0`. Use the natural log. A zero count drops out, because `p ln(p)` goes to 0 as `p` goes to 0. One taxon scores 0. An all-zero vector raises `ValueError`.

```python
shannon_diversity([10, 0, 0])  # 0.0
shannon_diversity([1, 1])      # ln(2)
```

This number is not a feature in the habitat model. The forest sees the whole phylum profile. Shannon is here because it is the usual one-number summary of that profile.

```bash
USE_HIDDEN_SOLUTIONS=0 pytest challenges/03_shannon-diversity
python -m challenges reveal 03
```
