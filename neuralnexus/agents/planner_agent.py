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
Break the user request into smaller tasks.
Assign each task to one of the following agents:

- research_agent → information gathering and explanations
- coding_agent → programming and technical implementation
- reasoning_agent → logical analysis, strategy, and planning

Respond ONLY with valid JSON in this format:
{
    "tasks": [
        {
            "task": "task description",
            "agent": "agent_name"
        }
    ]
}"""
    
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
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Plan parsing failed: {str(e)}, using fallback")
            return {
                "tasks": [
                    {
                        "task": query,
                        "agent": "research_agent"
                    }
                ]
            }
