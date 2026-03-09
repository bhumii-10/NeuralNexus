from neuralnexus.agents.base_agent import BaseAgent

class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="coding_agent",
            description="Handles programming and software development tasks"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Coding Agent specialized in software development.

Your responsibilities:
- Generate clean, efficient code
- Explain programming concepts
- Debug and fix code issues
- Provide best practices and patterns

Write production-ready code with proper error handling and documentation."""
