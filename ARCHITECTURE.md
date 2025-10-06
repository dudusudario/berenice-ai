# 🏗️ Arquitetura - Berenice AI SDR System

Arquitetura completa do sistema de SDR com Dashboard em tempo real.

---

## 📊 Visão Geral da Arquitetura

```
┌──────────────────────────────────────────────────────────────────┐
│                     CAMADA DE COMUNICAÇÃO                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐          ┌──────────────────┐                  │
│  │  WhatsApp   │  ◄────►  │     Z-API        │                  │
│  │  (Paciente) │          │   (Gateway)      │                  │
│  └─────────────┘          └────────┬─────────┘                  │
│                                     │                             │
│                            HTTPS POST (Webhook)                   │
│                                     │                             │
└─────────────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                     CAMADA DE APLICAÇÃO                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              FastAPI Server (main.py)                      │ │
│  │                                                             │ │
│  │  ┌──────────────────┐         ┌──────────────────┐        │ │
│  │  │  Webhooks API    │         │  Dashboard API   │        │ │
│  │  │  (webhook/msg)   │         │  (/dashboard/*)  │        │ │
│  │  └────────┬─────────┘         └────────┬─────────┘        │ │
│  │           │                             │                   │ │
│  │           │      ┌──────────────────────┘                  │ │
│  │           │      │                                          │ │
│  │           ▼      ▼                                          │ │
│  │  ┌────────────────────────────────┐                        │ │
│  │  │   WebSocket Manager            │                        │ │
│  │  │   (Real-time Broadcasting)     │                        │ │
│  │  └───────────┬────────────────────┘                        │ │
│  │              │                                               │ │
│  │              │ Broadcast to Dashboard                       │ │
│  │              │                                               │ │
│  └──────────────┼───────────────────────────────────────────── ┘ │
│                 │                                                 │
└─────────────────┼─────────────────────────────────────────────────┘
                  │
                  ▼ (WebSocket)
┌──────────────────────────────────────────────────────────────────┐
│                     CAMADA DE INTERFACE                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         React Dashboard (frontend/)                        │ │
│  │                                                             │ │
│  │  • Visualização de conversas em tempo real                 │ │
│  │  • Input/Output de mensagens                               │ │
│  │  • Status do agente (processando/idle)                     │ │
│  │  • Estatísticas do sistema                                 │ │
│  │  • Tema claro/escuro                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                  ▲
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                     CAMADA DE INTELIGÊNCIA                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          PydanticAI Agent (agent/sdr_agent.py)            │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  8 Tools Customizadas:                               │ │ │
│  │  │  • search_patient_history                            │ │ │
│  │  │  • find_treatment_info                               │ │ │
│  │  │  • get_frequently_asked_questions                    │ │ │
│  │  │  • handle_objection                                  │ │ │
│  │  │  • show_payment_options                              │ │ │
│  │  │  • calculate_payment_plan                            │ │ │
│  │  │  • check_insurance_accepted                          │ │ │
│  │  │  • find_available_appointments                       │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                     CAMADA DE DADOS                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────┐           ┌──────────────────────────┐  │
│  │  Graphiti + Neo4j  │           │  Base de Conhecimento    │  │
│  │                    │           │                          │  │
│  │  • Histórico       │           │  • treatments.json       │  │
│  │  • Contexto        │           │  • faqs.json             │  │
│  │  • Memória Temporal│           │  • Prompts               │  │
│  └────────────────────┘           └──────────────────────────┘  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Mensagem Completo

### 1. Paciente Envia Mensagem

```
👤 Paciente WhatsApp
     │
     │ "Olá, quero fazer clareamento"
     │
     ▼
📱 Z-API
     │
     │ POST https://seu-dominio.com/webhook/message
     │ {
     │   "phone": "5511999999999",
     │   "text": {"message": "Olá, quero fazer clareamento"}
     │ }
     │
     ▼
```

### 2. Backend Processa

```
🖥️ FastAPI Backend
     │
     ├─► 📡 Webhook recebe mensagem
     │   └─► Broadcast para Dashboard (WebSocket)
     │       └─► 📊 Dashboard mostra INPUT em tempo real
     │
     ├─► 💾 Armazena no Graphiti (Neo4j)
     │
     ├─► 🤖 Agente PydanticAI processa
     │   ├─► search_patient_history()
     │   ├─► find_treatment_info("clareamento")
     │   ├─► calculate_payment_plan(1200)
     │   └─► Gera resposta
     │
     ├─► 📤 Envia resposta via Z-API
     │   └─► POST https://api.z-api.io/.../send-text
     │
     └─► 📡 Broadcast para Dashboard (WebSocket)
         └─► 📊 Dashboard mostra OUTPUT em tempo real
