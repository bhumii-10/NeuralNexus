from neuralnexus.agents.router_agent import RouterAgent
from neuralnexus.agents.planner_agent import PlannerAgent
from neuralnexus.agents.research_agent import ResearchAgent
from neuralnexus.agents.coding_agent import CodingAgent
from neuralnexus.agents.reasoning_agent import ReasoningAgent
from neuralnexus.agents.critic_agent import CriticAgent
from neuralnexus.agents.formatter_agent import FormatterAgent
from neuralnexus.agents.synthesizer_agent import SynthesizerAgent
from neuralnexus.event.event_bus import event_bus
from neuralnexus.memory.memory_manager import memory_manager
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.router = RouterAgent()
        self.planner = PlannerAgent()
        self.critic = CriticAgent()
        self.formatter = FormatterAgent()
        self.synthesizer = SynthesizerAgent()
        self.agents = {
            "research_agent": ResearchAgent(),
            "coding_agent": CodingAgent(),
            "reasoning_agent": ReasoningAgent()
        }
        self.planning_keywords = [
            "design", "strategy", "architecture", "plan", "build", 
            "create", "system", "roadmap", "develop", "implement",
            "launch", "establish", "construct"
        ]
        # Informational keywords that should NOT trigger planning
        self.informational_keywords = [
            "what is", "explain", "describe", "define", "how does",
            "tell me about", "what are", "who is", "when was"
        ]
    
    def _needs_planning(self, query: str) -> bool:
        """Determine if query requires multi-agent planning"""
        query_lower = query.lower()
        
        # Check if it's a simple informational query
        is_informational = any(keyword in query_lower for keyword in self.informational_keywords)
        if is_informational:
            logger.info("Informational query detected, skipping planner")
            return False
        
        # Check for planning keywords
        has_planning_keyword = any(keyword in query_lower for keyword in self.planning_keywords)
        
        # Only use planner if:
        # 1. Has planning keywords AND query is substantial (>15 words)
        # 2. OR query is very long (>25 words) suggesting complexity
        word_count = len(query.split())
        
        if has_planning_keyword and word_count > 15:
            return True
        
        if word_count > 25:
            return True
        
        return False
    
    def _refine_response(self, query: str, draft_response: str) -> str:
        """Apply critic and formatter agents to refine response quality"""
        from neuralnexus.config.settings import settings
        
        # Check if refinement is enabled
        if not settings.ENABLE_REFINEMENT:
            logger.info("Response refinement disabled, returning draft")
            return draft_response
        
        logger.info("Starting response refinement pipeline")
        
        # Step 1: Log draft generation
        event_bus.publish_event("AGENT_DRAFT_GENERATED", {
            "draft_length": len(draft_response),
            "draft_word_count": len(draft_response.split())
        })
        
        # Step 2: Critic validation
        logger.info("Applying critic agent validation")
        reviewed_response = self.critic.review(query, draft_response)
        
        event_bus.publish_event("CRITIC_VALIDATION", {
            "reviewed_length": len(reviewed_response),
            "reviewed_word_count": len(reviewed_response.split()),
            "query": query[:100]
        })
        
        # Step 3: Formatter enforcement
        logger.info("Applying formatter agent with length enforcement")
        formatted_response = self.formatter.format_response(reviewed_response)
        
        event_bus.publish_event("FORMATTER_ENFORCED_LIMITS", {
            "final_length": len(formatted_response),
            "final_word_count": len(formatted_response.split()),
            "has_word_limit": any(phrase in query.lower() for phrase in ["under", "words", "maximum"])
        })
        
        logger.info("Response refinement pipeline completed")
        return formatted_response
    
    def _execute_task(self, task: str, agent_name: str, task_id: int = None, original_query: str = None) -> dict:
        """Execute a single task with specified agent and apply refinement pipeline"""
        if agent_name not in self.agents:
            logger.warning(f"Unknown agent: {agent_name}, using research_agent")
            agent_name = "research_agent"
        
        # Publish task execution event
        event_bus.publish_event("TASK_EXECUTED", {
            "task": task,
            "agent": agent_name,
            "task_id": task_id
        })
        
        # Generate draft response
        agent = self.agents[agent_name]
        draft_response = agent.execute(task)
        
        # Apply refinement pipeline
        query_for_refinement = original_query if original_query else task
        refined_response = self._refine_response(query_for_refinement, draft_response)
        
        # Save refined result to database if task_id provided
        if task_id:
            try:
                memory_manager.save_result(task_id, refined_response)
            except Exception as e:
                logger.error(f"Failed to save result: {str(e)}")
        
        # Publish task completion event
        event_bus.publish_event("TASK_COMPLETED", {
            "task": task,
            "agent": agent_name,
            "task_id": task_id,
            "response_length": len(refined_response)
        })
        
        return {
            "task": task,
            "agent": agent_name,
            "response": refined_response
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
                result = self._execute_task(task, agent_name, task_id, query)
                results.append(result)
            
            # Synthesize multiple agent outputs into single response
            logger.info("Synthesizing multiple agent outputs")
            synthesized_response = self.synthesizer.synthesize(query, results)
            
            event_bus.publish_event("RESPONSE_SYNTHESIZED", {
                "agent_count": len(results),
                "synthesized_length": len(synthesized_response),
                "synthesized_word_count": len(synthesized_response.split())
            })
            
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
                "results": results,
                "response": synthesized_response
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
            
            # Generate draft response
            draft_response = agent.execute(query)
            
            # Apply refinement pipeline
            refined_response = self._refine_response(query, draft_response)
            
            # Save refined result
            if task_id:
                try:
                    memory_manager.save_result(task_id, refined_response)
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
                "response": refined_response
            }

orchestrator = Orchestrator()
