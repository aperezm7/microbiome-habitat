# Complete the functions below, do not change the signatures.

def shannon_diversity(counts):
    """Shannon diversity of a count vector, natural log."""
    # Compute Shannon diversity from a count vector. Normalize the counts
    # yourself.
    # H = -sum(p * ln(p)) for each proportion p > 0. Use the natural log.
    # A zero count drops out, because p ln(p) goes to 0 as p goes to 0.
    # One taxon scores 0. An all-zero vector raises ValueError.
    # Example:
    #   shannon_diversity([10, 0, 0]) returns 0.0
    #   shannon_diversity([1, 1]) returns ln(2)
    raise NotImplementedError("shannon_diversity")
