import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { QueryResponse } from '@/services/api';

interface ChatPanelProps {
  response: QueryResponse | null;
  loading: boolean;
}

export default function ChatPanel({ response, loading }: ChatPanelProps) {
  const [showDetails, setShowDetails] = useState(false);

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
      {response.response && !response.planning_used && (
        <div className="bg-slate-700 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-slate-200 mb-4 border-b border-slate-600 pb-2">Response</h3>
          <div className="prose prose-invert prose-slate max-w-none">
            <ReactMarkdown
              components={{
                h1: ({node, ...props}) => <h1 className="text-xl font-bold text-slate-100 mb-3" {...props} />,
                h2: ({node, ...props}) => <h2 className="text-lg font-semibold text-slate-200 mb-2 mt-4" {...props} />,
                h3: ({node, ...props}) => <h3 className="text-base font-medium text-slate-300 mb-2 mt-3" {...props} />,
                p: ({node, ...props}) => <p className="text-slate-100 mb-3 leading-relaxed" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-1 mb-3 text-slate-100" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal list-inside space-y-1 mb-3 text-slate-100" {...props} />,
                li: ({node, ...props}) => <li className="text-slate-100 ml-2" {...props} />,
                code: ({node, inline, ...props}: any) => 
                  inline ? 
                    <code className="bg-slate-800 px-1.5 py-0.5 rounded text-sm text-purple-300" {...props} /> :
                    <code className="block bg-slate-800 p-3 rounded text-sm text-slate-100 overflow-x-auto" {...props} />,
                strong: ({node, ...props}) => <strong className="font-semibold text-slate-50" {...props} />,
              }}
            >
              {response.response}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {/* Synthesized Response for Multi-Agent */}
      {response.response && response.planning_used && (
        <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 rounded-xl p-6 border border-purple-500/30 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-purple-200 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Synthesized Response
            </h3>
            {response.results && response.results.length > 0 && (
              <button
                onClick={() => setShowDetails(!showDetails)}
                className="text-xs px-3 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-full transition-colors"
              >
                {showDetails ? 'Hide' : 'Show'} Details
              </button>
            )}
          </div>
          <div className="prose prose-invert prose-slate max-w-none">
            <ReactMarkdown
              components={{
                h1: ({node, ...props}) => <h1 className="text-xl font-bold text-purple-100 mb-3" {...props} />,
                h2: ({node, ...props}) => <h2 className="text-lg font-semibold text-purple-200 mb-2 mt-4" {...props} />,
                h3: ({node, ...props}) => <h3 className="text-base font-medium text-purple-300 mb-2 mt-3" {...props} />,
                p: ({node, ...props}) => <p className="text-slate-100 mb-3 leading-relaxed" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-2 mb-3 text-slate-100" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal list-inside space-y-2 mb-3 text-slate-100" {...props} />,
                li: ({node, ...props}) => <li className="text-slate-100 ml-2 leading-relaxed" {...props} />,
                code: ({node, inline, ...props}: any) => 
                  inline ? 
                    <code className="bg-purple-900/50 px-1.5 py-0.5 rounded text-sm text-purple-200" {...props} /> :
                    <code className="block bg-slate-800 p-3 rounded text-sm text-slate-100 overflow-x-auto" {...props} />,
                strong: ({node, ...props}) => <strong className="font-semibold text-purple-100" {...props} />,
              }}
            >
              {response.response}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {/* Multi-Agent Results - Collapsible */}
      {response.results && response.results.length > 0 && showDetails && (
        <div className="bg-slate-700 rounded-lg overflow-hidden">
          <div className="bg-slate-800 p-4 border-b border-slate-600">
            <h3 className="text-sm font-semibold text-slate-300">
              Agent Execution Details ({response.results.length} tasks)
            </h3>
          </div>
          <div className="p-4 space-y-3">
            {response.results.map((result, index) => (
              <div key={index} className="bg-slate-800 rounded-lg p-4 border border-slate-700">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="text-sm font-medium text-slate-200 mb-1">
                      Task {index + 1}: {result.task}
                    </div>
                    <div className="text-xs text-slate-400">
                      Agent: <span className="text-primary-400 font-medium">{result.agent}</span>
                    </div>
                  </div>
                </div>
                <div className="prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown
                    components={{
                      p: ({node, ...props}) => <p className="text-slate-300 mb-2 text-sm leading-relaxed" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm" {...props} />,
                      li: ({node, ...props}) => <li className="text-slate-300 ml-2" {...props} />,
                      code: ({node, inline, ...props}: any) => 
                        inline ? 
                          <code className="bg-slate-900 px-1 py-0.5 rounded text-xs text-purple-300" {...props} /> :
                          <code className="block bg-slate-900 p-2 rounded text-xs text-slate-100 overflow-x-auto" {...props} />,
                    }}
                  >
                    {result.response}
                  </ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
