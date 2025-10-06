# 📊 Berenice AI Dashboard

Dashboard em tempo real para monitorar conversas do Agente SDR da clínica odontológica.

## 🎯 Funcionalidades

- ✅ **Monitoramento em tempo real** via WebSocket
- ✅ **Visualização de conversas** ativas
- ✅ **Histórico completo** de mensagens
- ✅ **Input/Output** de todas as mensagens
- ✅ **Status do agente** (pensando/processando)
- ✅ **Estatísticas** do sistema
- ✅ **Tema claro/escuro**

---

## 🚀 Como Usar

### Desenvolvimento

```bash
# Navegar para a pasta frontend
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env

# Iniciar o dashboard
npm start
```

O dashboard abrirá em: **http://localhost:3000**

### Produção

```bash
# Build do frontend
npm run build

# Os arquivos otimizados estarão em: build/
# Sirva com nginx, vercel, netlify, etc.
```

---

## ⚙️ Configuração

### .env

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_CLINIC_NAME=Instituto Dental Life
```

### Para Produção

Atualize as URLs para o seu servidor:

```env
REACT_APP_API_URL=https://berenice-ai-production.up.railway.app
REACT_APP_WS_URL=wss://berenice-ai-production.up.railway.app
```

---

## 📡 Conexão com Backend

O dashboard se conecta ao backend FastAPI via:

### WebSocket (Real-time)
```
ws://localhost:8000/dashboard/ws
```

Recebe:
- 📥 Mensagens recebidas (input)
- 📤 Mensagens enviadas (output)
- 🤖 Status do agente (processando/idle)
- 📊 Estatísticas do sistema

### REST API

```
GET  /dashboard/conversations          # Lista conversas ativas
GET  /dashboard/conversation/:phone    # Histórico de conversa
GET  /dashboard/stats                  # Estatísticas
POST /dashboard/send-message           # Enviar mensagem manual
DELETE /dashboard/conversation/:phone  # Limpar conversa
```

---

## 🎨 Interface

### Tela Principal

```
┌─────────────────────────────────────────────────────────────┐
│  🦷 Berenice AI Dashboard          ●  Conectado             │
├─────────────────────────────────────────────────────────────┤
│  Conversas: 5  │  Mensagens: 42  │  Dashboards: 1  │  ...  │
├────────────────┬────────────────────────────────────────────┤
│ Conversas (5)  │                                            │
├────────────────┤         João Silva (5511999999999)         │
│ 👤 João Silva  │                                            │
│ 5511999999999  │  👤 Olá, quero fazer clareamento          │
│ 8 mensagens    │     14:30                                  │
├────────────────┤                                            │
│ 👤 Maria Clara │  🤖 Berenice está pensando...             │
│ 5511888888888  │                                            │
│ 3 mensagens    │  🤖 Ótimo! Temos 2 opções de clareamento  │
├────────────────┤     14:31                                  │
│ ...            │                                            │
└────────────────┴────────────────────────────────────────────┘
```

### Indicadores Visuais

- 🟢 Verde: Conectado ao backend
- 🔴 Vermelho: Desconectado
- 🟠 Laranja: Agente processando
- 👤 Input do paciente (esquerda)
- 🤖 Output do Berenice AI (direita)

---

## 📦 Estrutura

```
frontend/
├── public/              # Assets estáticos
├── src/
│   ├── services/
│   │   └── api.ts       # Cliente API + WebSocket
│   ├── pages/
│   │   ├── dashboard/   # Página do dashboard ⭐
│   │   └── chat/        # Chat UI original
│   ├── common/
│   │   ├── components/  # Componentes reutilizáveis
│   │   ├── theme/       # Temas (claro/escuro)
│   │   └── hooks/       # Custom hooks
│   └── routes/          # Rotas da aplicação
├── .env.example         # Variáveis de ambiente
└── package.json         # Dependências
```

---

## 🧪 Testando

### 1. Inicie o Backend

```bash
cd /Users/edu/Desktop/PROJETOS/berenice-ai/graphiti-agent
python main.py
```

### 2. Inicie o Frontend

```bash
cd frontend
npm start
```

### 3. Envie Mensagem WhatsApp

Envie para o número conectado ao Z-API. Você verá:

1. ✅ Mensagem aparecer em tempo real no dashboard
2. 🤖 Indicador "Berenice está pensando..."
3. ✅ Resposta do agente aparecer

---

## 🎯 Próximas Features

- [ ] Intervenção manual (humano assume conversa)
- [ ] Filtros e busca de conversas
- [ ] Exportar histórico
- [ ] Notificações de novas mensagens
- [ ] Métricas de conversão
- [ ] Análise de sentimento
- [ ] Tags e categorização

---

**Dashboard desenvolvido com ❤️ para Instituto Dental Life**
