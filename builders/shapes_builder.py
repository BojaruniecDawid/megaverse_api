import time
from typing import List, Tuple
from services.polyanets_service import PolyanetsService


class ShapeBuilder:
    def __init__(self, delay: float = 0.2):
        self.service = PolyanetsService()
        self.delay = delay

    def create_points(self, points: List[Tuple[int, int]]):
        #Create multiple Polyanets at given coordinates.
        for row, col in points:
            try:
                self.service.create_polyanet(row, col)
            except Exception as e:
                if "429" in str(e):
                    print(f"429 Too Many Requests at ({row},{col}), waiting {self.delay}s...")
                    time.sleep(self.delay)
                    self.service.create_polyanet(row, col)  # retry once
                else:
                    print(f"Failed to create Polyanet at ({row},{col}): {e}")
            time.sleep(self.delay)

    def delete_points(self, points: List[Tuple[int, int]]):
        #Delete multiple Polyanets at given coordinates.
        for row, col in points:
            try:
                self.service.delete_polyanet(row, col)
            except Exception as e:
                if "429" in str(e):
                    print(f"429 Too Many Requests at ({row},{col}), waiting {self.delay}s...")
                    time.sleep(self.delay)
                    self.service.delete_polyanet(row, col)  # retry once
                else:
                    print(f"Failed to delete Polyanet at ({row},{col}): {e}")
            time.sleep(self.delay)

    def diagonal_line(self, start_row: int, start_col: int, length: int, direction: str) -> List[Tuple[int, int]]:
        #Returns coordinates for a diagonal line.
        coords = []
        for i in range(length):
            row = start_row + i
            col = start_col + (i if direction == "right" else -i)
            coords.append((row, col))
        return coords

    def x_shape(self, start_row: int, start_col: int, size: int = 7) -> List[Tuple[int, int]]:
        line1 = self.diagonal_line(start_row, start_col, size, "right")
        line2 = self.diagonal_line(start_row, start_col + size - 1, size, "left")
        # Merge and remove duplicates
        return list(dict.fromkeys(line1 + line2))
