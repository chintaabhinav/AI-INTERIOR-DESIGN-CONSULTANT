# test_agents.py
"""Test that agents initialize correctly"""

from src.agents import InteriorDesignAgents

print("="*60)
print("TESTING AGENTS INITIALIZATION")
print("="*60)

# Initialize agent factory
agents = InteriorDesignAgents()

# Test each agent
print("\n1. Testing Controller Agent...")
try:
    controller = agents.controller_agent()
    print(f"✓ Controller Agent created: {controller.role}")
    print(f"  Delegation: {controller.allow_delegation}")
except Exception as e:
    print(f"✗ Controller Agent failed: {e}")

print("\n2. Testing Space Analysis Agent...")
try:
    space = agents.space_analysis_agent()
    print(f"✓ Space Analysis Agent created: {space.role}")
    print(f"  Tools: {len(space.tools)} tool(s)")
except Exception as e:
    print(f"✗ Space Analysis Agent failed: {e}")

print("\n3. Testing Style Consultant Agent...")
try:
    style = agents.style_consultant_agent()
    print(f"✓ Style Consultant Agent created: {style.role}")
    print(f"  Tools: {len(style.tools)} tool(s)")
except Exception as e:
    print(f"✗ Style Consultant Agent failed: {e}")

print("\n4. Testing Furniture Recommendation Agent...")
try:
    furniture = agents.furniture_recommendation_agent()
    print(f"✓ Furniture Agent created: {furniture.role}")
    print(f"  Tools: {len(furniture.tools)} tool(s)")
except Exception as e:
    print(f"✗ Furniture Agent failed: {e}")

print("\n5. Testing Budget Optimization Agent...")
try:
    budget = agents.budget_optimization_agent()
    print(f"✓ Budget Agent created: {budget.role}")
    print(f"  Tools: {len(budget.tools)} tool(s)")
except Exception as e:
    print(f"✗ Budget Agent failed: {e}")

print("\n" + "="*60)
print("AGENT TESTING COMPLETE!")
print("="*60)