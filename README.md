# NeuralNexus

A production-ready, domain-agnostic multi-agent AI orchestration framework that intelligently routes queries to specialized agents and coordinates complex task execution.

## Overview

NeuralNexus is a sophisticated AI collaboration system that leverages multiple specialized agents to handle diverse queries. The system automatically determines whether to use a single agent or orchestrate multiple agents for complex tasks, providing a seamless and intelligent query processing experience.

## Architecture

```
┌─────────────────────────────────────────┐
│         Next.js Frontend                │
│      (React + TailwindCSS)              │
└────────────────┬────────────────────────┘
                 │ REST API
┌────────────────▼────────────────────────┐
│         FastAPI Backend                 │
│  ┌──────────────────────────────────┐   │
│  │  Router Agent → Planner Agent    │   │
│  │  ↓                               │   │
│  │  Specialized Agents:             │   │
│  │  • Research Agent                │   │
│  │  • Coding Agent                  │   │
│  │  • Reasoning Agent               │   │
│  └──────────────────────────────────┘   │
│                                         │
│  Infrastructure:                        │
│  • Event Timeline System                │
│  • PostgreSQL Database                  │
│  • Memory Management                    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      PostgreSQL Database                │
│  • Queries  • Tasks  • Results          │
└─────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      LLM Provider (OpenAI-compatible)   │
│  OpenAI / Groq / DeepSeek / etc.        │
└─────────────────────────────────────────┘
```

## Key Features

### Intelligent Query Routing
- **Router Agent**: Analyzes queries and routes to appropriate specialized agents
- **Planner Agent**: Decomposes complex queries into multiple coordinated tasks
- **Automatic Mode Selection**: Simple queries use single agents, complex queries trigger multi-agent planning

### Specialized Agents
- **Research Agent**: Handles factual questions, knowledge queries, and explanations
- **Coding Agent**: Manages programming tasks, code generation, and debugging
- **Reasoning Agent**: Performs logical analysis, planning, and strategic thinking

### Infrastructure
- **Event Timeline**: Real-time tracking of all system events
- **PostgreSQL Database**: Persistent storage of queries, tasks, and results
- **Memory Management**: Intelligent context and history management
- **RESTful API**: Clean, well-documented endpoints

### Modern Frontend
- **Real-time Dashboard**: Live event tracking and query history
- **Three-Panel Layout**: History, chat interface, and event timeline
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Modern, professional UI

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Production-grade relational database
- **Pydantic**: Data validation and settings management

### Frontend
- **Next.js 14**: React framework with server-side rendering
- **TypeScript**: Type-safe JavaScript
- **TailwindCSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

### AI/ML
- **OpenAI-compatible API**: Works with OpenAI, Groq, DeepSeek, and other providers
- **Multi-agent Architecture**: Coordinated AI agent collaboration

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- OpenAI-compatible API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhumii-10/NeuralNexus.git
   cd NeuralNexus
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE neuralnexus;
   ```

6. **Update .env file**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/neuralnexus
   OPENAI_API_KEY=your_api_key_here
   MODEL_NAME=gpt-4
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd neuralnexus-ui
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   # .env.local is already configured for localhost:8000
   ```

## Running the Application

### Start Backend Server

