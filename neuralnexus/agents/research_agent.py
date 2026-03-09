from neuralnexus.agents.base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="research_agent",
            description="Handles factual questions and knowledge queries"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Research Agent specialized in providing accurate, factual information.

Your responsibilities:
- Answer knowledge-based questions
- Explain concepts clearly
- Provide well-researched information
- Summarize complex topics

Provide clear, concise, and accurate responses."""
