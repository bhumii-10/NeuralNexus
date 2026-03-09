import React from 'react';
import { QueryResponse } from '@/services/api';

interface ChatPanelProps {
  response: QueryResponse | null;
  loading: boolean;
}

export default function ChatPanel({ response, loading }: ChatPanelProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Processing your query...</p>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-slate-400">
          <svg className="w-16 h-16 mx-auto mb-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <p className="text-lg">Ask a question to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Agent Info */}
      <div className="bg-slate-700 rounded-lg p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-slate-400">Agent</span>
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${
            response.agent === 'multi_agent_execution' 
              ? 'bg-purple-500/20 text-purple-300'
              : 'bg-blue-500/20 text-blue-300'
          }`}>
            {response.agent.replace('_', ' ').toUpperCase()}
          </span>
        </div>
        {response.planning_used && (
          <div className="text-sm text-slate-300">
            <span className="text-green-400">✓</span> Multi-agent planning used
          </div>
        )}
        {response.routing_reason && (
          <div className="text-sm text-slate-400 mt-2">
            {response.routing_reason}
          </div>
        )}
      </div>

      {/* Simple Response */}
      {response.response && (
        <div className="bg-slate-700 rounded-lg p-4">
          <h3 className="text-sm font-medium text-slate-300 mb-2">Response</h3>
          <div className="text-slate-100 whitespace-pre-wrap">{response.response}</div>
        </div>
      )}

      {/* Multi-Agent Results */}
      {response.results && response.results.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-slate-300">Task Results</h3>
          {response.results.map((result, index) => (
            <div key={index} className="bg-slate-700 rounded-lg p-4">
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="text-sm font-medium text-slate-200 mb-1">
                    {result.task}
                  </div>
                  <div className="text-xs text-slate-400">
                    Agent: <span className="text-primary-400">{result.agent}</span>
                  </div>
                </div>
              </div>
              <div className="mt-3 text-sm text-slate-300 whitespace-pre-wrap">
                {result.response}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
