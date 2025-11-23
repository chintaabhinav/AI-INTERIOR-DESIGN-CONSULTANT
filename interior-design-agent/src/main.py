# src/main.py
"""
Main Orchestration for Interior Design Agent System
This is the entry point that coordinates all agents and tasks
"""

from crewai import Crew, Process
from src.agents import InteriorDesignAgents
from src.tasks import InteriorDesignTasks
import json
from datetime import datetime
import os


def run_design_consultation(
    room_type: str = "living room",
    room_length: float = 15.0,
    room_width: float = 12.0,
    room_height: float = 9.0,
    windows: str = "One large window on north wall",
    doors: str = "Entry door on south wall",
    style_preference: str = "Modern Scandinavian",
    color_preference: str = "Warm whites and natural tones",
    must_haves: str = "Seating for 4-5, TV area, storage",
    budget: int = 4000,
    avoid: str = "Nothing too minimal or cold"
) -> dict:
    """
    Run a complete interior design consultation.
    
    Args:
        room_type: Type of room (living room, bedroom, office, etc.)
        room_length: Room length in feet
        room_width: Room width in feet
        room_height: Ceiling height in feet
        windows: Description of window locations
        doors: Description of door locations
        style_preference: User's style preferences
        color_preference: Preferred colors
        must_haves: Required features/furniture
        budget: Total budget in USD
        avoid: Things to avoid
    
    Returns:
        Dictionary with results and final report
    """
    
    print("="*70)
    print("🏠 INTERIOR DESIGN AI CONSULTATION")
    print("="*70)
    print(f"\nStarting consultation for {room_type}...")
    print(f"Room: {room_length}' x {room_width}'")
    print(f"Budget: ${budget:,}")
    print(f"Style: {style_preference}")
    print("\n" + "-"*70)
    
    # Prepare input data
    room_info = {
        "room_type": room_type,
        "room_length": room_length,
        "room_width": room_width,
        "room_height": room_height,
        "windows": windows,
        "doors": doors,
        "must_haves": must_haves
    }
    
    user_preferences = {
        "style": style_preference,
        "color_preference": color_preference,
        "must_haves": must_haves,
        "avoid": avoid,
        "budget": budget
    }
    
    # Initialize agents and tasks
    print("\n🤖 Initializing AI Agents...")
    agents = InteriorDesignAgents()
    tasks = InteriorDesignTasks()
    
    print("✓ Controller Agent ready")
    print("✓ Space Analysis Agent ready")
    print("✓ Style Consultant Agent ready")
    print("✓ Furniture Recommendation Agent ready")
    print("✓ Budget Optimization Agent ready")
    
    # Create tasks
    print("\n📋 Creating Tasks...")
    task1 = tasks.analyze_space_task(room_info)
    task2 = tasks.define_style_task(user_preferences)
    task3 = tasks.find_furniture_task(room_info, style_preference, budget)
    task4 = tasks.optimize_budget_task("", budget)  # Will get furniture list from task3
    task5 = tasks.generate_final_report_task(room_info, user_preferences, budget)
    
    print("✓ Space Analysis Task created")
    print("✓ Style Definition Task created")
    print("✓ Furniture Search Task created")
    print("✓ Budget Optimization Task created")
    print("✓ Final Report Generation Task created")
    
    # Create the Crew
    print("\n👥 Assembling Design Team (Crew)...")
    crew = Crew(
        agents=[
            agents.space_analysis_agent(),
            agents.style_consultant_agent(),
            agents.furniture_recommendation_agent(),
            agents.budget_optimization_agent(),
            agents.controller_agent()
        ],
        tasks=[task1, task2, task3, task4, task5],
        process=Process.sequential,  # Tasks run in order
        verbose=False,  # Show detailed output
        memory=False,  # Enable memory across tasks
        cache=True,  # Cache results for efficiency
        max_rpm=10  # Rate limiting for API calls
    )
    
    print("✓ Crew assembled with 5 agents and 5 tasks")
    print("✓ Sequential process (tasks run in order)")
    print("✓ Memory enabled (agents share context)")
    
    # Execute the consultation
    print("\n" + "="*70)
    print("🚀 STARTING DESIGN CONSULTATION")
    print("="*70)
    print("\nThis will take 2-5 minutes. Agents are working...\n")
    
    try:
        # Run the crew
        result = crew.kickoff()
        
        print("\n" + "="*70)
        print("✅ CONSULTATION COMPLETE!")
        print("="*70)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "outputs/reports"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save full report
        report_file = f"{output_dir}/design_plan_{timestamp}.txt"
        with open(report_file, 'w') as f:
            f.write(str(result))
        
        print(f"\n📄 Full report saved to: {report_file}")
        
        # Save metadata
        metadata = {
            "timestamp": timestamp,
            "room_info": room_info,
            "user_preferences": user_preferences,
            "budget": budget,
            "report_file": report_file
        }
        
        metadata_file = f"{output_dir}/metadata_{timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📊 Metadata saved to: {metadata_file}")
        
        return {
            "success": True,
            "result": str(result),
            "report_file": report_file,
            "metadata": metadata,
            "timestamp": timestamp
        }
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR DURING CONSULTATION")
        print("="*70)
        print(f"\nError: {str(e)}")
        
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
        }


def main():
    """
    Main entry point for command-line usage.
    """
    print("\n" + "="*70)
    print("🏠 AI INTERIOR DESIGN CONSULTANT")
    print("="*70)
    
    # Example consultation
    result = run_design_consultation(
        room_type="living room",
        room_length=15,
        room_width=12,
        room_height=9,
        windows="Large window on north wall (6 feet wide)",
        doors="Entry door on south wall (left side)",
        style_preference="Modern Scandinavian with warm, cozy elements",
        color_preference="Warm whites, light grays, natural wood tones",
        must_haves="Comfortable seating for 4-5 people, TV viewing area, book storage",
        budget=4000,
        avoid="Too minimal or cold, heavy dark furniture"
    )
    
    if result["success"]:
        print("\n✅ Consultation completed successfully!")
        print(f"\n📄 View your design plan at:")
        print(f"   {result['report_file']}")
        
        print("\n" + "="*70)
        print("PREVIEW OF DESIGN PLAN")
        print("="*70)
        
        # Show preview (first 2000 characters)
        preview = result["result"][:2000]
        print(preview)
        
        if len(result["result"]) > 2000:
            print("\n... (see full report in file)")
    else:
        print(f"\n❌ Consultation failed: {result.get('error', 'Unknown error')}")
    
    return result


if __name__ == "__main__":
    main()