```bash
# From project root
uvicorn neuralnexus.api.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: http://localhost:8000

### Start Frontend Server

```bash
# From neuralnexus-ui directory
npm run dev
```

The frontend will be available at: http://localhost:3000

## API Endpoints

### Core Endpoints

**POST /query**
- Submit a query for processing
- Request: `{"query": "your question"}`
- Response: Agent selection, tasks, and results

**GET /events**
- Retrieve event timeline
- Query params: `limit` (default: 100)
- Response: List of system events

**GET /history**
- Retrieve query history
- Query params: `limit` (default: 10)
- Response: Past queries with tasks and results

**GET /health**
- Health check endpoint
- Response: `{"status": "healthy"}`

### API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage Examples

### Simple Queries (Single Agent)
```
"What is machine learning?"
"Explain recursion"
"What is Python?"
```

### Complex Queries (Multi-Agent Planning)
```
"Create a plan to build a web application"
"Design a microservices architecture"
"Develop a startup launch strategy"
```

### Coding Queries
```
"Write a Python function to sort a list"
"Create a REST API endpoint"
"Debug this code: [paste code]"
```

## Database Schema

### Tables

**queries**
- `id`: Primary key
- `query_text`: User query
- `timestamp`: Creation time

**tasks**
- `id`: Primary key
- `query_id`: Foreign key to queries
- `task_description`: Task details
- `agent`: Assigned agent name

**task_results**
- `id`: Primary key
- `task_id`: Foreign key to tasks
- `response`: Agent response
- `timestamp`: Completion time

## Configuration

### Environment Variables

**Required:**
- `OPENAI_API_KEY`: Your LLM provider API key
- `DATABASE_URL`: PostgreSQL connection string

**Optional:**
- `OPENAI_BASE_URL`: LLM provider endpoint (default: OpenAI)
- `MODEL_NAME`: Model to use (default: gpt-4)
- `TEMPERATURE`: Response randomness (default: 0.7)
- `MAX_TOKENS`: Maximum response length (default: 1000)

### Supported LLM Providers

**OpenAI**
```env
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4
```

**Groq**
```env
OPENAI_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
```

**DeepSeek**
```env
OPENAI_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
```

## Development

### Project Structure

```
NeuralNexus/
├── neuralnexus/              # Backend application
│   ├── agents/               # AI agents
│   │   ├── base_agent.py
│   │   ├── router_agent.py
│   │   ├── planner_agent.py
│   │   ├── research_agent.py
│   │   ├── coding_agent.py
│   │   └── reasoning_agent.py
│   ├── api/                  # FastAPI endpoints
│   │   └── main.py
│   ├── database/             # Database layer
│   │   ├── db.py
│   │   └── models.py
│   ├── event/                # Event system
│   │   └── event_bus.py
│   ├── memory/               # Memory management
│   │   └── memory_manager.py
│   ├── orchestrator/         # Orchestration logic
│   │   └── router.py
│   ├── config/               # Configuration
│   │   └── settings.py
│   └── utils/                # Utilities
│       └── logger.py
│
├── neuralnexus-ui/           # Frontend application
│   ├── pages/                # Next.js pages
│   ├── components/           # React components
│   ├── services/             # API client
│   └── styles/               # CSS styles
│
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

### Adding New Agents

1. Create agent class in `neuralnexus/agents/`
2. Inherit from `BaseAgent`
3. Implement `get_system_prompt()` method
4. Register in `orchestrator/router.py`

Example:
```python
from neuralnexus.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="custom_agent",
            description="Your agent description"
        )
    
    def get_system_prompt(self) -> str:
        return "Your system prompt..."
```

## Testing

### Backend Tests
```bash
# Health check
curl http://localhost:8000/health

# Submit query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AI?"}'
```

### Frontend Tests
1. Open http://localhost:3000
2. Submit a query
3. Verify response display
4. Check event timeline
5. View query history

## Deployment

### Backend Deployment

**Docker:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "neuralnexus.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Production Server:**
```bash
gunicorn neuralnexus.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment

**Vercel:**
```bash
cd neuralnexus-ui
vercel
```

**Docker:**
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## Performance

- **Query Processing**: 2-5 seconds (simple), 10-30 seconds (complex)
- **Database Operations**: <10ms per operation
- **Connection Pool**: 10 base + 20 overflow connections
- **Event Updates**: Real-time (5s polling)

## Security

- ✅ Environment variables for secrets
- ✅ PostgreSQL with connection pooling
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Error handling and logging

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- Next.js for the powerful React framework
- OpenAI and other LLM providers for AI capabilities
- The open-source community

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/bhumii-10/NeuralNexus/issues
- Documentation: See README.md and code comments

## Roadmap

- [ ] WebSocket support for real-time updates
- [ ] User authentication and authorization
- [ ] Agent performance analytics
- [ ] Custom agent marketplace
- [ ] Multi-language support
- [ ] Advanced query optimization
- [ ] Distributed task execution

---

**Built with ❤️ by the NeuralNexus Team**
