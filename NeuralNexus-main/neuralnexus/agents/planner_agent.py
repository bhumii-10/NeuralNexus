import json
from neuralnexus.agents.base_agent import BaseAgent
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="planner_agent",
            description="Decomposes complex queries into multiple tasks"
        )

    def get_system_prompt(self) -> str:
        return """You are a task planning agent.

Break the user query into smaller tasks for specialized agents.

RULES:
1. Each task must address ONE part of the query.
2. Tasks must NOT overlap.
3. Assign the best agent.

AGENTS:
- research_agent → factual info, explanations, technologies
- reasoning_agent → analysis, comparisons, decisions
- coding_agent → programming tasks

Return JSON only.

Example:

{
 "tasks":[
  {"task":"Explain the topic","agent":"research_agent"},
  {"task":"Design system architecture","agent":"reasoning_agent"},
  {"task":"Recommend best option","agent":"reasoning_agent"}
 ]
}
"""

    def plan(self, query: str) -> dict:

        logger.info(f"Planning tasks for query: {query[:50]}...")

        response = self.execute(query)

        try:

            result = json.loads(response)

            if "tasks" not in result or not isinstance(result["tasks"], list):
                raise ValueError("Invalid plan format")

            for task in result["tasks"]:
                if "task" not in task or "agent" not in task:
                    raise ValueError("Invalid task format")

            logger.info(f"Generated {len(result['tasks'])} tasks")

            return result

        except (json.JSONDecodeError, ValueError):

            logger.warning("Planner fallback triggered")

            return {
                "tasks":[
                    {"task":query,"agent":"research_agent"}
                ]
            }