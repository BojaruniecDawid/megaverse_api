import requests
from core.config import Config


class BaseRequest:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.candidate_id = Config.CANDIDATE_ID

    def post(self, endpoint: str, data: dict):
        data["candidateId"] = self.candidate_id
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        self._check_response(response)
        return response.json() if response.text else {}

    def delete(self, endpoint: str, data: dict):
        data["candidateId"] = self.candidate_id
        response = requests.delete(f"{self.base_url}/{endpoint}", json=data)
        self._check_response(response)
        return response.status_code

    @staticmethod
    def _check_response(response):
        if not response.ok:
            raise Exception(f"API Error {response.status_code}: {response.text}")