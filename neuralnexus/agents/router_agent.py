import json
from neuralnexus.agents.base_agent import BaseAgent

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="router_agent",
            description="Routes queries to appropriate specialized agents"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Router Agent. Analyze the user query and decide which specialized agent should handle it.

Available agents:
- research_agent: For factual questions, knowledge queries, explanations, and information retrieval
- coding_agent: For programming tasks, code generation, debugging, and software development
- reasoning_agent: For logical analysis, planning, step-by-step problem solving, and strategic thinking

Respond ONLY with valid JSON in this exact format:
{
    "agent": "agent_name",
    "reason": "brief explanation of why this agent was chosen"
}"""
    
    def route(self, query: str) -> dict:
        response = self.execute(query)
        
        try:
            result = json.loads(response)
            if "agent" not in result or "reason" not in result:
                raise ValueError("Invalid routing response format")
            return result
        except json.JSONDecodeError:
            return {
                "agent": "research_agent",
                "reason": "Default fallback due to routing error"
            }
