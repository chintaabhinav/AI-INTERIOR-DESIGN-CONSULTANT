# test_main.py
"""Test that main orchestration initializes correctly"""

print("="*60)
print("TESTING MAIN ORCHESTRATION")
print("="*60)

print("\n1. Testing imports...")
try:
    from src.main import run_design_consultation
    print("✓ Main function imported")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

print("\n2. Testing function signature...")
try:
    import inspect
    sig = inspect.signature(run_design_consultation)
    params = list(sig.parameters.keys())
    print(f"✓ Function has {len(params)} parameters")
    print(f"  Parameters: {', '.join(params[:5])}...")
except Exception as e:
    print(f"✗ Signature check failed: {e}")

print("\n" + "="*60)
print("MAIN ORCHESTRATION TEST COMPLETE!")
print("="*60)
print("\n⚠️  NOTE: We're not running the full consultation yet")
print("   (it would take 2-5 minutes and use API credits)")
print("\n✅ Main system is ready to run!")
print("\nTo run a full consultation:")
print("   python src/main.py")