```

### 3. Dashboard Visualiza

```
📊 React Dashboard
     │
     ├─► Recebe via WebSocket:
     │   ├─► incoming_message (INPUT)
     │   ├─► agent_status (processando...)
     │   └─► outgoing_message (OUTPUT)
     │
     └─► Atualiza UI em tempo real
         ├─► Mensagem do paciente (esquerda)
         ├─► Indicador "Berenice pensando..."
         └─► Resposta do agente (direita)
```

---

## 📂 Estrutura de Pastas Detalhada

```
berenice-ai/
│
├── main.py                          # ⭐ Aplicação FastAPI principal
│
├── api/                             # 📡 Endpoints da API
│   ├── webhooks.py                  # Recebe mensagens Z-API
│   └── dashboard.py                 # API do dashboard (WebSocket + REST)
│
├── agent/                           # 🤖 Agente Inteligente
│   ├── sdr_agent.py                # PydanticAI agent + tools
│   └── tools.py                    # Funções das 8 tools
│
├── services/                        # 🔧 Serviços
│   ├── zapi_service.py             # Cliente Z-API (enviar msg)
│   ├── graphiti_service.py         # Cliente Graphiti (memória)
│   └── websocket_service.py        # Manager WebSocket (broadcast)
│
├── models/                          # 📋 Modelos Pydantic
│   └── message.py                  # Modelos de mensagens
│
├── config/                          # ⚙️ Configurações
│   ├── settings.py                 # Variáveis de ambiente
│   └── prompts.py                  # System prompts
│
├── knowledge/                       # 📚 Base de Conhecimento
│   ├── treatments.json             # 9 tratamentos
│   └── faqs.json                   # 20 FAQs + objeções
│
├── frontend/                        # 🎨 Dashboard React
│   ├── public/                     # Assets
│   ├── src/
│   │   ├── services/
│   │   │   └── api.ts              # Cliente API + WebSocket
│   │   ├── pages/
│   │   │   └── dashboard/          # Página principal ⭐
│   │   │       └── index.tsx
│   │   ├── common/
│   │   │   ├── theme/              # Temas
│   │   │   └── components/         # Componentes
│   │   └── routes/                 # Rotas
│   │       └── index.tsx
│   ├── .env.example
│   └── package.json
│
├── requirements.txt                 # Dependências Python
├── .env.example                    # Config backend
└── docs/
    ├── README_SDR.md               # Doc técnica
    ├── QUICKSTART.md               # Início rápido
    ├── DEPLOY.md                   # Deploy
    └── ARCHITECTURE.md             # Este arquivo
```

---

## 🔌 Endpoints da API

### Webhooks (Z-API → Backend)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/webhook/message` | Recebe mensagens do WhatsApp |
| POST | `/webhook/status` | Recebe status de mensagens |
| GET | `/webhook/health` | Health check |

### Dashboard API (Backend → Frontend)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| WS | `/dashboard/ws` | WebSocket real-time |
| GET | `/dashboard/conversations` | Lista conversas ativas |
| GET | `/dashboard/conversation/:phone` | Histórico de conversa |
| GET | `/dashboard/stats` | Estatísticas do sistema |
| POST | `/dashboard/send-message` | Enviar mensagem manual |
| DELETE | `/dashboard/conversation/:phone` | Limpar conversa |

### Z-API (Backend → WhatsApp)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `https://api.z-api.io/instances/{id}/token/{token}/send-text` | Enviar texto |
| POST | `.../send-image` | Enviar imagem |
| POST | `.../send-document` | Enviar documento |
| POST | `.../send-presence` | Indicador digitando |
| POST | `.../read-message` | Marcar como lido |

---

## 📨 Formato de Mensagens WebSocket

### Input (Paciente → Sistema)

```json
{
  "type": "incoming_message",
  "direction": "input",
  "phone": "5511999999999",
  "sender_name": "João Silva",
  "message": "Olá, quero fazer clareamento",
  "message_id": "msg_123abc",
  "timestamp": "2025-10-06T14:30:00.000Z"
}
```

### Output (Sistema → Paciente)

```json
{
  "type": "outgoing_message",
  "direction": "output",
  "phone": "5511999999999",
  "patient_name": "João Silva",
  "message": "Ótimo! Temos 2 opções de clareamento...",
  "message_id": null,
  "timestamp": "2025-10-06T14:30:05.000Z"
}
```

### Agent Status

```json
{
  "type": "agent_status",
  "phone": "5511999999999",
  "status": "processing",  // ou "idle"
  "timestamp": "2025-10-06T14:30:02.000Z"
}
```

### Stats Update

```json
{
  "type": "stats",
  "data": {
    "active_conversations": 5,
    "total_messages": 42,
    "dashboard_connections": 2,
    "graphiti_status": "connected",
    "timestamp": "2025-10-06T14:30:00.000Z"
  }
}
```

---

## 🔐 Segurança

### CORS

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://seu-dashboard.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### WebSocket Authentication (Futuro)

```python
# Adicionar token de autenticação
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    if not verify_token(token):
        await websocket.close(code=1008)
        return
    # ...
```

---

## 🚀 Deploy

