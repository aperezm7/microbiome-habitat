from habitat.labels import habitat_from_empo


def test_three_habitats():
    assert habitat_from_empo("Host-associated", "Animal") == "host-associated"
    assert habitat_from_empo("Host-associated", "Plant") == "host-associated"
    assert habitat_from_empo("Free-living", "Saline") == "free-living saline"
    assert habitat_from_empo("Free-living", "Non-saline") == "free-living non-saline"


def test_controls_are_dropped():
    assert habitat_from_empo("Control", "") is None
    assert habitat_from_empo("", "Saline") is None
    assert habitat_from_empo(None, "Saline") is None
