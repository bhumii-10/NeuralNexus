# NeuralNexus UI - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd neuralnexus-ui
npm install
```

### 2. Configure Environment

The `.env.local` file is already created with:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If your backend runs on a different port, update this file.

### 3. Start Development Server

```bash
npm run dev
```

The UI will be available at: http://localhost:3000

## Prerequisites

✅ Node.js 18 or higher
✅ npm or yarn
✅ NeuralNexus backend running on port 8000

## Verify Backend Connection

Before starting the UI, ensure the backend is running:

```bash
# Test backend health
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Project Structure

```
neuralnexus-ui/
├── pages/
│   ├── index.tsx              # Main dashboard
│   ├── _app.tsx               # App configuration
│   └── _document.tsx          # HTML document
│
├── components/
│   ├── ChatPanel.tsx          # Query results display
│   ├── EventTimeline.tsx      # Real-time events
│   ├── QueryHistory.tsx       # Past queries
│   └── QueryInput.tsx         # Query input form
│
├── services/
│   └── api.ts                 # API client functions
│
├── styles/
│   └── globals.css            # Global styles
│
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── tailwind.config.js         # Tailwind config
├── next.config.js             # Next.js config
└── .env.local                 # Environment variables
```

## Available Scripts

```bash
# Development
npm run dev          # Start dev server (port 3000)

# Production
npm run build        # Build for production
npm start            # Start production server

# Utilities
npm run lint         # Run ESLint
```

## Features

### 1. Query Interface
- Submit queries to NeuralNexus
- Real-time processing feedback
- Error handling

### 2. Event Timeline (Right Panel)
- Live event updates every 5 seconds
- Color-coded event types:
  - 💬 USER_QUERY (Blue)
  - 📝 TASK_CREATED (Yellow)
  - ⚡ TASK_EXECUTED (Purple)
  - ✅ TASK_COMPLETED (Green)
  - 🤖 AGENT_RESPONSE (Cyan)

### 3. Query History (Left Panel)
- View past queries
- Click to re-run
- Shows task count
- Auto-refreshes every 10 seconds

### 4. Response Display (Center Panel)
- Simple agent responses
- Multi-agent task breakdown
- Agent routing information
- Task execution results

## Customization

### Change API URL

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://your-backend-url:port
```

### Adjust Polling Intervals

Edit component files:

**EventTimeline.tsx** (line 15):
```typescript
const interval = setInterval(fetchEvents, 5000); // 5 seconds
```

**QueryHistory.tsx** (line 23):
```typescript
const interval = setInterval(fetchHistory, 10000); // 10 seconds
```

### Customize Colors

Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9', // Change primary color
        // ... other shades
      },
    },
  },
}
```

## Troubleshooting

### Port 3000 Already in Use

```bash
# Use different port
PORT=3001 npm run dev
```

### Backend Connection Failed

1. Check backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verify `.env.local` has correct URL

3. Check CORS settings in backend

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

## Production Deployment

### Build

```bash
npm run build
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Other Platforms

The built files are in `.next/` directory. Use:
```bash
npm start
```

Or deploy as static site:
```bash
npm run build
npm run export
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Performance

- Initial load: ~500ms
- Event updates: Every 5s
- History updates: Every 10s
- Query response: Depends on backend

## Security

- API calls use environment variables
- No sensitive data in client code
- HTTPS recommended for production

## Support

For issues or questions:
1. Check backend logs
2. Check browser console
3. Verify API connectivity
4. Review component error states