### Backend (FastAPI)

```bash
# Railway, Render, ou VPS
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**URL gerada**: `https://berenice-ai-production.up.railway.app`

### Frontend (React)

**Opção 1: Vercel** (Recomendado para React)

```bash
cd frontend
npm install -g vercel
vercel
```

**URL gerada**: `https://berenice-ai-dashboard.vercel.app`

**Opção 2: Netlify**

```bash
cd frontend
npm run build
# Upload da pasta build/ no Netlify
```

**Opção 3: Servir do Backend** (Simples)

```bash
# Build do frontend
cd frontend
npm run build

# Configurar FastAPI para servir
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend/build", html=True))
```

---

## 🔄 Fluxo de Dados Completo

### Mensagem Recebida (Input)

1. **WhatsApp** → paciente envia mensagem
2. **Z-API** → recebe e faz POST para `/webhook/message`
3. **Backend** → webhook processa e:
   - ✅ Broadcast `incoming_message` via WebSocket
   - ✅ Armazena no Graphiti
   - ✅ Envia para agente processar
4. **Dashboard** → mostra mensagem em tempo real (esquerda)

### Agente Processando

5. **Agente PydanticAI** → processa mensagem
   - ✅ Broadcast `agent_status: processing`
   - ✅ Usa tools para buscar informações
   - ✅ Gera resposta inteligente
6. **Dashboard** → mostra indicador "🤖 Berenice pensando..."

### Mensagem Enviada (Output)

7. **Backend** → envia resposta:
   - ✅ POST para Z-API `/send-text`
   - ✅ Broadcast `outgoing_message` via WebSocket
   - ✅ Armazena no Graphiti
8. **Z-API** → entrega mensagem no WhatsApp
9. **Dashboard** → mostra resposta em tempo real (direita)

### Atualização de Stats

10. **Backend** → atualiza estatísticas
11. **Dashboard** → atualiza contadores em tempo real

---

## 🧪 Como Testar

### 1. Iniciar Backend

```bash
cd /Users/edu/Desktop/PROJETOS/berenice-ai/graphiti-agent
python main.py
```

**Console mostra:**
```
🚀 Application ready on http://0.0.0.0:8000
📊 Dashboard URL: http://0.0.0.0:8000/dashboard/ws
🌐 Frontend: Open frontend/index.html or run npm start in frontend/
```

### 2. Iniciar Frontend

```bash
cd frontend
npm install
npm start
```

**Browser abre:** `http://localhost:3000`

### 3. Enviar Mensagem de Teste

```bash
# Via Z-API (WhatsApp real)
# Ou teste manual:
curl -X POST http://localhost:8000/webhook/message \
  -H "Content-Type: application/json" \
  -d '{
    "messageId": "test_123",
    "phone": "5511999999999",
    "fromMe": false,
    "text": {"message": "Olá, quero agendar"},
    "senderName": "Teste",
    "momment": 1696598400000
  }'
```

### 4. Ver no Dashboard

✅ Mensagem aparece instantaneamente
✅ Indicador "Berenice pensando..."
✅ Resposta do agente aparece
✅ Contadores atualizados

---

## 📊 Monitoramento

### Logs Backend

```bash
# Tempo real
tail -f logs/berenice-ai.log

# Filtrar por tipo
grep "incoming_message" logs/berenice-ai.log
grep "outgoing_message" logs/berenice-ai.log
```

### Logs Frontend

- Chrome DevTools → Console
- Network tab → WS (ver mensagens WebSocket)

### Neo4j

```cypher
// Ver todas conversas
MATCH (n) RETURN n LIMIT 25

// Buscar paciente específico
MATCH (n)
WHERE n.phone = '5511999999999'
RETURN n
```

---

## 🎯 Próximas Melhorias

### Backend
- [ ] Autenticação JWT para dashboard
- [ ] Rate limiting
- [ ] Redis para conversation_states
- [ ] Logs estruturados (JSON)
- [ ] Métricas Prometheus

### Frontend
- [ ] Login/autenticação
- [ ] Intervenção manual
- [ ] Busca/filtros avançados
- [ ] Exportar conversas (PDF/CSV)
- [ ] Notificações push
- [ ] Modo escuro persistente
- [ ] Gráficos de métricas

### Integração
- [ ] Google Calendar (agenda real)
- [ ] CRM (HubSpot, Pipedrive)
- [ ] Pagamento online
- [ ] Notificações SMS/Email

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web assíncrono
- **WebSocket**: Comunicação real-time
- **PydanticAI**: Framework de agentes IA
- **Graphiti**: Grafo de conhecimento temporal
- **Neo4j**: Banco de dados de grafo

### Frontend
- **React**: Biblioteca UI
- **TypeScript**: Type safety
- **Styled-Components**: CSS-in-JS
- **React Router**: Roteamento
- **WebSocket API**: Real-time

---

**Arquitetura desenhada para escalabilidade, manutenibilidade e performance! 🚀**
