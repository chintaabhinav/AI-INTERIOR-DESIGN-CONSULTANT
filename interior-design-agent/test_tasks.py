# test_tasks.py
"""Test that tasks initialize correctly"""

from src.tasks import InteriorDesignTasks

print("="*60)
print("TESTING TASKS INITIALIZATION")
print("="*60)

# Initialize task factory
tasks = InteriorDesignTasks()

# Test room info
room_info = {
    "room_type": "living room",
    "room_length": 15,
    "room_width": 12,
    "room_height": 9,
    "must_haves": "Seating for 5, TV area, storage"
}

user_prefs = {
    "style": "Modern Scandinavian",
    "color_preference": "Warm whites and natural tones",
    "budget": 4000
}

print("\n1. Testing Space Analysis Task...")
try:
    task1 = tasks.analyze_space_task(room_info)
    print(f"✓ Space Analysis Task created")
    print(f"  Agent: {task1.agent.role}")
except Exception as e:
    print(f"✗ Space Analysis Task failed: {e}")

print("\n2. Testing Style Definition Task...")
try:
    task2 = tasks.define_style_task(user_prefs)
    print(f"✓ Style Definition Task created")
    print(f"  Agent: {task2.agent.role}")
except Exception as e:
    print(f"✗ Style Definition Task failed: {e}")

print("\n3. Testing Furniture Search Task...")
try:
    task3 = tasks.find_furniture_task(room_info, "Modern Scandinavian", 4000)
    print(f"✓ Furniture Search Task created")
    print(f"  Agent: {task3.agent.role}")
except Exception as e:
    print(f"✗ Furniture Search Task failed: {e}")

print("\n4. Testing Budget Optimization Task...")
try:
    task4 = tasks.optimize_budget_task("furniture list", 4000)
    print(f"✓ Budget Optimization Task created")
    print(f"  Agent: {task4.agent.role}")
except Exception as e:
    print(f"✗ Budget Optimization Task failed: {e}")

print("\n5. Testing Final Report Task...")
try:
    task5 = tasks.generate_final_report_task(room_info, user_prefs, 4000)
    print(f"✓ Final Report Task created")
    print(f"  Agent: {task5.agent.role}")
except Exception as e:
    print(f"✗ Final Report Task failed: {e}")

print("\n" + "="*60)
print("TASK TESTING COMPLETE!")
print("="*60)