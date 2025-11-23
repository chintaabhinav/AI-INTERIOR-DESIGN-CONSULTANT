# src/tools/room_layout_optimizer.py
"""
Custom Tool: Room Layout Optimizer
Purpose: Validates furniture placement and calculates optimal room layouts
"""

from crewai_tools import BaseTool
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import json


class RoomLayoutOptimizerInput(BaseModel):
    """Input schema for Room Layout Optimizer."""
    room_length: float = Field(..., description="Room length in feet")
    room_width: float = Field(..., description="Room width in feet")
    furniture_list: str = Field(
        ..., 
        description='JSON array string with furniture items. '
                   'REQUIRED format: [{"name":"ItemName","width":##,"depth":##},...] '
                   'where width and depth are in INCHES. '
                   'Example: "[{\\"name\\":\\"Sofa\\",\\"width\\":84,\\"depth\\":36},{\\"name\\":\\"Table\\",\\"width\\":48,\\"depth\\":24}]"'
    )
    room_type: str = Field(
        default="living_room",
        description="Type of room: living_room, bedroom, office, etc."
    )


class RoomLayoutOptimizer(BaseTool):
    """
    Custom tool for validating and optimizing furniture layout in a room.
    
    This tool validates if furniture physically fits in the room and provides
    layout recommendations based on industry standards.
    """
    
    name: str = "room_layout_optimizer"
    description: str = (
        "Validates if furniture fits in a room and provides layout recommendations. "
        "CRITICAL: furniture_list MUST be a JSON array string with this exact format: "
        "[{\"name\":\"ItemName\",\"width\":##,\"depth\":##},...] "
        "where width and depth are in INCHES (not feet). "
        "Example input: room_length=15.0, room_width=12.0, "
        "furniture_list='[{\"name\":\"Sofa\",\"width\":84,\"depth\":36},{\"name\":\"Chair\",\"width\":32,\"depth\":34}]', "
        "room_type='living_room'. "
        "Returns: JSON with layout validation, space analysis, and recommendations."
    )
    
    def _run(
        self,
        room_length: float,
        room_width: float,
        furniture_list: str,
        room_type: str = "living_room"
    ) -> str:
        """Execute room layout validation."""
        try:
            # Parse furniture list from JSON string
            if isinstance(furniture_list, str):
                furniture_items = json.loads(furniture_list)
            else:
                furniture_items = furniture_list
            
            # Input validation
            validation_result = self._validate_inputs(
                room_length, room_width, furniture_items
            )
            if not validation_result["valid"]:
                return json.dumps({
                    "error": "Invalid input",
                    "details": validation_result["errors"],
                    "hint": "furniture_list must be array like: [{\"name\":\"Sofa\",\"width\":84,\"depth\":36}]"
                }, indent=2)
            
            # Calculate metrics
            room_area_sqft = room_length * room_width
            furniture_footprint = self._calculate_furniture_footprint(furniture_items)
            open_space_sqft = room_area_sqft - furniture_footprint
            open_space_percent = (open_space_sqft / room_area_sqft) * 100
            
            # Validate layout
            layout_validation = self._validate_layout(
                room_length, room_width, furniture_items, room_type
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                room_length, room_width, furniture_items,
                open_space_percent, layout_validation
            )
            
            # Build result
            result = {
                "layout_valid": layout_validation["overall_valid"],
                "room_dimensions": {
                    "length_ft": room_length,
                    "width_ft": room_width,
                    "total_area_sqft": round(room_area_sqft, 2)
                },
                "furniture_analysis": {
                    "total_pieces": len(furniture_items),
                    "total_footprint_sqft": round(furniture_footprint, 2),
                    "footprint_percent": round((furniture_footprint / room_area_sqft) * 100, 2)
                },
                "space_analysis": {
                    "open_space_sqft": round(open_space_sqft, 2),
                    "open_space_percent": round(open_space_percent, 2),
                    "circulation_rating": self._rate_circulation(open_space_percent)
                },
                "clearances": layout_validation["clearances"],
                "issues": layout_validation["issues"],
                "recommendations": recommendations,
                "summary": self._generate_summary(
                    layout_validation["overall_valid"],
                    open_space_percent,
                    layout_validation["issues"]
                )
            }
            
            return json.dumps(result, indent=2)
            
        except json.JSONDecodeError as e:
            return json.dumps({
                "error": "Invalid JSON format in furniture_list",
                "details": str(e),
                "received": furniture_list[:200],
                "expected_format": '[{"name":"Sofa","width":84,"depth":36}]'
            }, indent=2)
        except Exception as e:
            return json.dumps({
                "error": f"Layout optimization failed: {str(e)}",
                "room_dimensions": f"{room_length}' x {room_width}'"
            }, indent=2)
    
    def _validate_inputs(self, room_length: float, room_width: float, 
                        furniture_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate all inputs."""
        errors = []
        
        if room_length < 6 or room_length > 50:
            errors.append(f"Room length ({room_length}') outside range (6-50 feet)")
        if room_width < 6 or room_width > 50:
            errors.append(f"Room width ({room_width}') outside range (6-50 feet)")
        
        if not furniture_list:
            errors.append("Furniture list is empty")
        elif not isinstance(furniture_list, list):
            errors.append(f"Furniture list must be an array, got {type(furniture_list).__name__}")
        elif len(furniture_list) > 20:
            errors.append("Too many furniture pieces (max 20)")
        else:
            for i, item in enumerate(furniture_list):
                if not isinstance(item, dict):
                    errors.append(f"Item {i+1} must be an object with name, width, depth")
                    continue
                    
                if "name" not in item:
                    errors.append(f"Item {i+1} missing 'name' field")
                if "width" not in item:
                    errors.append(f"Item {i+1} ('{item.get('name', 'unnamed')}') missing 'width' field")
                if "depth" not in item:
                    errors.append(f"Item {i+1} ('{item.get('name', 'unnamed')}') missing 'depth' field")
                    
                if "width" in item and "depth" in item:
                    width = item.get("width", 0)
                    depth = item.get("depth", 0)
                    if width < 6 or width > 200:
                        errors.append(f"Item '{item.get('name', i+1)}' width ({width}\") unrealistic")
                    if depth < 6 or depth > 200:
                        errors.append(f"Item '{item.get('name', i+1)}' depth ({depth}\") unrealistic")
        
        return {"valid": len(errors) == 0, "errors": errors}
    
    def _calculate_furniture_footprint(self, furniture_list: List[Dict[str, Any]]) -> float:
        """Calculate total furniture footprint in square feet."""
        total_sqft = 0
        for item in furniture_list:
            width_ft = item.get("width", 0) / 12
            depth_ft = item.get("depth", 0) / 12
            total_sqft += width_ft * depth_ft
        return total_sqft
    
    def _validate_layout(self, room_length: float, room_width: float,
                        furniture_list: List[Dict[str, Any]], room_type: str) -> Dict[str, Any]:
        """Validate layout against industry standards."""
        issues = []
        clearances = {}
        
        room_length_inches = room_length * 12
        room_width_inches = room_width * 12
        
        for item in furniture_list:
            name = item.get("name", "Unknown")
            width = item.get("width", 0)
            depth = item.get("depth", 0)
            
            larger_dim = max(width, depth)
            if larger_dim > 32:
                clearances[f"{name}_doorway"] = {
                    "passes": False,
                    "note": f"May not fit through standard 32\" doorway ({larger_dim}\")"
                }
            
            fits_length = width <= room_length_inches and depth <= 36
            fits_width = width <= room_width_inches and depth <= 36
            
            if not (fits_length or fits_width):
                issues.append(f"{name} ({width}\"x{depth}\") too large for room")
        
        clearances["walkway_estimate"] = {
            "minimum_inches": 30,
            "preferred_inches": 36,
            "note": "Ensure 30-36\" clearance for main walkways"
        }
        
        overall_valid = len(issues) == 0
        
        return {
            "overall_valid": overall_valid,
            "clearances": clearances,
            "issues": issues
        }
    
    def _rate_circulation(self, open_space_percent: float) -> str:
        """Rate the circulation space quality."""
        if open_space_percent >= 70:
            return "Excellent - Very spacious"
        elif open_space_percent >= 60:
            return "Good - Comfortable circulation"
        elif open_space_percent >= 50:
            return "Adequate - Functional but cozy"
        elif open_space_percent >= 40:
            return "Tight - May feel cramped"
        else:
            return "Poor - Too crowded"
    
    def _generate_recommendations(self, room_length: float, room_width: float,
                                 furniture_list: List[Dict[str, Any]],
                                 open_space_percent: float,
                                 layout_validation: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if open_space_percent < 50:
            recommendations.append("Consider reducing furniture - less than 50% open space")
        elif open_space_percent > 80:
            recommendations.append("Room has extra space - could add accent pieces")
        
        if room_length > room_width * 1.5:
            recommendations.append("Long narrow room - create zones")
        
        if layout_validation["issues"]:
            recommendations.append("Layout issues detected - see issues list")
        else:
            recommendations.append("Layout is feasible - maintain 30-36\" walkways")
        
        return recommendations
    
    def _generate_summary(self, layout_valid: bool, open_space_percent: float,
                         issues: List[str]) -> str:
        """Generate human-readable summary."""
        if not layout_valid:
            return f"❌ Layout NOT feasible - {len(issues)} issue(s) found."
        
        if open_space_percent >= 60:
            return f"✓ Layout VALIDATED - {round(open_space_percent)}% open space."
        elif open_space_percent >= 50:
            return f"✓ Layout FEASIBLE - {round(open_space_percent)}% open space."
        else:
            return f"⚠ Layout POSSIBLE but tight - {round(open_space_percent)}% open space."