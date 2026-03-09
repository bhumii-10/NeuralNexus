from neuralnexus.agents.base_agent import BaseAgent

class ReasoningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="reasoning_agent",
            description="Handles logical analysis and planning tasks"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Reasoning Agent specialized in logical analysis and planning.

Your responsibilities:
- Break down complex problems
- Provide step-by-step analysis
- Create strategic plans
- Apply logical reasoning

Think systematically and provide structured, well-reasoned responses."""
