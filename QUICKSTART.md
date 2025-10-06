# 🚀 Guia de Início Rápido - Berenice AI

## ⏱️ Tempo estimado: 15 minutos

Este guia vai te ajudar a colocar o Berenice AI funcionando em minutos!

---

## Passo 1: Verifique os Pré-requisitos (2 min)

```bash
# Verifique Python 3.10+
python --version

# Deve mostrar: Python 3.10.x ou superior
```

---

## Passo 2: Configure o Ambiente (3 min)

```bash
# Já está na pasta do projeto
cd /Users/edu/Desktop/PROJETOS/berenice-ai/graphiti-agent

# Ative o ambiente virtual (se ainda não estiver ativo)
source venv/bin/activate

# Verifique as dependências
pip list | grep -E "(pydantic-ai|graphiti|fastapi)"
```

---

## Passo 3: Configure o Neo4j (5 min)

### Opção A: Neo4j já está configurado (VPS)

Seu `.env` já tem:
```env
NEO4J_URI=bolt://147.79.81.91:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=Neo4jVPS2025!
```

✅ **Pule para o Passo 4!**

### Opção B: Usar Neo4j Desktop (local)

1. Baixe [Neo4j Desktop](https://neo4j.com/download/)
2. Crie novo projeto → Adicionar DBMS local
3. Defina senha
4. Inicie o DBMS
5. Atualize o `.env`:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sua_senha_aqui
```

---

## Passo 4: Configure a OpenAI API (1 min)

```bash
# Edite o .env
nano .env

# Adicione sua chave (se ainda não tiver):
OPENAI_API_KEY=sk-...
```

**Não tem chave?** Pegue em: https://platform.openai.com/api-keys

---

## Passo 5: Configure o Z-API (3 min)

### 1. Crie uma Conta

- Acesse: https://www.z-api.io/
- Clique em "Começar Agora"
- Crie sua conta grátis

### 2. Crie uma Instância

- No painel, clique em "Nova Instância"
- Conecte seu WhatsApp (escaneie QR Code)
- Copie as credenciais:
  - **Instance ID**: `sua_instancia_id`
  - **Token**: `seu_token`
  - **Client Token**: `seu_client_token`

### 3. Atualize o .env

```env
ZAPI_INSTANCE_ID=sua_instancia_id
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token
```

---

## Passo 6: Teste as Configurações (1 min)

```bash
# Teste se as configurações estão corretas
python config/settings.py
```

**Saída esperada:**
```
✅ All settings configured correctly!
Neo4j URI: bolt://...
Clinic: Instituto Dental Life
Model: gpt-4o-mini
```

Se der erro, verifique o `.env`!

---

## Passo 7: Inicie o Servidor (1 min)

```bash
# Inicie o servidor
python main.py
```

**Saída esperada:**
```
INFO     Starting Berenice AI SDR Agent...
INFO     ✅ Configuration validated
INFO     ✅ Graphiti initialized
INFO     🚀 Application ready on http://0.0.0.0:8000
INFO     📱 Clinic: Instituto Dental Life
INFO     📍 Webhook URL: http://0.0.0.0:8000/webhook/message
```

---

## Passo 8: Exponha o Webhook com ngrok (DESENVOLVIMENTO) (2 min)

### 1. Instale ngrok

```bash
# macOS
brew install ngrok

# Ou baixe em: https://ngrok.com/download
```

### 2. Exponha a porta 8000

```bash
# Em outro terminal
ngrok http 8000
```

**Saída:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### 3. Configure o Webhook no Z-API

1. Vá para o painel Z-API
2. Clique na sua instância → **Webhooks**
3. Configure:
   - **Webhook de Mensagens**: `https://abc123.ngrok.io/webhook/message`
   - **Webhook de Status**: `https://abc123.ngrok.io/webhook/status`
4. Clique em **Salvar**

---

## Passo 9: Teste o Agente! 🎉

### 1. Envie uma Mensagem

Abra o WhatsApp e envie para o número conectado:

```
Olá
```

### 2. Aguarde a Resposta

O agente deve responder algo como:

```
Bom dia! 🌅 Sou a Berenice, do Instituto Dental Life.
Como posso ajudar você hoje?
```

### 3. Continue o Teste

```
Você: Quero fazer um clareamento

Berenice: Ótimo! O clareamento dental é...
```

---

## ✅ Funcionou? Parabéns!

### Próximos Passos:

1. **Personalize** os tratamentos em `knowledge/treatments.json`
2. **Adicione** FAQs em `knowledge/faqs.json`
3. **Ajuste** o prompt em `config/prompts.py`
4. **Teste** diferentes cenários de conversa

---

## ❌ Não Funcionou?

### Problema: Webhook não recebe mensagens

**Solução:**
- Verifique se o ngrok está rodando
- Confirme que o webhook está correto no Z-API
- Teste o webhook manualmente:

```bash
curl -X POST https://seu-ngrok.ngrok.io/webhook/health
```

### Problema: Erro ao conectar no Neo4j

**Solução:**
- Verifique se o Neo4j está rodando
- Confirme usuário e senha no `.env`
- Teste a conexão:

```bash
python -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'senha')); driver.verify_connectivity()"
```

### Problema: OpenAI API Error

**Solução:**
- Verifique se a chave está correta
- Confirme se tem créditos na conta OpenAI
- Teste a chave:

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Problema: Z-API não envia mensagens

**Solução:**
- Verifique se o WhatsApp está conectado (QR Code)
- Confirme as credenciais no `.env`
- Teste envio manual:

```bash
curl -X POST https://api.z-api.io/instances/SUA_INSTANCIA/token/SEU_TOKEN/send-text \
  -H "Client-Token: SEU_CLIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone":"5511999999999","message":"Teste"}'
```

---

## 📚 Leitura Adicional

- [README_SDR.md](README_SDR.md) - Documentação completa
- [Z-API Docs](https://developer.z-api.io/) - Documentação Z-API
- [PydanticAI Docs](https://ai.pydantic.dev/) - Documentação PydanticAI
- [Graphiti Docs](https://help.getzep.com/graphiti/) - Documentação Graphiti

---

## 💬 Precisa de Ajuda?

- **Email**: suporte@institutodental.life
- **WhatsApp**: (11) 4118-3589

---

**Boa sorte! 🍀**
