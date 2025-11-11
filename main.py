import asyncio
import requests
from core.config import Config
from builders.shapes_builder import ShapeBuilder
from builders.goal_mapper import GoalMapper, AsyncGoalMapper

if __name__ == "__main__":

    #1 X shape
    builder = ShapeBuilder(delay=0.4)
    
    points = builder.x_shape(start_row=2, start_col=2, size=7)
    builder.create_points(points)
    print("X shape created!")

    #2 butterfly pattern
    BASE_URL = Config.BASE_URL
    CANDIDATE_ID = Config.CANDIDATE_ID

    GOAL_URL = f"{BASE_URL}/map/{CANDIDATE_ID}/goal"

    response = requests.get(GOAL_URL, headers={"Content-Type": "application/json"}).json()
    goal_matrix = response["goal"]

    # Set index_base=1 if API uses 0-based indexing
    mapper = AsyncGoalMapper(candidate_id=CANDIDATE_ID, concurrency=20, delay=0.05, index_base=0)

    # Optional: delete existing elements
    asyncio.run(mapper.delete_goal(goal_matrix))

    # Create the goal pattern exactly as in the matrix
    asyncio.run(mapper.create_goal(goal_matrix))