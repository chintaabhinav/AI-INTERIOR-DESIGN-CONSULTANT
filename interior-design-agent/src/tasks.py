# src/tasks.py - OPTIMIZED FOR LOW TOKEN USAGE
"""
Task Definitions for Interior Design System - Optimized Version
"""

from crewai import Task
from src.agents import InteriorDesignAgents


class InteriorDesignTasks:
    """Task definitions optimized for token efficiency."""
    
    def __init__(self):
        self.agents = InteriorDesignAgents()
    
    def analyze_space_task(self, room_info: dict) -> Task:
        """Task: Analyze space - OPTIMIZED"""
        return Task(
            description=f"""Analyze this {room_info.get('room_type')} space:
            - Size: {room_info.get('room_length')}' x {room_info.get('room_width')}'
            - Features: {room_info.get('windows')}, {room_info.get('doors')}
            - Needs: {room_info.get('must_haves')}
            
            Provide: room area, layout constraints, furniture size recommendations (2-3 sentences).""",
            agent=self.agents.space_analysis_agent(),
            expected_output="Brief space analysis with key measurements and recommendations"
        )
    
    def define_style_task(self, user_preferences: dict) -> Task:
        """Task: Define style - OPTIMIZED"""
        return Task(
            description=f"""Define design style for:
            - Preferred style: {user_preferences.get('style')}
            - Colors: {user_preferences.get('color_preference')}
            - Budget: ${user_preferences.get('budget')}
            
            Provide: style name, 3-4 key characteristics, color palette (keep brief).""",
            agent=self.agents.style_consultant_agent(),
            expected_output="Concise style direction with key guidelines"
        )
    
    def find_furniture_task(self, room_info: dict, style_direction: str, budget: int) -> Task:
        """Task: Find furniture - OPTIMIZED"""
        return Task(
            description=f"""Find 5-6 furniture items for {room_info.get('room_type')}:
            - Style: {style_direction}
            - Needs: {room_info.get('must_haves')}
            - Budget: ${budget}
            
            For each item provide: name, price, dimensions, store, brief reason. Keep descriptions short.""",
            agent=self.agents.furniture_recommendation_agent(),
            expected_output="List of 5-6 furniture items with essential details"
        )
    
    def optimize_budget_task(self, furniture_list: str, budget: int) -> Task:
        """Task: Optimize budget - OPTIMIZED"""
        return Task(
            description=f"""Review furniture list and optimize for ${budget} budget.
            
            Provide: total cost, budget status, 2-3 money-saving tips (brief).""",
            agent=self.agents.budget_optimization_agent(),
            expected_output="Budget summary with optimization suggestions"
        )
    
    def generate_final_report_task(self, room_info: dict, user_preferences: dict, budget: int) -> Task:
        """Task: Generate report - OPTIMIZED"""
        return Task(
            description=f"""Create final design plan summary for {room_info.get('room_type')}.
            
            Include:
            1. Executive summary (2-3 sentences)
            2. Room: {room_info.get('room_length')}' x {room_info.get('room_width')}'
            3. Style direction from Style Consultant
            4. Furniture list from Furniture Agent
            5. Budget summary from Budget Agent
            6. Next steps (3-4 bullet points)
            
            Keep concise and actionable. Total output should be 200-300 words.""",
            agent=self.agents.controller_agent(),
            expected_output="Concise final design plan (200-300 words)"
        )