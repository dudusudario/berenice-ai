"""
Script para testar se todas as configurações estão corretas.
Execute: python test_setup.py
"""
import asyncio
import sys
from pathlib import Path

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


async def test_env_file():
    """Test if .env file exists and is configured."""
    print_header("1. Testando arquivo .env")

    env_file = Path(".env")

    if not env_file.exists():
        print_error("Arquivo .env não encontrado!")
        print_info("Copie .env.example para .env e configure as variáveis")
        return False

    print_success("Arquivo .env encontrado")

    # Read and check required variables
    with open(env_file, 'r') as f:
        content = f.read()

    required_vars = [
        "NEO4J_URI",
        "NEO4J_PASSWORD",
        "OPENAI_API_KEY",
        "ZAPI_INSTANCE_ID",
        "ZAPI_TOKEN",
        "CLINIC_NAME"
    ]

    missing = []
    for var in required_vars:
        if var not in content or f"{var}=your_" in content or f"{var}=\n" in content:
            missing.append(var)

    if missing:
        print_error(f"Variáveis não configuradas: {', '.join(missing)}")
        return False

    print_success("Todas as variáveis obrigatórias estão configuradas")
    return True


async def test_dependencies():
    """Test if required packages are installed."""
    print_header("2. Testando dependências")

    required_packages = [
        ("fastapi", "FastAPI"),
        ("pydantic_ai", "PydanticAI"),
        ("graphiti_core", "Graphiti"),
        ("httpx", "HTTPX"),
        ("uvicorn", "Uvicorn"),
    ]

    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            print_success(f"{name} instalado")
        except ImportError:
            print_error(f"{name} NÃO instalado")
            all_ok = False

    return all_ok


async def test_settings():
    """Test if settings can be loaded."""
    print_header("3. Testando configurações")

    try:
        from config.settings import settings, validate_settings

        print_success("Módulo de configurações carregado")

        try:
            validate_settings()
            print_success("Configurações validadas com sucesso")

            print_info(f"Clínica: {settings.clinic_name}")
            print_info(f"Neo4j: {settings.neo4j_uri}")
            print_info(f"Model: {settings.model_choice}")

            return True
        except ValueError as e:
            print_error(f"Erro na validação: {e}")
            return False

    except Exception as e:
        print_error(f"Erro ao carregar configurações: {e}")
        return False


async def test_neo4j():
    """Test Neo4j connection."""
    print_header("4. Testando conexão Neo4j")

    try:
        from neo4j import GraphDatabase
        from config.settings import settings

        driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )

        print_info("Conectando ao Neo4j...")
        driver.verify_connectivity()
        print_success("Conexão Neo4j estabelecida com sucesso!")

        # Test query
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            if record["test"] == 1:
                print_success("Consulta de teste executada com sucesso")

        driver.close()
        return True

    except Exception as e:
        print_error(f"Erro ao conectar no Neo4j: {e}")
        print_warning("Verifique se o Neo4j está rodando e as credenciais estão corretas")
        return False


async def test_openai():
    """Test OpenAI API connection."""
    print_header("5. Testando API OpenAI")

    try:
        from openai import OpenAI
        from config.settings import settings

        client = OpenAI(api_key=settings.openai_api_key)

        print_info("Testando conexão com OpenAI...")

        # Simple test
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Responda apenas: OK"}],
            max_tokens=5
        )

        if response.choices:
            print_success("API OpenAI funcionando!")
            print_info(f"Resposta: {response.choices[0].message.content}")
            return True

    except Exception as e:
        print_error(f"Erro ao testar OpenAI API: {e}")
        print_warning("Verifique se a chave API está correta e tem créditos")
        return False


async def test_zapi():
    """Test Z-API configuration."""
    print_header("6. Testando configuração Z-API")

    try:
        from services.zapi_service import ZAPIService
        import httpx

        print_info("Verificando credenciais Z-API...")

        # Just check if service can be instantiated
        service = ZAPIService()
        print_success("Serviço Z-API configurado")

        # Try to check instance status (optional)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{service.base_url.replace('/token/', '/token/')}/status",
                    headers=service.headers,
                    timeout=10.0
                )
                if response.status_code == 200:
                    print_success("Instância Z-API ativa!")
                else:
                    print_warning("Não foi possível verificar status da instância")
        except:
            print_warning("Não foi possível verificar status da instância (isso é normal)")

        return True

    except Exception as e:
        print_error(f"Erro ao testar Z-API: {e}")
        return False


async def test_knowledge_base():
    """Test if knowledge base files exist."""
    print_header("7. Testando base de conhecimento")

    files = [
        "knowledge/treatments.json",
        "knowledge/faqs.json"
    ]

    all_ok = True
    for file_path in files:
        if Path(file_path).exists():
            print_success(f"{file_path} encontrado")
        else:
            print_error(f"{file_path} NÃO encontrado")
            all_ok = False

    return all_ok


async def test_graphiti_init():
    """Test Graphiti initialization."""
    print_header("8. Testando Graphiti")

    try:
        from services.graphiti_service import GraphitiService

        service = GraphitiService()
        print_info("Inicializando Graphiti...")

        await service.initialize()
        print_success("Graphiti inicializado com sucesso!")

        await service.close()
        return True

    except Exception as e:
        print_error(f"Erro ao inicializar Graphiti: {e}")
        return False


async def main():
    """Run all tests."""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        BERENICE AI - TESTE DE CONFIGURAÇÃO                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.END)

    tests = [
        ("Arquivo .env", test_env_file),
        ("Dependências", test_dependencies),
        ("Configurações", test_settings),
        ("Neo4j", test_neo4j),
        ("OpenAI API", test_openai),
        ("Z-API", test_zapi),
        ("Base de Conhecimento", test_knowledge_base),
        ("Graphiti", test_graphiti_init),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))

    # Summary
    print_header("RESUMO DOS TESTES")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSOU")
        else:
            print_error(f"{test_name}: FALHOU")

    print(f"\n{Colors.BOLD}")
    print(f"Resultado: {passed}/{total} testes passaram")
    print(Colors.END)

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Tudo configurado corretamente!{Colors.END}")
        print(f"{Colors.GREEN}Você pode iniciar o servidor com: python main.py{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  Alguns testes falharam!{Colors.END}")
        print(f"{Colors.YELLOW}Verifique as mensagens de erro acima e corrija os problemas.{Colors.END}\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
