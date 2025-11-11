import pytest
from builders.shapes_builder import ShapeBuilder

def test_x_shape_coordinates():
    builder = ShapeBuilder()
    coords = builder.x_shape(start_row=3, start_col=3, size=7)

    # Check center point
    assert (6, 6) in coords

    # Check corners
    assert (3, 3) in coords
    assert (9, 9) in coords
    assert (3, 9) in coords
    assert (9, 3) in coords

    # Ensure no duplicates
    assert len(coords) == len(set(coords))