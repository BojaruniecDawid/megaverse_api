from core.base_request import BaseRequest

class ComethsService:
    def __init__(self):
        self.client = BaseRequest()
        self.endpoint = "comeths"

    def create_cometh(self, row: int, column: int, direction: str):
        if direction.lower() not in {"up", "down", "left", "right"}:
            raise ValueError(f"Invalid direction: {direction}")
        data = {"row": row, "column": column, "direction": direction.lower()}
        return self.client.post(self.endpoint, data)

    def delete_cometh(self, row: int, column: int):
        data = {"row": row, "column": column}
        return self.client.delete(self.endpoint, data)