# Complete the functions below, do not change the signatures.

def relative_abundance(counts):
    """Convert a count vector or mapping to proportions that sum to 1."""
    # Convert non-negative counts into proportions that sum to 1.
    # A list returns a list in the same order.
    # A mapping returns a mapping with the same keys.
    # A zero count stays zero.
    # Raise ValueError for an empty vector, a negative count, a non-numeric
    # value, or a total of zero.
    # Example:
    #   relative_abundance([2, 2, 0]) returns [0.5, 0.5, 0.0]
    #   relative_abundance({"Firmicutes": 1, "Proteobacteria": 3})
    #   returns {"Firmicutes": 0.25, "Proteobacteria": 0.75}
    raise NotImplementedError("relative_abundance")
