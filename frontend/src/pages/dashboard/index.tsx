/**
 * Berenice AI Dashboard - Monitor conversations in real-time
 */
import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import {
  dashboardWs,
  Message,
  Conversation,
  Stats,
  getConversations,
  getStats,
} from '../../services/api';

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: ${({ theme }) => theme.background};
  color: ${({ theme }) => theme.text};
`;

const Header = styled.div`
  padding: 20px;
  background: ${({ theme }) => theme.header};
  border-bottom: 1px solid ${({ theme }) => theme.border};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Title = styled.h1`
  font-size: 24px;
  margin: 0;
`;

const ConnectionStatus = styled.div<{ connected: boolean }>`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;

  &::before {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: ${({ connected }) => (connected ? '#4caf50' : '#f44336')};
  }
`;

const StatsBar = styled.div`
  padding: 15px 20px;
  background: ${({ theme }) => theme.statsBar};
  border-bottom: 1px solid ${({ theme }) => theme.border};
  display: flex;
  gap: 30px;
`;

const StatItem = styled.div`
  display: flex;
  flex-direction: column;

  span:first-child {
    font-size: 12px;
    opacity: 0.7;
    margin-bottom: 4px;
  }

  span:last-child {
    font-size: 20px;
    font-weight: bold;
  }
`;

const Content = styled.div`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

const ConversationList = styled.div`
  width: 300px;
  border-right: 1px solid ${({ theme }) => theme.border};
  overflow-y: auto;
  background: ${({ theme }) => theme.sidebar};
`;

const ConversationItem = styled.div<{ active: boolean }>`
  padding: 15px;
  border-bottom: 1px solid ${({ theme }) => theme.border};
  cursor: pointer;
  background: ${({ active, theme }) => (active ? theme.active : 'transparent')};

  &:hover {
    background: ${({ theme }) => theme.hover};
  }
`;

const MessagesArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const MessageBubble = styled.div<{ direction: 'input' | 'output' }>`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
  align-self: ${({ direction }) =>
    direction === 'output' ? 'flex-end' : 'flex-start'};
  background: ${({ direction, theme }) =>
    direction === 'output' ? theme.outgoing : theme.incoming};
  color: ${({ direction, theme }) =>
    direction === 'output' ? theme.outgoingText : theme.incomingText};
  position: relative;
  word-wrap: break-word;

  .timestamp {
    font-size: 10px;
    opacity: 0.7;
    margin-top: 5px;
  }

  .label {
    font-size: 11px;
    font-weight: bold;
    opacity: 0.8;
    margin-bottom: 4px;
  }
`;

const AgentStatus = styled.div<{ status: string }>`
  padding: 8px 16px;
  background: ${({ status }) =>
    status === 'processing' ? '#ff9800' : '#4caf50'};
  color: white;
  border-radius: 20px;
  font-size: 12px;
  align-self: center;
  margin: 10px 0;
`;

export const Dashboard: React.FC = () => {
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedPhone, setSelectedPhone] = useState<string | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    // Connect to WebSocket
    dashboardWs.connect();

    dashboardWs.onConnection((isConnected) => {
      setConnected(isConnected);
    });

    dashboardWs.onMessage((message) => {
      console.log('Received message:', message);

      // Add message to list
      setMessages((prev) => [...prev, message]);

      // Update conversations list
      if (message.type === 'incoming_message' || message.type === 'outgoing_message') {
        loadConversations();
      }
    });

    dashboardWs.onStats((newStats) => {
      setStats(newStats);
    });

    // Load initial data
    loadConversations();
    loadStats();

    // Refresh stats every 10 seconds
    const statsInterval = setInterval(loadStats, 10000);

    return () => {
      clearInterval(statsInterval);
      dashboardWs.disconnect();
    };
  }, []);

  const loadConversations = async () => {
    try {
      const data = await getConversations();
      setConversations(data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const loadStats = async () => {
    try {
      const data = await getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const filteredMessages = selectedPhone
    ? messages.filter(
        (msg) =>
          msg.phone === selectedPhone ||
          (msg.type === 'agent_status' && msg.phone === selectedPhone)
      )
    : [];

  return (
    <DashboardContainer>
      <Header>
        <Title>🦷 Berenice AI Dashboard</Title>
        <ConnectionStatus connected={connected}>
          {connected ? 'Conectado' : 'Desconectado'}
        </ConnectionStatus>
      </Header>

      <StatsBar>
        <StatItem>
          <span>Conversas Ativas</span>
          <span>{stats?.active_conversations || 0}</span>
        </StatItem>
        <StatItem>
          <span>Total de Mensagens</span>
          <span>{stats?.total_messages || 0}</span>
        </StatItem>
        <StatItem>
          <span>Dashboards Conectados</span>
          <span>{stats?.dashboard_connections || 0}</span>
        </StatItem>
        <StatItem>
          <span>Graphiti</span>
          <span style={{ fontSize: '14px' }}>{stats?.graphiti_status || 'N/A'}</span>
        </StatItem>
      </StatsBar>

      <Content>
        <ConversationList>
          <div style={{ padding: '15px', fontWeight: 'bold', borderBottom: '1px solid #ddd' }}>
            Conversas ({conversations.length})
          </div>
          {conversations.map((conv) => (
            <ConversationItem
              key={conv.phone}
              active={selectedPhone === conv.phone}
              onClick={() => setSelectedPhone(conv.phone)}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                {conv.patient_name}
              </div>
              <div style={{ fontSize: '12px', opacity: 0.7 }}>{conv.phone}</div>
              <div style={{ fontSize: '11px', opacity: 0.6, marginTop: '5px' }}>
                {conv.messages_count} mensagens
              </div>
            </ConversationItem>
          ))}
        </ConversationList>

        <MessagesArea>
          {selectedPhone ? (
            <>
              <div
                style={{
                  padding: '15px 20px',
                  borderBottom: '1px solid #ddd',
                  fontWeight: 'bold',
                }}
              >
                {conversations.find((c) => c.phone === selectedPhone)?.patient_name ||
                  selectedPhone}
              </div>

              <MessagesContainer>
                {filteredMessages.length === 0 && (
                  <div style={{ textAlign: 'center', opacity: 0.5, marginTop: '50px' }}>
                    Aguardando mensagens...
                  </div>
                )}

                {filteredMessages.map((msg, index) => {
                  if (msg.type === 'agent_status') {
                    return (
                      <AgentStatus key={index} status={msg.status || 'idle'}>
                        {msg.status === 'processing'
                          ? '🤖 Berenice está pensando...'
                          : '✅ Mensagem processada'}
                      </AgentStatus>
                    );
                  }

                  return (
                    <MessageBubble key={index} direction={msg.direction || 'input'}>
                      <div className="label">
                        {msg.direction === 'output'
                          ? '🤖 Berenice AI'
                          : `👤 ${msg.sender_name || 'Paciente'}`}
                      </div>
                      <div>{msg.message}</div>
                      <div className="timestamp">
                        {new Date(msg.timestamp).toLocaleTimeString('pt-BR')}
                      </div>
                    </MessageBubble>
                  );
                })}
              </MessagesContainer>
            </>
          ) : (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                opacity: 0.5,
              }}
            >
              Selecione uma conversa para visualizar
            </div>
          )}
        </MessagesArea>
      </Content>
    </DashboardContainer>
  );
};
