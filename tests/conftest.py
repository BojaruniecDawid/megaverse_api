import pytest
from services.polyanets_service import PolyanetsService
from services.soloons_service import SoloonsService
from services.comeths_service import ComethsService

@pytest.fixture
def polyanets_service():
    return PolyanetsService()

@pytest.fixture
def soloons_service():
    return SoloonsService()

@pytest.fixture
def comeths_service():
    return ComethsService()