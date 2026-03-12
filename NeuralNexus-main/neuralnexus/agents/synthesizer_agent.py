from neuralnexus.agents.base_agent import BaseAgent
from typing import List, Dict


class SynthesizerAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="synthesizer_agent",
            description="Combines outputs from multiple agents into a final response"
        )

    def get_system_prompt(self) -> str:
        return """You are a Synthesizer Agent responsible for merging outputs from multiple AI agents into one final response.

CORE OBJECTIVE
Combine the agent outputs into a single clear answer that directly addresses the user's query.

STRICT RULES
1. Use ONLY information present in the agent outputs.
2. Do NOT invent new facts, technologies, or concepts.
3. Remove redundant or repeated information.
4. Preserve key insights from each agent.
5. Maintain topic consistency with the user's query.

RESPONSE GUIDELINES
• Produce a clean and well-structured response.
• Prefer bullet points when possible.
• Keep explanations concise.
• Maintain logical flow.

IMPORTANT
If agents provide multiple options (e.g., technologies, approaches, strategies):
• List the options clearly.
• If the query asks for a recommendation, select ONE option and justify it briefly.

OUTPUT REQUIREMENTS
• Clear structure
• Bullet points when helpful
• Concise summary at the end
• Maximum ~150 words when possible
"""

    def synthesize(self, user_query: str, agent_outputs: List[Dict]) -> str:
        """Merge outputs from multiple agents into one response"""

        outputs_text = "\n\n".join([
            f"Agent: {output.get('agent', 'unknown')}\n{output.get('response', '')}"
            for output in agent_outputs
        ])

        synthesis_prompt = f"""
User Query:
{user_query}

Agent Outputs:
{outputs_text}

Create a final response that answers the user's query using the agent outputs.
"""

        return self.execute(synthesis_prompt)