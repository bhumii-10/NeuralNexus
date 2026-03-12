import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/* =========================
   TYPES
========================= */

export interface QueryRequest {
  query: string;
  context?: string;   // NEW: conversation context
}

export interface QueryResponse {
  agent: string;
  planning_used: boolean;
  routing_reason?: string;
  response?: string;
  tasks?: Array<{
    task: string;
    agent: string;
  }>;
  results?: Array<{
    task: string;
    agent: string;
    response: string;
  }>;
}

export interface Event {
  timestamp: string;
  event_type: string;
  data: any;
}

export interface EventsResponse {
  total: number;
  events: Event[];
}

export interface QueryHistory {
  id: number;
  query_text: string;
  timestamp: string;
  tasks: Array<{
    id: number;
    description: string;
    agent: string;
    result?: {
      response: string;
      timestamp: string;
    };
  }>;
}

export interface HistoryResponse {
  total: number;
  history: QueryHistory[];
}

/* =========================
   API CALLS
========================= */

export const sendQuery = async (
  query: string,
  context?: string
): Promise<QueryResponse> => {

  const payload: QueryRequest = {
    query,
    context
  };

  const response = await api.post<QueryResponse>('/query', payload);

  return response.data;
};

export const getEvents = async (limit: number = 50): Promise<EventsResponse> => {
  const response = await api.get<EventsResponse>(`/events?limit=${limit}`);
  return response.data;
};

export const getHistory = async (limit: number = 10): Promise<HistoryResponse> => {
  const response = await api.get<HistoryResponse>(`/history?limit=${limit}`);
  return response.data;
};

export const checkHealth = async (): Promise<{ status: string }> => {
  const response = await api.get('/health');
  return response.data;
};

export const deleteHistory = async (
  queryId: number
): Promise<{ success: boolean; message: string }> => {
  const response = await api.delete(`/history/${queryId}`);
  return response.data;
};