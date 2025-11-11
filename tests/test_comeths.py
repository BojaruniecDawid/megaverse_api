import pytest


@pytest.mark.parametrize("direction", ["up", "down", "left", "right"])
def test_create_and_delete_cometh(comeths_service, direction):
    row, col = 3, 3

    # Create Cometh
    resp = comeths_service.create_cometh(row, col, direction)
    assert resp is not None

    # Delete Cometh
    status = comeths_service.delete_cometh(row, col)
    assert status == 200