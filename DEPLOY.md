# 🚀 Deploy em Produção - Berenice AI

Este guia mostra como fazer deploy do Berenice AI e obter um **webhook URL permanente**.

---

## 📋 Pré-requisitos

- ✅ Código funcionando localmente
- ✅ Conta GitHub (para deploy automático)
- ✅ Credenciais configuradas (.env)

---

## Opção 1: Railway (RECOMENDADO) ⭐

### Vantagens:
- ✅ Deploy em 5 minutos
- ✅ HTTPS automático
- ✅ URL pública permanente
- ✅ $5 grátis/mês
- ✅ Deploy automático via GitHub

### Passo a Passo:

#### 1. Prepare o Repositório

```bash
cd /Users/edu/Desktop/PROJETOS/berenice-ai/graphiti-agent

# Initialize git (se ainda não tiver)
git init
git add .
git commit -m "Initial commit - Berenice AI SDR"

# Crie um repositório no GitHub e conecte
git remote add origin https://github.com/seu-usuario/berenice-ai.git
git branch -M main
git push -u origin main
```

#### 2. Deploy no Railway

1. Acesse: https://railway.app/
2. Clique em **"Start a New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Autorize o Railway a acessar seu GitHub
5. Selecione o repositório **berenice-ai**
6. Railway vai detectar Python e fazer deploy automaticamente

#### 3. Configure Variáveis de Ambiente

No painel do Railway:

1. Clique no seu projeto
2. Vá em **"Variables"**
3. Adicione todas as variáveis do seu `.env`:

```
NEO4J_URI=bolt://147.79.81.91:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=Neo4jVPS2025!
OPENAI_API_KEY=sk-...
MODEL_CHOICE=gpt-4o-mini
ZAPI_INSTANCE_ID=seu_instance_id
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token
ZAPI_BASE_URL=https://api.z-api.io
CLINIC_NAME=Instituto dental life
CLINIC_PHONE=551141183589
CLINIC_ADDRESS=Rua Groenlandia 848, Jardim America - Sao Paulo - SP
DEBUG=False
HOST=0.0.0.0
```

#### 4. Obtenha seu Webhook URL

Após o deploy:

1. Railway vai gerar uma URL pública tipo:
   ```
   https://berenice-ai-production-abc123.up.railway.app
   ```

2. Seu **WEBHOOK URL** será:
   ```
   📥 INPUT: https://berenice-ai-production-abc123.up.railway.app/webhook/message
   📥 STATUS: https://berenice-ai-production-abc123.up.railway.app/webhook/status
   ```

3. **Configure no Z-API**:
   - Vá em: https://www.z-api.io/admin
   - Selecione sua instância
   - Webhooks → Webhook de Mensagens: Cole a URL acima
   - Webhooks → Webhook de Status: Cole a URL de status
   - Salvar

#### 5. Teste

Envie uma mensagem WhatsApp para o número conectado e veja funcionar! 🎉

**Logs:** Acesse os logs em tempo real no painel Railway.

---

## Opção 2: Render ⚡

### Vantagens:
- ✅ Plano gratuito permanente
- ✅ HTTPS automático
- ✅ Deploy via GitHub

### Passo a Passo:

#### 1. Prepare o Repositório (igual Railway acima)

#### 2. Deploy no Render

1. Acesse: https://render.com/
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: berenice-ai
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

#### 3. Configure Variáveis de Ambiente

No painel Render, adicione as mesmas variáveis do Railway.

⚠️ **IMPORTANTE**: No plano gratuito, o serviço "dorme" após 15min de inatividade.
Para manter ativo 24/7, considere o plano pago ($7/mês).

#### 4. Obtenha seu Webhook URL

Render vai gerar:
```
https://berenice-ai.onrender.com
```

Seu webhook será:
```
https://berenice-ai.onrender.com/webhook/message
```

---

## Opção 3: VPS Próprio (Digital Ocean, Linode, etc.) 💻

### Vantagens:
- ✅ Controle total
- ✅ Mais barato em escala
- ✅ Sem limitações

### Custo:
- ~$5-10/mês (VPS básico)

### Passo a Passo:

#### 1. Crie VPS

1. Acesse: https://www.digitalocean.com/
2. Crie um Droplet Ubuntu 22.04
3. Anote o IP público: `123.45.67.89`

