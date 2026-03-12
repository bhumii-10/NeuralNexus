# NeuralNexus UI

Modern frontend dashboard for NeuralNexus multi-agent AI orchestration framework.

## Features

- 🎯 Real-time query processing
- 📊 Event timeline visualization
- 📚 Query history tracking
- 🤖 Multi-agent execution display
- 🎨 Modern dark theme UI
- ⚡ Real-time updates

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Axios** - API client

## Getting Started

### Prerequisites

- Node.js 18+ installed
- NeuralNexus backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
# Build
npm run build

# Start production server
npm start
```

## Project Structure

```
neuralnexus-ui/
├── pages/
│   ├── index.tsx          # Main dashboard page
│   ├── _app.tsx           # App wrapper
│   └── _document.tsx      # Document wrapper
├── components/
│   ├── ChatPanel.tsx      # Query results display
│   ├── EventTimeline.tsx  # Event timeline panel
│   ├── QueryHistory.tsx   # History sidebar
│   └── QueryInput.tsx     # Query input form
├── services/
│   └── api.ts             # API client
├── styles/
│   └── globals.css        # Global styles
└── public/                # Static assets
```

## API Integration

The frontend connects to the NeuralNexus backend:

- `POST /query` - Submit queries
- `GET /events` - Fetch event timeline
- `GET /history` - Fetch query history
- `GET /health` - Health check

Configure the API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features

### Query Interface
- Type queries in the input box
- Submit with Enter or click Send
- Real-time processing feedback

### Event Timeline
- Live event updates every 5 seconds
- Color-coded event types
- Timestamp tracking

### Query History
- View past queries
- Click to re-run queries
- Task count display

### Response Display
- Simple agent responses
- Multi-agent task breakdown
- Agent routing information

## Customization

### Colors
Edit `tailwind.config.js` to customize the color scheme.

### API Polling
Adjust polling intervals in components:
- Events: 5 seconds
- History: 10 seconds

## Development

```bash
# Run dev server
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint
```

## License

MIT
