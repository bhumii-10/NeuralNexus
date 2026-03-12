import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { QueryResponse } from "@/services/api";

interface Message {
  role: "user" | "assistant";
  query?: string;
  response?: QueryResponse;
}

interface ChatPanelProps {
  messages: Message[];
  loading: boolean;
}

export default function ChatPanel({ messages, loading }: ChatPanelProps) {

  const [showDetailsIndex, setShowDetailsIndex] = useState<number | null>(null);

  if (messages.length === 0 && !loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-slate-400">Ask a question to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {messages.map((msg, index) => {

        if (msg.role === "user") {

          return (
            <div key={index} className="flex justify-end">
              <div className="bg-slate-900 border border-slate-700 text-white px-4 py-3 rounded-lg max-w-xl shadow">
                {msg.query}
              </div>
            </div>
          );

        }

        const response = msg.response;

        if (!response) return null;

        return (

          <div key={index} className="space-y-4">

            {/* Agent Info */}
            <div className="bg-slate-700 rounded-lg p-4">

              <div className="flex items-center justify-between mb-2">

                <span className="text-sm text-slate-400">Agent</span>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${
                    response.agent === "multi_agent_execution"
                      ? "bg-purple-500/20 text-purple-300"
                      : "bg-blue-500/20 text-blue-300"
                  }`}
                >
                  {response.agent.replace("_", " ").toUpperCase()}
                </span>

              </div>

              {response.planning_used && (
                <div className="text-sm text-slate-300">
                  ✓ Multi-agent planning used
                </div>
              )}

            </div>

            {/* Synthesized Response */}
            {response.planning_used && response.response && (

              <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 rounded-xl p-6 border border-purple-500/30 shadow-lg">

                <div className="flex items-center justify-between mb-4">

                  <h3 className="text-lg font-semibold text-purple-200">
                    Synthesized Response
                  </h3>

                  {response.results && (

                    <button
                      onClick={() =>
                        setShowDetailsIndex(
                          showDetailsIndex === index ? null : index
                        )
                      }
                      className="text-xs px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded-full"
                    >
                      {showDetailsIndex === index
                        ? "Hide Details"
                        : "Show Details"}
                    </button>

                  )}

                </div>

                <div className="prose prose-invert max-w-none">
                  <ReactMarkdown>{response.response}</ReactMarkdown>
                </div>

              </div>

            )}

            {/* Simple Response */}
            {!response.planning_used && response.response && (

              <div className="bg-slate-700 rounded-lg p-6">

                <h3 className="text-lg font-semibold text-slate-200 mb-4 border-b border-slate-600 pb-2">
                  Response
                </h3>

                <div className="prose prose-invert max-w-none">
                  <ReactMarkdown>{response.response}</ReactMarkdown>
                </div>

              </div>

            )}

            {/* Agent Details */}
            {response.results && showDetailsIndex === index && (

              <div className="bg-slate-700 rounded-lg overflow-hidden">

                <div className="bg-slate-800 p-4 border-b border-slate-600">

                  <h3 className="text-sm font-semibold text-slate-300">
                    Agent Execution Details ({response.results.length})
                  </h3>

                </div>

                <div className="p-4 space-y-3">

                  {response.results.map((result, i) => (

                    <div
                      key={i}
                      className="bg-slate-800 rounded-lg p-4 border border-slate-700"
                    >

                      <div className="text-sm font-medium text-slate-200 mb-1">
                        Task {i + 1}: {result.task}
                      </div>

                      <div className="text-xs text-slate-400 mb-2">
                        Agent: {result.agent}
                      </div>

                      <div className="prose prose-invert prose-sm max-w-none">
                        <ReactMarkdown>{result.response}</ReactMarkdown>
                      </div>

                    </div>

                  ))}

                </div>

              </div>

            )}

          </div>

        );

      })}

      {loading && (
        <div className="text-slate-400">Processing...</div>
      )}

    </div>
  );
}