#### 2. Configure o Servidor

```bash
# SSH no servidor
ssh root@123.45.67.89

# Instalar dependências
apt update
apt install -y python3.10 python3-pip nginx certbot python3-certbot-nginx

# Clonar repositório
cd /opt
git clone https://github.com/seu-usuario/berenice-ai.git
cd berenice-ai/graphiti-agent

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copiar e configurar .env
cp .env.example .env
nano .env  # Configure suas variáveis
```

#### 3. Configurar Systemd Service

```bash
# Criar serviço
cat > /etc/systemd/system/berenice-ai.service << 'EOF'
[Unit]
Description=Berenice AI SDR Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/berenice-ai/graphiti-agent
Environment="PATH=/opt/berenice-ai/graphiti-agent/venv/bin"
ExecStart=/opt/berenice-ai/graphiti-agent/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Iniciar serviço
systemctl daemon-reload
systemctl start berenice-ai
systemctl enable berenice-ai
```

#### 4. Configurar Nginx + SSL

```bash
# Configurar Nginx
cat > /etc/nginx/sites-available/berenice-ai << 'EOF'
server {
    listen 80;
    server_name seu-dominio.com;  # Substitua pelo seu domínio

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Ativar site
ln -s /etc/nginx/sites-available/berenice-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Configurar SSL (HTTPS)
certbot --nginx -d seu-dominio.com
```

#### 5. Seu Webhook URL

```
https://seu-dominio.com/webhook/message
```

---

## 🎯 Qual Opção Escolher?

| Critério | Railway | Render (Free) | Render (Paid) | VPS |
|----------|---------|---------------|---------------|-----|
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Custo inicial** | $0 | $0 | $7/mês | $5/mês |
| **Uptime 24/7** | ✅ | ❌ (dorme) | ✅ | ✅ |
| **HTTPS auto** | ✅ | ✅ | ✅ | ❌ (config manual) |
| **Escalável** | ✅ | ✅ | ✅ | ⚠️ (manual) |

### **Recomendação:**

- **Iniciando/Testando**: Railway (deploy em 5min)
- **Produção Séria**: Railway ou VPS
- **Budget Zero**: Render Free + Cron job para manter ativo

---

## 🔍 Verificar se está Funcionando

Após deploy, teste:

```bash
# Teste health check
curl https://seu-webhook-url.com/health

# Deve retornar:
{
  "status": "healthy",
  "service": "berenice-ai-sdr",
  "graphiti": "connected"
}
```

---

## 📊 Monitoramento

### Railway
- Logs em tempo real no dashboard
- Métricas de uso
- Alertas automáticos

### Render
- Logs no dashboard
- Métricas básicas

### VPS
```bash
# Ver logs
journalctl -u berenice-ai -f

# Status do serviço
systemctl status berenice-ai
```

---

## 🆘 Troubleshooting

### Webhook não recebe mensagens

1. **Verifique a URL no Z-API**
   - Tem que ser HTTPS em produção
   - Sem barra no final: `/webhook/message` ✅ `/webhook/message/` ❌

2. **Teste manualmente**
   ```bash
   curl -X POST https://seu-webhook.com/webhook/message \
     -H "Content-Type: application/json" \
     -d '{"phone":"5511999999999","text":{"message":"teste"},"messageId":"test","fromMe":false,"momment":1234567890}'
   ```

3. **Verifique logs**
   - Railway: Dashboard → Logs
   - Render: Dashboard → Logs
   - VPS: `journalctl -u berenice-ai -f`

### Erro de conexão Neo4j

- ✅ Verifique se o Neo4j VPS está acessível publicamente
- ✅ Firewall liberado na porta 7687
- ✅ Credenciais corretas no `.env`

### Timeout na OpenAI

- ✅ Chave API válida
- ✅ Créditos disponíveis
- ✅ Rate limit não atingido

---

## 🎉 Deploy Concluído!

Após seguir esses passos, você terá:

✅ Servidor rodando 24/7
✅ Webhook URL permanente: `https://seu-dominio.com/webhook/message`
✅ HTTPS configurado
✅ Logs monitorados
✅ Deploy automático (Railway/Render)

**Próximo passo**: Configure o webhook URL no Z-API e comece a receber mensagens! 🚀
