from openai import OpenAI
from neuralnexus.config.settings import settings
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
    
    def call_llm(self, prompt: str, temperature: float = None) -> str:
        try:
            logger.info(f"Calling LLM with model: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens
            )
            
            result = response.choices[0].message.content
            logger.info("LLM call successful")
            return result
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise

llm_client = LLMClient()
