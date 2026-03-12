from typing import Dict, Callable
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class ToolRegistry:
    """Placeholder for future tool integration capabilities"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
    
    def register_tool(self, name: str, func: Callable):
        self.tools[name] = func
        logger.info(f"Registered tool: {name}")
    
    def get_tool(self, name: str) -> Callable:
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        return list(self.tools.keys())

tool_registry = ToolRegistry()
