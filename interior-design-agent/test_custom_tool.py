# test_custom_tool.py
"""Test the Room Layout Optimizer custom tool"""

from src.tools.room_layout_optimizer import RoomLayoutOptimizer
import json

print("="*60)
print("TESTING CUSTOM TOOL: Room Layout Optimizer")
print("="*60)

# Initialize the tool
tool = RoomLayoutOptimizer()

# Test Case 1: Valid layout
print("\n### TEST 1: Valid Living Room Layout ###")
result1 = tool._run(
    room_length=15,
    room_width=12,
    furniture_list=[
        {"name": "Sofa", "width": 84, "depth": 36},
        {"name": "Coffee Table", "width": 48, "depth": 24},
        {"name": "TV Stand", "width": 60, "depth": 18},
        {"name": "Armchair", "width": 32, "depth": 34}
    ],
    room_type="living_room"
)

result1_dict = json.loads(result1)
print(f"✓ Layout Valid: {result1_dict['layout_valid']}")
print(f"✓ Open Space: {result1_dict['space_analysis']['open_space_percent']}%")
print(f"✓ Rating: {result1_dict['space_analysis']['circulation_rating']}")
print(f"✓ Summary: {result1_dict['summary']}")

# Test Case 2: Too much furniture
print("\n### TEST 2: Overcrowded Room ###")
result2 = tool._run(
    room_length=10,
    room_width=10,
    furniture_list=[
        {"name": "King Bed", "width": 76, "depth": 80},
        {"name": "Dresser", "width": 60, "depth": 20},
        {"name": "Nightstand 1", "width": 24, "depth": 20},
        {"name": "Nightstand 2", "width": 24, "depth": 20},
        {"name": "Desk", "width": 48, "depth": 24},
        {"name": "Bookshelf", "width": 36, "depth": 12}
    ],
    room_type="bedroom"
)

result2_dict = json.loads(result2)
print(f"✓ Layout Valid: {result2_dict['layout_valid']}")
print(f"✓ Open Space: {result2_dict['space_analysis']['open_space_percent']}%")
print(f"✓ Rating: {result2_dict['space_analysis']['circulation_rating']}")
print(f"✓ Issues: {len(result2_dict['issues'])} found")

# Test Case 3: Invalid input
print("\n### TEST 3: Invalid Input Handling ###")
result3 = tool._run(
    room_length=2,  # Too small
    room_width=100,  # Too large
    furniture_list=[],  # Empty
    room_type="office"
)

result3_dict = json.loads(result3)
if "error" in result3_dict:
    print(f"✓ Error handling works: {result3_dict['error']}")
    print(f"✓ Errors caught: {len(result3_dict['details'])}")

print("\n" + "="*60)
print("CUSTOM TOOL TESTING COMPLETE!")
print("="*60)