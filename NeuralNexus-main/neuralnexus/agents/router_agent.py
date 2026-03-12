import json
from neuralnexus.agents.base_agent import BaseAgent

class RouterAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="router_agent",
            description="Routes queries to appropriate specialized agents"
        )

    def get_system_prompt(self) -> str:
        return """You are a Router Agent.

Choose which agent should handle the query.

Agents:
- research_agent → explanations, knowledge
- coding_agent → programming or implementation
- reasoning_agent → comparison, recommendation, decision

Return JSON only:

{
 "agent":"agent_name",
 "reason":"short explanation"
}
"""

    def route(self, query: str) -> dict:

        query_lower = query.lower()

        if any(word in query_lower for word in [
            "best","better","recommend","compare","which","choose"
        ]):
            return {
                "agent":"reasoning_agent",
                "reason":"comparison or recommendation"
            }

        if any(word in query_lower for word in [
            "code","implement","function","program"
        ]):
            return {
                "agent":"coding_agent",
                "reason":"programming query"
            }

        response = self.execute(query)

        try:
            result = json.loads(response)

            if "agent" not in result:
                raise ValueError()

            return result

        except:
            return {
                "agent":"research_agent",
                "reason":"default fallback"
            }