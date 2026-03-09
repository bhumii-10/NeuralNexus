from neuralnexus.agents.router_agent import RouterAgent
from neuralnexus.agents.planner_agent import PlannerAgent
from neuralnexus.agents.research_agent import ResearchAgent
from neuralnexus.agents.coding_agent import CodingAgent
from neuralnexus.agents.reasoning_agent import ReasoningAgent
from neuralnexus.event.event_bus import event_bus
from neuralnexus.memory.memory_manager import memory_manager
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.router = RouterAgent()
        self.planner = PlannerAgent()
        self.agents = {
            "research_agent": ResearchAgent(),
            "coding_agent": CodingAgent(),
            "reasoning_agent": ReasoningAgent()
        }
        self.planning_keywords = [
            "plan", "strategy", "design", "build", "create", "launch"
        ]
    
    def _needs_planning(self, query: str) -> bool:
        """Determine if query requires multi-agent planning"""
        word_count = len(query.split())
        has_keyword = any(keyword in query.lower() for keyword in self.planning_keywords)
        
        return word_count > 12 or has_keyword
    
    def _execute_task(self, task: str, agent_name: str, task_id: int = None) -> dict:
        """Execute a single task with specified agent"""
        if agent_name not in self.agents:
            logger.warning(f"Unknown agent: {agent_name}, using research_agent")
            agent_name = "research_agent"
        
        # Publish task execution event
        event_bus.publish_event("TASK_EXECUTED", {
            "task": task,
            "agent": agent_name,
            "task_id": task_id
        })
        
        agent = self.agents[agent_name]
        response = agent.execute(task)
        
        # Save result to database if task_id provided
        if task_id:
            try:
                memory_manager.save_result(task_id, response)
            except Exception as e:
                logger.error(f"Failed to save result: {str(e)}")
        
        # Publish task completion event
        event_bus.publish_event("TASK_COMPLETED", {
            "task": task,
            "agent": agent_name,
            "task_id": task_id,
            "response_length": len(response)
        })
        
        return {
            "task": task,
            "agent": agent_name,
            "response": response
        }
    
    def process_query(self, query: str) -> dict:
        logger.info(f"Processing query: {query[:50]}...")
        
        # Publish user query event
        event_bus.publish_event("USER_QUERY", {"query": query})
        
        # Save query to database
        try:
            query_id = memory_manager.save_query(query)
        except Exception as e:
            logger.error(f"Failed to save query to database: {str(e)}")
            query_id = None
        
        # Check if planning is needed
        if self._needs_planning(query):
            logger.info("Complex query detected, using planner agent")
            
            # Get task plan
            plan = self.planner.plan(query)
            tasks = plan.get("tasks", [])
            
            logger.info(f"Executing {len(tasks)} tasks")
            
            # Execute each task
            results = []
            for task_info in tasks:
                task = task_info.get("task", "")
                agent_name = task_info.get("agent", "research_agent")
                
                # Save task to database
                task_id = None
                if query_id:
                    try:
                        task_id = memory_manager.save_task(query_id, task, agent_name)
                        event_bus.publish_event("TASK_CREATED", {
                            "task": task,
                            "agent": agent_name,
                            "task_id": task_id,
                            "query_id": query_id
                        })
                    except Exception as e:
                        logger.error(f"Failed to save task: {str(e)}")
                
                logger.info(f"Executing task: {task[:50]}... with {agent_name}")
                result = self._execute_task(task, agent_name, task_id)
                results.append(result)
            
            # Publish agent response event
            event_bus.publish_event("AGENT_RESPONSE", {
                "mode": "multi_agent",
                "task_count": len(tasks),
                "query_id": query_id
            })
            
            return {
                "agent": "multi_agent_execution",
                "planning_used": True,
                "tasks": tasks,
                "results": results
            }
        
        else:
            # Simple query - use router agent
            logger.info("Simple query, using router agent")
            
            routing_decision = self.router.route(query)
            selected_agent_name = routing_decision["agent"]
            
            logger.info(f"Routed to: {selected_agent_name}")
            
            if selected_agent_name not in self.agents:
                logger.warning(f"Unknown agent: {selected_agent_name}, using research_agent")
                selected_agent_name = "research_agent"
            
            # Save as single task
            task_id = None
            if query_id:
                try:
                    task_id = memory_manager.save_task(query_id, query, selected_agent_name)
                    event_bus.publish_event("TASK_CREATED", {
                        "task": query,
                        "agent": selected_agent_name,
                        "task_id": task_id,
                        "query_id": query_id
                    })
                except Exception as e:
                    logger.error(f"Failed to save task: {str(e)}")
            
            agent = self.agents[selected_agent_name]
            
            # Publish task execution event
            event_bus.publish_event("TASK_EXECUTED", {
                "task": query,
                "agent": selected_agent_name,
                "task_id": task_id
            })
            
            response = agent.execute(query)
            
            # Save result
            if task_id:
                try:
                    memory_manager.save_result(task_id, response)
                except Exception as e:
                    logger.error(f"Failed to save result: {str(e)}")
            
            # Publish completion events
            event_bus.publish_event("TASK_COMPLETED", {
                "task": query,
                "agent": selected_agent_name,
                "task_id": task_id
            })
            
            event_bus.publish_event("AGENT_RESPONSE", {
                "mode": "single_agent",
                "agent": selected_agent_name,
                "query_id": query_id
            })
            
            return {
                "agent": selected_agent_name,
                "planning_used": False,
                "routing_reason": routing_decision["reason"],
                "response": response
            }

orchestrator = Orchestrator()
