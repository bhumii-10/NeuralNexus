import React, { useEffect, useState } from 'react';
import { Event, getEvents } from '@/services/api';

export default function EventTimeline() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchEvents = async () => {
    try {
      const data = await getEvents(50);
      setEvents(data.events.reverse());
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 5000);
    return () => clearInterval(interval);
  }, []);

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'USER_QUERY':
        return '💬';
      case 'TASK_CREATED':
        return '📝';
      case 'TASK_EXECUTED':
        return '⚡';
      case 'TASK_COMPLETED':
        return '✅';
      case 'AGENT_RESPONSE':
        return '🤖';
      default:
        return '📌';
    }
  };

  const getEventColor = (eventType: string) => {
    switch (eventType) {
      case 'USER_QUERY':
        return 'bg-blue-500/20 text-blue-300';
      case 'TASK_CREATED':
        return 'bg-yellow-500/20 text-yellow-300';
      case 'TASK_EXECUTED':
        return 'bg-purple-500/20 text-purple-300';
      case 'TASK_COMPLETED':
        return 'bg-green-500/20 text-green-300';
      case 'AGENT_RESPONSE':
        return 'bg-cyan-500/20 text-cyan-300';
      default:
        return 'bg-slate-500/20 text-slate-300';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {events.length === 0 ? (
        <div className="text-center text-slate-400 py-8">
          No events yet
        </div>
      ) : (
        events.map((event, index) => (
          <div key={index} className="bg-slate-700 rounded-lg p-3 hover:bg-slate-600 transition-colors">
            <div className="flex items-start gap-3">
              <span className="text-2xl">{getEventIcon(event.event_type)}</span>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${getEventColor(event.event_type)}`}>
                    {event.event_type.replace('_', ' ')}
                  </span>
                </div>
                <div className="text-xs text-slate-400">
                  {new Date(event.timestamp).toLocaleString('en-IN', {
                    timeZone: 'Asia/Kolkata',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: true
                  })}
                </div>
                {event.data.task && (
                  <div className="text-sm text-slate-300 mt-1 truncate">
                    {event.data.task}
                  </div>
                )}
                {event.data.agent && (
                  <div className="text-xs text-slate-400 mt-1">
                    Agent: {event.data.agent}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
