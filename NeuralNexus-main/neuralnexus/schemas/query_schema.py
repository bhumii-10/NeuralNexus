from pydantic import BaseModel, Field
from typing import Optional, List


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query to process")
    context: Optional[str] = Field(
        None,
        description="Conversation context from previous chat messages"
    )


class TaskResult(BaseModel):
    task: str = Field(..., description="Task description")
    agent: str = Field(..., description="Agent that executed the task")
    response: str = Field(..., description="Task execution response")


class QueryResponse(BaseModel):
    agent: str = Field(..., description="Agent or execution mode used")
    planning_used: bool = Field(..., description="Whether multi-agent planning was used")
    routing_reason: Optional[str] = Field(None, description="Routing reason for simple queries")
    response: Optional[str] = Field(None, description="Response for simple queries")
    tasks: Optional[List[dict]] = Field(None, description="Task list for multi-agent execution")
    results: Optional[List[TaskResult]] = Field(None, description="Results for multi-agent execution")