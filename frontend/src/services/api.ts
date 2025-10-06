/**
 * API service for connecting to Berenice AI backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

export interface Message {
  type: 'incoming_message' | 'outgoing_message' | 'agent_status';
  direction?: 'input' | 'output';
  phone: string;
  sender_name?: string;
  patient_name?: string;
  message?: string;
  message_id?: string;
  timestamp: string;
  status?: string;
}

export interface Conversation {
  phone: string;
  patient_name: string;
  started_at: string | null;
  messages_count: number;
  last_activity: string | null;
}

export interface Stats {
  active_conversations: number;
  total_messages: number;
  dashboard_connections: number;
  graphiti_status: string;
  timestamp: string;
}

/**
 * Fetch all active conversations
 */
export async function getConversations(): Promise<Conversation[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/conversations`);
    const data = await response.json();

    if (data.success) {
      return data.conversations;
    }

    throw new Error('Failed to fetch conversations');
  } catch (error) {
    console.error('Error fetching conversations:', error);
    throw error;
  }
}

/**
 * Fetch conversation history for a specific patient
 */
export async function getConversationHistory(phone: string, limit = 50) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/dashboard/conversation/${phone}?limit=${limit}`
    );
    const data = await response.json();

    if (data.success) {
      return data.messages;
    }

    throw new Error('Failed to fetch conversation history');
  } catch (error) {
    console.error('Error fetching conversation history:', error);
    throw error;
  }
}

/**
 * Fetch system statistics
 */
export async function getStats(): Promise<Stats> {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
    const data = await response.json();

    if (data.success) {
      return data.stats;
    }

    throw new Error('Failed to fetch stats');
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
}

/**
 * Send manual message to patient (human intervention)
 */
export async function sendManualMessage(phone: string, message: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/send-message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone, message }),
    });

    const data = await response.json();

    if (data.success) {
      return data;
    }

    throw new Error('Failed to send message');
  } catch (error) {
    console.error('Error sending manual message:', error);
    throw error;
  }
}

/**
 * Clear a conversation
 */
export async function clearConversation(phone: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/conversation/${phone}`, {
      method: 'DELETE',
    });

    const data = await response.json();

    if (data.success) {
      return data;
    }

    throw new Error('Failed to clear conversation');
  } catch (error) {
    console.error('Error clearing conversation:', error);
    throw error;
  }
}

/**
 * WebSocket connection for real-time updates
 */
export class DashboardWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 3000;
  private onMessageCallback: ((message: Message) => void) | null = null;
  private onStatsCallback: ((stats: Stats) => void) | null = null;
  private onConnectionCallback: ((connected: boolean) => void) | null = null;

  /**
   * Connect to WebSocket server
   */
  connect() {
    try {
      this.ws = new WebSocket(`${WS_URL}/dashboard/ws`);

      this.ws.onopen = () => {
        console.log('✅ Connected to Berenice AI Dashboard');
        this.reconnectAttempts = 0;

        if (this.onConnectionCallback) {
          this.onConnectionCallback(true);
        }

        // Send ping every 30 seconds to keep connection alive
        setInterval(() => {
          if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send('ping');
          }
        }, 30000);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          // Handle different message types
          if (data.type === 'stats' && this.onStatsCallback) {
            this.onStatsCallback(data.data);
          } else if (this.onMessageCallback) {
            this.onMessageCallback(data);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('❌ Disconnected from Berenice AI Dashboard');

        if (this.onConnectionCallback) {
          this.onConnectionCallback(false);
        }

        // Attempt reconnection
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(
            `Reconnecting in ${this.reconnectDelay / 1000}s (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})...`
          );

          setTimeout(() => this.connect(), this.reconnectDelay);
        }
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Set callback for incoming messages
   */
  onMessage(callback: (message: Message) => void) {
    this.onMessageCallback = callback;
  }

  /**
   * Set callback for stats updates
   */
  onStats(callback: (stats: Stats) => void) {
    this.onStatsCallback = callback;
  }

  /**
   * Set callback for connection status changes
   */
  onConnection(callback: (connected: boolean) => void) {
    this.onConnectionCallback = callback;
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Export singleton instance
export const dashboardWs = new DashboardWebSocket();
