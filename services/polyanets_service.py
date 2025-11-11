from core.base_request import BaseRequest


class PolyanetsService(BaseRequest):
    def create_polyanet(self, row: int, column: int):
        return self.post("polyanets", {"row": row, "column": column})

    def delete_polyanet(self, row: int, column: int):
        return self.delete("polyanets", {"row": row, "column": column})