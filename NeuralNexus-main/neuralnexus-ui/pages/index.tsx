import React, { useState } from "react";
import Head from "next/head";
import QueryInput from "@/components/QueryInput";
import ChatPanel from "@/components/ChatPanel";
import EventTimeline from "@/components/EventTimeline";
import QueryHistory from "@/components/QueryHistory";
import { QueryResponse, sendQuery } from "@/services/api";

interface Message {
  role: "user" | "assistant";
  query?: string;
  response?: QueryResponse;
}

export default function Home() {

  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /* =========================
     BUILD CONTEXT FROM CHAT
  ========================= */

  const buildContext = () => {

    let context = "";

    messages.forEach((msg) => {

      if (msg.role === "user" && msg.query) {
        context += `User: ${msg.query}\n`;
      }

      if (msg.role === "assistant" && msg.response?.response) {
        context += `Assistant: ${msg.response.response}\n`;
      }

    });

    return context;

  };

  /* =========================
     SUBMIT QUERY
  ========================= */

  const handleSubmitQuery = async (query: string) => {

    setLoading(true);
    setError(null);

    const userMessage: Message = {
      role: "user",
      query: query
    };

    setMessages(prev => [...prev, userMessage]);

    try {

      const context = buildContext();

      const result = await sendQuery(query, context);

      const assistantMessage: Message = {
        role: "assistant",
        response: result
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (err: any) {

      setError(err.message || "Failed to process query");

    } finally {

      setLoading(false);

    }
  };

  const handleSelectHistoryQuery = (query: string) => {
    handleSubmitQuery(query);
  };

  const handleNewChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <>
      <Head>
        <title>NeuralNexus - Multi-Agent AI Orchestration</title>
      </Head>

      <main className="min-h-screen bg-slate-900 text-white">

        {/* HEADER */}
        <header className="bg-slate-800 border-b border-slate-700">

          <div className="container mx-auto px-4 py-4">

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">

                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">🧠</span>
                </div>

                <div>
                  <h1 className="text-2xl font-bold">NeuralNexus</h1>
                  <p className="text-sm text-slate-400">
                    Multi-Agent AI Orchestration
                  </p>
                </div>

              </div>

              <div className="flex items-center gap-4">

                <button
                  onClick={handleNewChat}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded-lg text-sm font-medium"
                >
                  + New Chat
                </button>

                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-slate-400">Online</span>
                </div>

              </div>

            </div>

          </div>

        </header>


        {/* MAIN LAYOUT */}
        <div className="container mx-auto px-4 py-6">

          <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">

            {/* HISTORY */}
            <div className="col-span-3 bg-slate-800 rounded-lg p-4 overflow-hidden flex flex-col">

              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                📚 Query History
              </h2>

              <div className="flex-1 overflow-y-auto">
                <QueryHistory onSelectQuery={handleSelectHistoryQuery} />
              </div>

            </div>


            {/* CHAT */}
            <div className="col-span-6 bg-slate-800 rounded-lg p-6 flex flex-col">

              <div className="flex-1 overflow-y-auto mb-4">

                {error && (
                  <div className="bg-red-500/20 border border-red-500 text-red-300 rounded-lg p-4 mb-4">
                    <p className="font-medium">Error</p>
                    <p className="text-sm">{error}</p>
                  </div>
                )}

                <ChatPanel
                  messages={messages}
                  loading={loading}
                />

              </div>

              <div className="border-t border-slate-700 pt-4">

                <QueryInput
                  onSubmit={handleSubmitQuery}
                  loading={loading}
                />

              </div>

            </div>


            {/* EVENTS */}
            <div className="col-span-3 bg-slate-800 rounded-lg p-4 overflow-hidden flex flex-col">

              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                ⚡ Event Timeline
              </h2>

              <div className="flex-1 overflow-y-auto">
                <EventTimeline />
              </div>

            </div>

          </div>

        </div>

      </main>
    </>
  );
}