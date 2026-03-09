from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Query(Base):
    __tablename__ = 'queries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="query", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(Integer, ForeignKey('queries.id'), nullable=False)
    task_description = Column(Text, nullable=False)
    agent = Column(String(100), nullable=False)
    
    query = relationship("Query", back_populates="tasks")
    result = relationship("TaskResult", back_populates="task", uselist=False, cascade="all, delete-orphan")

class TaskResult(Base):
    __tablename__ = 'task_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    task = relationship("Task", back_populates="result")
