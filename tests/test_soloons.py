import pytest


@pytest.mark.parametrize("color", ["blue", "red", "purple", "white"])
def test_create_and_delete_soloon(soloons_service, color):
    row, col = 2, 2

    # Create Soloons
    resp = soloons_service.create_soloon(row, col, color)
    assert resp is not None

    # Delete Soloons
    status = soloons_service.delete_soloon(row, col)
    assert status == 200
