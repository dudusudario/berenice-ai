# Demo do Agente Graphiti

Aqui demonstramos o poder do Graphiti, uma solução de grafo de conhecimento temporal que permite que agentes de IA mantenham e consultem conhecimento em evolução ao longo do tempo. A implementação mostra como usar o Graphiti com Pydantic AI para construir agentes inteligentes que podem raciocinar sobre fatos em constante mudança.

## Visão Geral

Esta demo inclui três componentes principais:

1. **Exemplo de Início Rápido (`quickstart.py`)**: Um tutorial abrangente demonstrando os recursos principais do Graphiti.
2. **Interface do Agente (`agent.py`)**: Um agente conversacional alimentado por Pydantic AI que pode pesquisar e consultar o grafo de conhecimento do Graphiti.
3. **Demo de Evolução de LLM (`llm_evolution.py`)**: Uma simulação mostrando como o conhecimento evolui ao longo do tempo, com três fases de desenvolvimento de LLM que atualizam o grafo de conhecimento.

## Pré-requisitos

- Python 3.10 ou superior
- Neo4j 5.26 ou superior (para armazenar o grafo de conhecimento)
- Chave da API OpenAI (para inferência de LLM e embeddings)

## Instalação

### 1. Configure um ambiente virtual

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o Neo4j

Você tem algumas opções fáceis para configurar o Neo4j:

#### Opção A: Usando Local-AI-Packaged (Configuração Simplificada)
1. Clone o repositório: `git clone https://github.com/coleam00/local-ai-packaged`
2. Siga as instruções de instalação para configurar o Neo4j através do pacote
3. Anote o nome de usuário e senha que você definiu no .env e o URI será bolt://localhost:7687

#### Opção B: Usando Neo4j Desktop
1. Baixe e instale o [Neo4j Desktop](https://neo4j.com/download/)
2. Crie um novo projeto e adicione um DBMS local
3. Inicie o DBMS e defina uma senha
4. Anote os detalhes da conexão (URI, nome de usuário, senha)

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
MODEL_CHOICE=gpt-4.1-mini  # Or another OpenAI model
```

## Executando a Demo

### 1. Execute o Exemplo de Início Rápido

Para se familiarizar com os recursos principais do Graphiti:

```bash
python quickstart.py
```

Isso irá demonstrar:
- Adicionar episódios ao grafo de conhecimento
- Realizar pesquisas básicas
- Usar busca de nó central para resultados sensíveis ao contexto
- Utilizar receitas de pesquisa para recuperação de nós

### 2. Experimente o Poder do Conhecimento Temporal

Para ver como o conhecimento evolui ao longo do tempo, execute a demo de evolução de LLM em um terminal:

```bash
python llm_evolution.py
```

**⚠️ AVISO: Executar este script irá limpar todos os dados existentes no seu banco de dados Neo4j!**

Esta demo interativa irá:
1. Adicionar informações sobre os principais LLMs atuais (Gemini, Claude, GPT-4.1)
2. Atualizar o grafo de conhecimento quando Claude 4 emerge como o melhor LLM
3. Atualizar novamente quando MLMs tornam os LLMs tradicionais obsoletos

O script fará pausas entre as fases, permitindo que você interaja com o agente para ver como seu conhecimento muda.

### 3. Interaja com o Agente

Em um terminal separado, execute a interface do agente:

```bash
python agent.py
```

Isso iniciará uma interface conversacional onde você pode:
1. Fazer perguntas sobre LLMs
2. Ver o agente recuperar informações do grafo de conhecimento
3. Experimentar como as respostas do agente mudam conforme o grafo de conhecimento evolui

## Fluxo de Trabalho da Demo

Para a melhor experiência de demonstração:

1. Comece com um banco de dados Neo4j limpo
2. No Terminal 1: Execute `python llm_evolution.py` e complete a Fase 1
3. No Terminal 2: Execute `python agent.py` e pergunte "Qual é o melhor LLM?"
4. No Terminal 1: Continue para a Fase 2 digitando "continue"
5. No Terminal 2: Faça a mesma pergunta novamente para ver o conhecimento atualizado
6. No Terminal 1: Continue para a Fase 3
7. No Terminal 2: Pergunte "Os LLMs ainda são relevantes?" para ver a evolução final

Este fluxo de trabalho demonstra como o Graphiti mantém conhecimento temporal e como as respostas do agente se adaptam ao grafo de conhecimento em mudança.

## Recursos Principais

- **Conhecimento Temporal**: O Graphiti rastreia quando os fatos se tornam válidos e inválidos
- **Busca Híbrida**: Combina similaridade semântica e recuperação de texto BM25
- **Consultas Sensíveis ao Contexto**: Reordena resultados com base na distância do grafo
- **Suporte a Dados Estruturados**: Funciona com episódios em texto e JSON
- **Integração Fácil**: Funciona perfeitamente com Pydantic AI para desenvolvimento de agentes

## Estrutura do Projeto

- `agent.py`: Agente Pydantic AI com capacidades de pesquisa do Graphiti
- `quickstart.py`: Tutorial demonstrando recursos principais do Graphiti
- `llm_evolution.py`: Demo mostrando como o conhecimento evolui ao longo do tempo
- `requirements.txt`: Dependências do projeto
- `.env`: Configuração para chaves de API e conexão Neo4j

## Recursos Adicionais

- [Documentação do Graphiti](https://help.getzep.com/graphiti/graphiti/overview)
- [Documentação do Pydantic AI](https://ai.pydantic.dev/)
- [Documentação do Neo4j](https://neo4j.com/docs/)

## Licença

Este projeto inclui código da Zep Software, Inc. sob a Licença Apache 2.0.
