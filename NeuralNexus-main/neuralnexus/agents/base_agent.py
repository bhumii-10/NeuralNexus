from abc import ABC, abstractmethod
from neuralnexus.llm.llm_client import llm_client
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseAgent(ABC):

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = llm_client

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    def execute(self, query: str) -> str:

        logger.info(f"Agent {self.name} executing query")

        system_prompt = self.get_system_prompt()

        full_prompt = f"""
{system_prompt}

IMPORTANT RULES:
- Focus strictly on the user's query
- Maintain topic consistency
- Avoid unrelated technologies or concepts
- Prefer concise structured responses

User Query:
{query}

Response:
"""

        response = self.llm.call_llm(full_prompt)

        logger.info(f"Agent {self.name} completed execution")

        return response