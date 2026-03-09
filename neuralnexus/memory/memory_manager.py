from typing import List, Dict
from neuralnexus.utils.logger import setup_logger
from neuralnexus.database.db import database

logger = setup_logger(__name__)

class MemoryManager:
    """Enhanced memory management with database persistence"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
    
    def add_interaction(self, query: str, agent: str, response: str):
        """Add interaction to in-memory history"""
        self.conversation_history.append({
            "query": query,
            "agent": agent,
            "response": response
        })
        logger.info(f"Stored interaction in memory (total: {len(self.conversation_history)})")
    
    def save_query(self, query_text: str) -> int:
        """Save query to database and return query ID"""
        try:
            query_id = database.save_query(query_text)
            logger.info(f"Query saved to database with ID: {query_id}")
            return query_id
        except Exception as e:
            logger.error(f"Failed to save query: {str(e)}")
            raise
    
    def save_task(self, query_id: int, task_description: str, agent: str) -> int:
        """Save task to database and return task ID"""
        try:
            task_id = database.save_task(query_id, task_description, agent)
            logger.info(f"Task saved to database with ID: {task_id}")
            return task_id
        except Exception as e:
            logger.error(f"Failed to save task: {str(e)}")
            raise
    
    def save_result(self, task_id: int, response: str):
        """Save task result to database"""
        try:
            database.save_result(task_id, response)
            logger.info(f"Result saved to database for task ID: {task_id}")
        except Exception as e:
            logger.error(f"Failed to save result: {str(e)}")
            raise
    
    def get_query_history(self, limit: int = 10) -> List[Dict]:
        """Get query history from database"""
        try:
            history = database.get_query_history(limit)
            logger.info(f"Retrieved {len(history)} queries from history")
            return history
        except Exception as e:
            logger.error(f"Failed to get query history: {str(e)}")
            return []
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get in-memory conversation history"""
        return self.conversation_history[-limit:]
    
    def clear(self):
        """Clear in-memory history"""
        self.conversation_history.clear()
        logger.info("Memory cleared")

memory_manager = MemoryManager()
