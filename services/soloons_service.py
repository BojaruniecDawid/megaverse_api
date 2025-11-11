from core.base_request import BaseRequest


class SoloonsService:
    def __init__(self):
        self.client = BaseRequest()
        self.endpoint = "soloons"

    def create_soloon(self, row: int, column: int, color: str):
        if color.lower() not in {"blue", "red", "purple", "white"}:
            raise ValueError(f"Invalid color: {color}")
        data = {"row": row, "column": column, "color": color.lower()}
        return self.client.post(self.endpoint, data)

    def delete_soloon(self, row: int, column: int):
        data = {"row": row, "column": column}
        return self.client.delete(self.endpoint, data)