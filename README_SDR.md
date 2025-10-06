# Berenice AI - Agente SDR para Clínica Odontológica 🦷🤖

Sistema de SDR (Sales Development Representative) inteligente para clínicas odontológicas, usando WhatsApp como canal de comunicação principal.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Reference](#api-reference)
- [Manutenção](#manutenção)

---

## 🎯 Visão Geral

O Berenice AI é um agente SDR automatizado que:

- **Recebe mensagens** via WhatsApp através da API Z-API
- **Qualifica leads** automaticamente com base nas conversas
- **Mantém contexto** temporal usando Graphiti + Neo4j
- **Responde perguntas** sobre tratamentos, preços e horários
- **Agenda consultas** diretamente pelo WhatsApp
- **Trata objeções** com respostas empáticas e informativas
- **Faz follow-up** proativo com leads que não converteram

### Tecnologias Utilizadas

- **PydanticAI**: Framework para agentes de IA com validação de tipos
- **Graphiti + Neo4j**: Grafo de conhecimento temporal
- **FastAPI**: API REST para receber webhooks
- **Z-API**: Integração com WhatsApp
- **OpenAI GPT-4o-mini**: Modelo de linguagem

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    WhatsApp (Paciente)                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Z-API (Webhook HTTP POST)                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Server (main.py)                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Webhook Receiver (api/webhooks.py)             │   │
│  │  - Recebe mensagens                             │   │
│  │  - Processa em background                       │   │
│  │  - Envia para agente                            │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│           Agente SDR (agent/sdr_agent.py)               │
│  ┌─────────────────────────────────────────────────┐   │
│  │  PydanticAI Agent com Tools:                    │   │
│  │  - search_patient_history                       │   │
│  │  - find_treatment_info                          │   │
│  │  - handle_objection                             │   │
│  │  - check_availability                           │   │
│  │  - calculate_payment_plan                       │   │
│  └─────────────────────────────────────────────────┘   │
└───────────┬─────────────────┬───────────────────────────┘
            │                 │
            ▼                 ▼
┌─────────────────┐   ┌─────────────────────────────────┐
│  Graphiti/Neo4j │   │  Base de Conhecimento          │
│  - Histórico    │   │  - Tratamentos (JSON)           │
│  - Contexto     │   │  - FAQs (JSON)                  │
│  - Memória      │   │  - Objeções (JSON)              │
└─────────────────┘   └─────────────────────────────────┘
```

---

## ✨ Funcionalidades

### 1. Recepção e Qualificação de Leads

- ✅ Saudação personalizada por horário
- ✅ Identificação de leads novos vs. recorrentes
- ✅ Qualificação automática (BANT: Budget, Authority, Need, Timeline)
- ✅ Score de qualificação (0-100)

### 2. Informações sobre Tratamentos

- ✅ Busca inteligente por sintomas ou necessidades
- ✅ Detalhes de preços e durações
- ✅ Benefícios de cada tratamento
- ✅ Opções de pagamento e parcelamento

### 3. Agendamento

- ✅ Verificação de disponibilidade
- ✅ Proposta de horários flexíveis
- ✅ Confirmação automática
- ✅ Lembretes 24h antes (futuro)

### 4. Tratamento de Objeções

- ✅ Preço ("muito caro")
- ✅ Tempo ("não tenho tempo")
- ✅ Medo ("tenho medo de dentista")
- ✅ Indecisão ("vou pensar")

### 5. Memória e Contexto

- ✅ Histórico completo de conversas
- ✅ Preferências do paciente
- ✅ Tratamentos de interesse
- ✅ Objeções anteriores
- ✅ Tentativas de agendamento

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Neo4j 5.26+ (local ou cloud)
- Conta Z-API ativa
- Chave OpenAI API

### Passo 1: Clone e Configure Ambiente

```bash
cd /Users/edu/Desktop/PROJETOS/berenice-ai/graphiti-agent

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Configure Neo4j

**Opção A: Neo4j Desktop**
1. Baixe [Neo4j Desktop](https://neo4j.com/download/)
2. Crie um novo projeto e DBMS
3. Inicie o DBMS
4. Anote URI, usuário e senha

**Opção B: Neo4j Aura (Cloud)**
1. Crie conta em [Neo4j Aura](https://neo4j.com/cloud/aura/)
2. Crie um banco gratuito
3. Anote as credenciais

### Passo 3: Configure Z-API

1. Acesse [Z-API](https://www.z-api.io/)
2. Crie uma conta e instância
3. Conecte seu WhatsApp (QR Code)
4. Anote: `instance_id`, `token`, `client_token`

### Passo 4: Configure Variáveis de Ambiente

```bash
cp .env.example .env
nano .env  # ou use seu editor preferido
```

Edite o arquivo `.env`:

```env
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sua_senha

# OpenAI
OPENAI_API_KEY=sk-...
MODEL_CHOICE=gpt-4o-mini

# Z-API
ZAPI_INSTANCE_ID=sua_instancia
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token
ZAPI_BASE_URL=https://api.z-api.io

# Clínica
CLINIC_NAME=Instituto Dental Life
CLINIC_PHONE=551141183589
CLINIC_ADDRESS=Rua Groenlandia 848, Jardim America - Sao Paulo - SP

# App
DEBUG=True
PORT=8000
HOST=0.0.0.0
```

---

## ⚙️ Configuração

### 1. Personalize os Tratamentos

Edite `knowledge/treatments.json`:

```json
{
  "id": "novo_tratamento",
  "name": "Nome do Tratamento",
  "description": "Descrição completa",
  "price_range": "R$ 500 - R$ 1.000",
  "keywords": ["palavra1", "palavra2"]
}
```

### 2. Adicione FAQs

Edite `knowledge/faqs.json`:

```json
{
  "question": "Pergunta frequente?",
  "answer": "Resposta detalhada..."
}
```

### 3. Customize o Prompt do Agente

Edite `config/prompts.py` → `SDR_SYSTEM_PROMPT`

### 4. Configure Webhooks no Z-API

1. Acesse o painel Z-API
2. Vá em **Webhooks**
3. Configure:
   - **Webhook de Mensagens**: `https://seu-dominio.com/webhook/message`
   - **Webhook de Status**: `https://seu-dominio.com/webhook/status`

---

## 🎮 Uso

### Iniciar o Servidor

```bash
# Desenvolvimento
python main.py

# Produção
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testar Localmente com ngrok

```bash
# Em outro terminal
ngrok http 8000

# Use o URL do ngrok para configurar o webhook no Z-API
# Exemplo: https://abc123.ngrok.io/webhook/message
```

### Endpoints Disponíveis

- `GET /` - Informações da API
- `GET /health` - Health check
- `POST /webhook/message` - Recebe mensagens do WhatsApp
- `POST /webhook/status` - Recebe status de mensagens
- `GET /docs` - Documentação Swagger automática

### Testar o Agente

1. Envie mensagem WhatsApp para o número conectado ao Z-API
2. Aguarde resposta do agente
3. Verifique logs no terminal

### Logs

```bash
# Ver logs em tempo real
tail -f logs/app.log  # Se configurado

# Ou veja no terminal
python main.py
```

---

## 📁 Estrutura do Projeto

```
graphiti-agent/
├── main.py                    # FastAPI app principal
├── requirements.txt           # Dependências Python
├── .env.example              # Exemplo de configuração
├── .env                      # Configuração (NÃO COMMITAR!)
│
├── config/
│   ├── settings.py           # Configurações carregadas do .env
│   └── prompts.py            # System prompts e templates
│
├── api/
│   └── webhooks.py           # Endpoints de webhook
│
├── agent/
│   ├── sdr_agent.py          # Agente PydanticAI principal
│   └── tools.py              # Tools customizadas do agente
│
├── services/
│   ├── zapi_service.py       # Cliente Z-API (enviar mensagens)
│   └── graphiti_service.py   # Cliente Graphiti (memória)
│
├── models/
│   └── message.py            # Modelos Pydantic para mensagens
│
├── knowledge/
│   ├── treatments.json       # Base de tratamentos
│   └── faqs.json             # Perguntas frequentes
│
└── utils/                    # Utilitários (futuro)
```

---

## 🔧 API Reference

### Webhook: Receber Mensagem

**POST** `/webhook/message`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "messageId": "msg_123",
  "phone": "5511999999999",
  "fromMe": false,
  "text": {
    "message": "Olá, quero saber sobre clareamento"
  },
  "senderName": "João Silva",
  "momment": 1696598400000
}
```

**Response:**
```json
{
  "status": "received",
  "messageId": "msg_123"
}
```

---

## 📊 Fluxo de Conversação

### Exemplo 1: Novo Lead

```
Paciente: Olá
Berenice: Bom dia! 🌅 Sou a Berenice, do Instituto Dental Life. Como posso ajudar você hoje?

Paciente: Queria saber sobre clareamento
Berenice: Ótimo! O clareamento dental é um dos nossos procedimentos mais procurados!

          Temos duas opções:
          ✨ Clareamento a laser (3-4 sessões) - R$ 800 a R$ 1.500
          ✨ Clareamento caseiro (moldeira) - R$ 500 a R$ 800

          Ambos são seguros e trazem resultados excelentes! Qual te interessa mais?

Paciente: O a laser. Mas tá caro né?
Berenice: Entendo sua preocupação com o investimento! 💰

          Aqui no Instituto Dental Life:
          ✅ Parcelamos em até 12x sem juros
          ✅ Aceitamos diversos cartões
          ✅ Fazemos orçamento sem compromisso

          Se pagar à vista no PIX, tem 5% de desconto!
          Que tal agendar uma avaliação gratuita para conversarmos melhor?

Paciente: Pode ser! Quando tem vaga?
Berenice: Excelente! 📅 Tenho as seguintes opções disponíveis:

          - Amanhã (08/10) às 09:00
          - Amanhã (08/10) às 14:00
          - Quarta (09/10) às 10:30

          Qual funciona melhor para você?
```

---

## 🛠️ Manutenção

### Adicionar Novo Tratamento

1. Edite `knowledge/treatments.json`
2. Adicione o objeto do tratamento
3. Reinicie o servidor

### Atualizar Preços

Edite os campos `price_range` em `knowledge/treatments.json`

### Monitorar Conversões

```python
# Ver conversas ativas
curl http://localhost:8000/webhook/health

# Ver histórico no Neo4j
# Acesse Neo4j Browser e execute:
MATCH (n) RETURN n LIMIT 25
```

### Backup do Graphiti

```bash
# Backup do Neo4j
neo4j-admin dump --database=neo4j --to=/backup/berenice-$(date +%Y%m%d).dump
```

---

## 🚀 Deploy em Produção

### Opção 1: VPS (Digital Ocean, Linode, etc.)

```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install python3.10 python3-pip

# Clonar repositório
git clone [seu-repo]
cd graphiti-agent

# Configurar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Criar serviço systemd
sudo nano /etc/systemd/system/berenice-ai.service
```

**berenice-ai.service:**
```ini
[Unit]
Description=Berenice AI SDR Agent
After=network.target

[Service]
Type=simple
User=seu-usuario
WorkingDirectory=/caminho/para/graphiti-agent
Environment="PATH=/caminho/para/venv/bin"
ExecStart=/caminho/para/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar serviço
sudo systemctl daemon-reload
sudo systemctl start berenice-ai
sudo systemctl enable berenice-ai
```

### Opção 2: Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t berenice-ai .
docker run -d -p 8000:8000 --env-file .env berenice-ai
```

### Opção 3: Railway / Render

1. Conecte seu repositório GitHub
2. Configure variáveis de ambiente
3. Deploy automático a cada push

---

## 📈 Próximos Passos

### Features Planejadas

- [ ] Dashboard administrativo
- [ ] Relatórios de conversão
- [ ] Integração com Google Calendar
- [ ] Sistema de filas para alta demanda
- [ ] Análise de sentimento
- [ ] Follow-up automático agendado
- [ ] Envio de fotos de tratamentos
- [ ] Integração com CRM
- [ ] Múltiplos atendentes humanos
- [ ] Transferência para atendimento humano

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é proprietário do Instituto Dental Life.

---

## 🆘 Suporte

- **Email**: suporte@institutodental.life
- **WhatsApp**: (11) 4118-3589
- **Issues**: [GitHub Issues](seu-repo/issues)

---

## 🙏 Agradecimentos

- [PydanticAI](https://ai.pydantic.dev/) - Framework de agentes
- [Graphiti](https://github.com/getzep/graphiti) - Grafo de conhecimento
- [Z-API](https://www.z-api.io/) - Integração WhatsApp
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web

---

**Desenvolvido com ❤️ para o Instituto Dental Life**
