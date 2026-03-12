from neuralnexus.agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="critic_agent",
            description="Reviews and improves agent responses for quality and accuracy"
        )
    
    def get_system_prompt(self) -> str:
        return """You are a Critic Agent specialized in reviewing and improving AI-generated responses.

CRITICAL VALIDATION RULES:
1. TOPIC RELEVANCE: Ensure response directly addresses the user's query
2. LOGICAL CORRECTNESS: Verify all claims are accurate and well-supported
3. LENGTH ADHERENCE: If word limit specified, enforce it strictly
4. REMOVE UNNECESSARY SECTIONS: Cut any content not directly relevant
5. TOPIC CONSISTENCY: Remove any off-topic drift or unrelated concepts

OUTPUT REQUIREMENT:
Return ONLY the improved response. Do NOT add meta-commentary about your review.
If response is off-topic, rewrite it to focus on the actual query.
If response exceeds word limit, shorten it to meet the constraint."""
    
    def review(self, original_query: str, draft_response: str) -> str:
        """Review and improve a draft response"""
        review_prompt = f"""Original Query: {original_query}

Draft Response:
{draft_response}

Review the draft response and provide an improved version that is more accurate, complete, and clear."""
        
        return self.execute(review_prompt)
