import React, { useEffect, useState } from 'react';
import { QueryHistory as QueryHistoryType, getHistory } from '@/services/api';

interface QueryHistoryProps {
  onSelectQuery: (query: string) => void;
}

export default function QueryHistory({ onSelectQuery }: QueryHistoryProps) {
  const [history, setHistory] = useState<QueryHistoryType[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const data = await getHistory(20);
      setHistory(data.history);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
    const interval = setInterval(fetchHistory, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {history.length === 0 ? (
        <div className="text-center text-slate-400 py-8">
          No history yet
        </div>
      ) : (
        history.map((item) => (
          <div
            key={item.id}
            onClick={() => onSelectQuery(item.query_text)}
            className="bg-slate-700 rounded-lg p-3 hover:bg-slate-600 cursor-pointer transition-colors"
          >
            <div className="text-sm text-slate-200 mb-2 line-clamp-2">
              {item.query_text}
            </div>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>{item.tasks.length} tasks</span>
              <span>{new Date(item.timestamp).toLocaleDateString()}</span>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
