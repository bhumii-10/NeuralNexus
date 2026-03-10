import React, { useEffect, useState } from 'react';
import { QueryHistory as QueryHistoryType, getHistory, deleteHistory } from '@/services/api';

interface QueryHistoryProps {
  onSelectQuery: (query: string) => void;
}

export default function QueryHistory({ onSelectQuery }: QueryHistoryProps) {
  const [history, setHistory] = useState<QueryHistoryType[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<number | null>(null);

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

  const handleDelete = async (e: React.MouseEvent, queryId: number) => {
    e.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this query?')) {
      return;
    }

    setDeletingId(queryId);
    try {
      await deleteHistory(queryId);
      await fetchHistory();
    } catch (error) {
      console.error('Failed to delete query:', error);
      alert('Failed to delete query');
    } finally {
      setDeletingId(null);
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
            className="bg-slate-700 rounded-lg p-3 hover:bg-slate-600 cursor-pointer transition-colors relative group"
          >
            <div className="text-sm text-slate-200 mb-2 line-clamp-2 pr-8">
              {item.query_text}
            </div>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>{item.tasks.length} tasks</span>
              <span>{new Date(item.timestamp).toLocaleString('en-IN', {
                timeZone: 'Asia/Kolkata',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
              })}</span>
            </div>
            <button
              onClick={(e) => handleDelete(e, item.id)}
              disabled={deletingId === item.id}
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-red-500 hover:bg-red-600 text-white rounded p-1 disabled:opacity-50"
              title="Delete query"
            >
              {deletingId === item.id ? (
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              )}
            </button>
          </div>
        ))
      )}
    </div>
  );
}
