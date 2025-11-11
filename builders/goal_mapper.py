import time
import requests
import asyncio
from services.polyanets_service import PolyanetsService
from services.soloons_service import SoloonsService
from services.comeths_service import ComethsService


class GoalMapper:
    def __init__(self, delay: float = 0.2):
        self.polyanets = PolyanetsService()
        self.soloons = SoloonsService()
        self.comeths = ComethsService()
        self.delay = delay

    def process_goal(self, goal_matrix):
        for row_idx, row in enumerate(goal_matrix, start=1):
            for col_idx, value in enumerate(row, start=1):
                if value == "SPACE":
                    continue
                self.send_request(row_idx, col_idx, value)
                time.sleep(self.delay)

    def send_request(self, row, col, value):
        try:
            if value == "POLYANET":
                self.polyanets.create_polyanet(row, col)
            elif value.endswith("_SOLOON"):
                color = value.split("_")[0].lower()
                self.soloons.create_soloon(row, col, color)
            elif value.endswith("_COMETH"):
                direction = value.split("_")[0].lower()
                self.comeths.create_cometh(row, col, direction)
            else:
                print(f"Unknown goal value: {value} at ({row},{col})")
        except Exception as e:
            print(f"Failed to create {value} at ({row},{col}): {e}")


class AsyncGoalMapper:

    def __init__(self, candidate_id: str, concurrency: int = 20, delay: float = 0.05, index_base: int = 1):
        self.polyanets = PolyanetsService()
        self.soloons = SoloonsService()
        self.comeths = ComethsService()
        self.candidate_id = candidate_id
        self.concurrency = concurrency
        self.delay = delay
        self.index_base = index_base

    async def create_goal(self, goal_matrix):
        # Create elements from goal matrix.
        await self._process_matrix(goal_matrix, action="create")

    async def delete_goal(self, goal_matrix):
        # Delete elements from goal matrix.
        await self._process_matrix(goal_matrix, action="delete")

    async def _process_matrix(self, matrix, action="create"):
        # Process the goal matrix asynchronously with concurrency and retries.
        semaphore = asyncio.Semaphore(self.concurrency)
        tasks = []

        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                if value == "SPACE":
                    continue

                # Adjust coordinates according to API indexing
                api_row = row_idx + self.index_base
                api_col = col_idx + self.index_base

                tasks.append(
                    self._process_element(semaphore, api_row, api_col, value, action, rows, cols)
                )

        await asyncio.gather(*tasks)

    async def _process_element(self, semaphore, row, col, value, action, max_rows, max_cols):
        # Handle creating or deleting a single element with retries.
        async with semaphore:
            for attempt in range(3):
                try:
                    # Validate coordinates
                    if row < self.index_base or col < self.index_base or row > max_rows + self.index_base - 1 or col > max_cols + self.index_base - 1:
                        print(f"Skipping {value} at ({row},{col}) – out of bounds")
                        return

                    if action == "create":
                        if value == "POLYANET":
                            self.polyanets.create_polyanet(row, col)
                        elif value.endswith("_SOLOON"):
                            color = value.split("_")[0].lower()
                            self.soloons.create_soloon(row, col, color)
                        elif value.endswith("_COMETH"):
                            direction = value.split("_")[0].lower()
                            self.comeths.create_cometh(row, col, direction)
                    elif action == "delete":
                        if value == "POLYANET":
                            self.polyanets.delete_polyanet(row, col)
                        elif value.endswith("_SOLOON"):
                            self.soloons.delete_soloon(row, col)
                        elif value.endswith("_COMETH"):
                            self.comeths.delete_cometh(row, col)
                    else:
                        print(f"Unknown value: {value} at ({row},{col})")

                    await asyncio.sleep(self.delay)
                    return
                except Exception as e:
                    print(f"Attempt {attempt+1} failed for {action} {value} at ({row},{col}): {e}")
                    await asyncio.sleep(self.delay * 2)
            print(f"Failed to {action} {value} at ({row},{col}) after retries")