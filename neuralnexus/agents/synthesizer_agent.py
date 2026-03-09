from neuralnexus.agents.base_agent import BaseAgent
from typing import List, Dict

class SynthesizerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="synthesizer_agent",
            description="Synthesizes multiple agent outputs into a single concise response"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Synthesizer Agent specialized in merging multiple AI agent outputs into a single concise, structured response.

MANDATORY OUTPUT TEMPLATE:
[Topic Title]

Key Components:
- [Component 1 from agent insights]
- [Component 2 from agent insights]
- [Component 3 from agent insights]

System Flow:
[1-2 sentences describing how the system/concept works]

Key Strategy:
- [Strategic point 1]
- [Strategic point 2]
- [Strategic point 3]

Summary:
[1 sentence final takeaway]

SYNTHESIS RULES:
1. Extract unique insights from each agent output
2. Merge overlapping information into single points
3. Remove redundancy and repetition
4. Organize into the template structure
5. Maximum 120-150 words total

OUTPUT REQUIREMENT:
Return ONLY the synthesized response in the template structure.
NO meta-commentary. NO markdown symbols like ** or ##.
Use plain text with bullet points (-)."""
    
    def synthesize(self, user_query: str, agent_outputs: List[Dict]) -> str:
        """Synthesize multiple agent outputs into a single concise response"""
        
        outputs_text = "\n\n".join([
            f"Agent: {output.get('agent', 'unknown')}\nOutput: {output.get('response', '')}"
            for output in agent_outputs
        ])
        
        synthesis_prompt = f"""User Query: {user_query}

Agent Outputs to Synthesize:
{outputs_text}

Synthesize these outputs into a single concise response (maximum 150 words) that directly answers the user's query."""
        
        return self.execute(synthesis_prompt)
