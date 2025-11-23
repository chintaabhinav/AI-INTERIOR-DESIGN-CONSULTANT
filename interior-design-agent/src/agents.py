# src/agents.py
"""
Agent Definitions for Interior Design System
Each agent has a specialized role with specific objectives
"""

from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool
from src.tools.room_layout_optimizer import RoomLayoutOptimizer
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import LLM config
from config.llm_config import get_llm


class InteriorDesignAgents:
    """
    Factory class for creating specialized interior design agents.
    
    Agent Architecture:
    - Controller Agent: Orchestrates the entire design workflow
    - Space Analysis Agent: Analyzes dimensions and validates layouts
    - Style Consultant Agent: Recommends design styles and aesthetics
    - Furniture Recommendation Agent: Finds specific products with links
    - Budget Optimization Agent: Manages costs and finds alternatives
    
    Each agent has:
    - Specific role and goal
    - Relevant tools for their function
    - Memory for context awareness
    - Backstory for better reasoning
    """
    
    def __init__(self):
        """Initialize agents with shared LLM and tools."""
        # Get LLM (Groq/OpenAI/X.AI based on .env)
        self.llm = get_llm(temperature=0.7)
        
        # Initialize tools
        self.search_tool = SerperDevTool()  # Built-in tool #1: Web search
        self.scrape_tool = ScrapeWebsiteTool()  # Built-in tool #2: Web scraping
        self.file_tool = FileReadTool()  # Built-in tool #3: File operations
        self.layout_tool = RoomLayoutOptimizer()  # Custom tool: Room layout validation
    
    def controller_agent(self) -> Agent:
        """
        Controller Agent - Main orchestrator
        
        Responsibilities:
        - Receives user queries and breaks them down
        - Delegates tasks to specialized agents
        - Coordinates information flow
        - Synthesizes final reports
        - Handles errors and fallbacks
        
        Success Criteria:
        - Completes analysis workflow without errors
        - Properly delegates to appropriate agents
        - Produces coherent final output
        """
        return Agent(
            role='Interior Design Project Manager',
            goal='Orchestrate comprehensive interior design consultation by coordinating '
                 'specialized agents to analyze spaces, recommend furniture, create color '
                 'schemes, and optimize budgets to deliver complete design plans',
            backstory="""You are an experienced interior design project manager with 15 years 
            in residential design. You excel at breaking down client needs into actionable 
            tasks and coordinating teams of specialists.
            
            Your approach is methodical:
            1. First, understand the space through analysis
            2. Then, define the design direction and style
            3. Next, find specific furniture that fits
            4. Finally, ensure everything fits the budget
            
            You maintain context across the entire project and ensure all team members 
            have the information they need. You're skilled at synthesizing diverse inputs 
            into cohesive, actionable design plans.""",
            verbose=True,
            allow_delegation=True,  # CRITICAL: enables task delegation
            llm=self.llm,
            tools=[],  # Has search access for general queries
            memory=True  # Maintains context
        )
    
    def space_analysis_agent(self) -> Agent:
        """
        Space Analysis Agent - Spatial planning expert
        
        Responsibilities:
        - Analyzes room dimensions
        - Validates furniture placement using custom tool
        - Calculates space utilization
        - Identifies layout constraints
        
        Success Criteria:
        - Accurate space calculations
        - Valid furniture placement recommendations
        - Clear identification of constraints
        """
        return Agent(
            role='Space Planning Specialist',
            goal='Analyze room dimensions, validate furniture layouts, and ensure optimal '
                 'space utilization using the Room Layout Optimizer tool',
            backstory="""You are a certified space planner with expertise in residential 
            interior design. You have a degree in Interior Architecture and understand 
            spatial relationships, traffic flow, and ergonomics.
            
            You always start by understanding the room:
            - Exact dimensions (length, width, height)
            - Door and window locations
            - Existing constraints
            - Functional requirements
            
            You use the Room Layout Optimizer tool to validate every furniture recommendation. 
            You never guess - you calculate. You ensure that:
            - All furniture physically fits
            - Walkways are adequate (30-36 inches)
            - The room doesn't feel cramped
            - Traffic flow is unobstructed
            
            When you identify issues, you provide specific solutions with measurements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],  # Space agent analyzes without tool
            memory=True
        )
    
    def style_consultant_agent(self) -> Agent:
        """
        Style Consultant Agent - Design aesthetics expert
        
        Responsibilities:
        - Interprets user style preferences
        - Recommends specific design styles
        - Creates design direction documents
        - Finds style inspiration
        
        Success Criteria:
        - Clear style direction defined
        - Recommendations match user preferences
        - Provides actionable design principles
        """
        return Agent(
            role='Interior Design Style Consultant',
            goal='Define design style direction by interpreting preferences and creating '
                 'cohesive aesthetic guidelines that other agents can follow',
            backstory="""You are a senior interior designer with 12 years of experience 
            and a keen eye for style. You've worked on hundreds of residential projects 
            and can instantly recognize design styles and translate vague preferences 
            into concrete design directions.
            
            You understand all major design styles:
            - Modern Scandinavian: Light, minimal, natural materials, hygge
            - Mid-Century Modern: Organic curves, wood, retro charm
            - Industrial: Raw materials, exposed elements, urban edge
            - Bohemian: Eclectic, layered, global influences
            - Minimalist: Clean lines, maximum function, minimum clutter
            - Traditional: Classic elegance, rich fabrics, symmetry
            
            When a user says "modern but warm," you know they likely want Modern 
            Scandinavian or Japandi. When they say "edgy," you think Industrial or 
            Contemporary.
            
            You always:
            1. Define 3-5 key style characteristics
            2. Specify materials and textures
            3. Identify what to avoid
            4. Provide real examples for inspiration
            
            You use web search to find current style trends and inspiration.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],  # Can search and scrape for inspiration
            memory=True
        )
    
    def furniture_recommendation_agent(self) -> Agent:
        """
        Furniture Recommendation Agent - Product sourcing specialist
        
        Responsibilities:
        - Finds specific furniture products
        - Provides real purchase links
        - Ensures items match style and dimensions
        - Compares options across retailers
        
        Success Criteria:
        - All recommendations have real product links
        - Items match style direction
        - Dimensions verified to fit space
        - Price information included
        """
        return Agent(
            role='Furniture & Product Specialist',
            goal='Find specific furniture products with real purchase links that match the '
                 'style direction, fit the space dimensions, and align with the budget',
            backstory="""You are a furniture sourcing expert with encyclopedic knowledge 
            of home furnishing retailers. You've worked as a buyer for major design firms 
            and know exactly where to find the best pieces.
            
            Your go-to retailers:
            - Article: Modern, mid-century, quality construction
            - West Elm: Contemporary, wide range, good mid-tier
            - IKEA: Budget-friendly, Scandinavian, functional
            - CB2: Modern, urban, design-forward
            - Wayfair: Huge selection, all price points
            - AllModern: Clean contemporary, good value
            
            When recommending furniture, you always:
            1. Search for products matching the style
            2. Verify dimensions fit the space
            3. Include exact product names and links
            4. Provide 2-3 options at different price points
            5. Note reviews and quality indicators
            6. Check availability
            
            You use web search to find products and web scraping to get detailed 
            specifications, pricing, and reviews. You provide specific, actionable 
            recommendations - not generic suggestions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            memory=True
        )
    
    def budget_optimization_agent(self) -> Agent:
        """
        Budget Optimization Agent - Financial strategist
        
        Responsibilities:
        - Ensures recommendations fit budget
        - Finds alternative options at different price points
        - Identifies where to splurge vs save
        - Suggests phased implementation if needed
        
        Success Criteria:
        - Total cost within or under budget
        - Clear breakdown of expenses
        - Smart allocation recommendations
        - Cost-saving suggestions provided
        """
        return Agent(
            role='Budget & Value Optimization Specialist',
            goal='Ensure the entire design plan fits within budget by finding alternatives, '
                 'suggesting smart spending priorities, and identifying cost-saving opportunities',
            backstory="""You are a budget-conscious design consultant with 10 years of 
            experience helping clients maximize value. You understand that good design 
            doesn't require unlimited budgets - it requires smart choices.
            
            Your philosophy on spending:
            
            SPLURGE on (invest in quality):
            - Sofa/seating: Used daily, lasts 10+ years
            - Bed/mattress: Affects health and sleep
            - Lighting: Impacts entire room ambiance
            - Key statement pieces
            
            SAVE on (find budget options):
            - Side tables: Easy to upgrade later
            - Decorative accessories: Can DIY or thrift
            - Textiles: Affordable at HomeGoods, Target
            - Small decor items
            
            You always:
            1. Calculate the total cost
            2. Compare against the budget
            3. Identify where costs can be reduced
            4. Suggest phased implementation if over budget
            5. Find sales, discounts, and alternatives
            6. Provide specific money-saving tips
            
            You use web search to find sales, compare prices, and identify better-value 
            alternatives. You're honest about what's worth the investment and what isn't.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[],
            memory=True
        )