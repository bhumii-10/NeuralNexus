from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from neuralnexus.database.models import Base, Query, Task, TaskResult
from neuralnexus.config.settings import settings
from neuralnexus.utils.logger import setup_logger
from typing import List, Dict, Optional
from datetime import datetime
import pytz

logger = setup_logger(__name__)

# Asia/Kolkata timezone
IST = pytz.timezone("Asia/Kolkata")

def ensure_timezone_aware(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware (IST)"""
    if dt.tzinfo is None:
        # Naive datetime - assume it's already in IST
        return IST.localize(dt)
    return dt

class Database:
    def __init__(self, db_url: str = None):
        # Use provided URL or get from settings
        if db_url is None:
            db_url = settings.DATABASE_URL
        
        # Create engine with PostgreSQL optimizations
        self.engine = create_engine(
            db_url,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=10,        # Connection pool size
            max_overflow=20,     # Max overflow connections
            echo=False
        )
        
        # Create all tables
        Base.metadata.create_all(bind=self.engine)
        
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Log successful connection
        db_name = db_url.split('/')[-1].split('?')[0]
        logger.info(f"NeuralNexus connected to PostgreSQL database: {db_name}")
    
    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def save_query(self, query_text: str) -> int:
        """Save a query and return its ID"""
        session = self.get_session()
        try:
            query = Query(query_text=query_text)
            session.add(query)
            session.commit()
            query_id = query.id
            logger.info(f"Query saved with ID: {query_id}")
            return query_id
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save query: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_task(self, query_id: int, task_description: str, agent: str) -> int:
        """Save a task and return its ID"""
        session = self.get_session()
        try:
            task = Task(
                query_id=query_id,
                task_description=task_description,
                agent=agent
            )
            session.add(task)
            session.commit()
            task_id = task.id
            logger.info(f"Task saved with ID: {task_id}")
            return task_id
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save task: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_result(self, task_id: int, response: str):
        """Save a task result"""
        session = self.get_session()
        try:
            result = TaskResult(task_id=task_id, response=response)
            session.add(result)
            session.commit()
            logger.info(f"Result saved for task ID: {task_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save result: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_query_history(self, limit: int = 10) -> List[Dict]:
        """Get recent query history with tasks and results"""
        session = self.get_session()
        try:
            queries = session.query(Query).order_by(Query.timestamp.desc()).limit(limit).all()
            
            history = []
            for query in queries:
                # Ensure timestamp is timezone-aware
                query_timestamp = ensure_timezone_aware(query.timestamp)
                
                query_data = {
                    "id": query.id,
                    "query_text": query.query_text,
                    "timestamp": query_timestamp.isoformat(),
                    "tasks": []
                }
                
                for task in query.tasks:
                    task_data = {
                        "id": task.id,
                        "description": task.task_description,
                        "agent": task.agent,
                        "result": None
                    }
                    
                    if task.result:
                        # Ensure result timestamp is timezone-aware
                        result_timestamp = ensure_timezone_aware(task.result.timestamp)
                        
                        task_data["result"] = {
                            "response": task.result.response,
                            "timestamp": result_timestamp.isoformat()
                        }
                    
                    query_data["tasks"].append(task_data)
                
                history.append(query_data)
            
            return history
        finally:
            session.close()
    
    def delete_query(self, query_id: int):
        """Delete a query and all related tasks and results (cascade delete)"""
        session = self.get_session()
        try:
            # Get the query
            query = session.query(Query).filter(Query.id == query_id).first()
            
            if not query:
                raise ValueError(f"Query with ID {query_id} not found")
            
            # Delete related task results first
            for task in query.tasks:
                if task.result:
                    session.delete(task.result)
            
            # Delete related tasks
            for task in query.tasks:
                session.delete(task)
            
            # Delete the query
            session.delete(query)
            session.commit()
            
            logger.info(f"Query {query_id} and related data deleted successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete query {query_id}: {str(e)}")
            raise
        finally:
            session.close()

database = Database()
