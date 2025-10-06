#!/usr/bin/env python3
"""Test Neo4j and OpenAI API connections"""

import os
from openai import OpenAI
from neo4j import GraphDatabase

def test_openai():
    """Test OpenAI API connection"""
    print("🔍 Testing OpenAI API connection...")
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False

        client = OpenAI(api_key=api_key)

        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Connection successful!' if you can read this."}],
            max_tokens=20
        )

        result = response.choices[0].message.content
        print(f"✅ OpenAI API connected successfully!")
        print(f"   Response: {result}")
        return True

    except Exception as e:
        print(f"❌ OpenAI API connection failed: {str(e)}")
        return False

def test_neo4j():
    """Test Neo4j database connection"""
    print("\n🔍 Testing Neo4j connection...")
    try:
        uri = os.getenv('NEO4J_URI')
        user = os.getenv('NEO4J_USER')
        password = os.getenv('NEO4J_PASSWORD')

        if not all([uri, user, password]):
            print("❌ Neo4j credentials not found in environment")
            return False

        print(f"   URI: {uri}")
        print(f"   User: {user}")

        driver = GraphDatabase.driver(uri, auth=(user, password))

        # Verify connection
        driver.verify_connectivity()

        # Test with a simple query
        with driver.session() as session:
            result = session.run("RETURN 'Connection successful!' AS message, datetime() AS timestamp")
            record = result.single()

            print(f"✅ Neo4j connected successfully!")
            print(f"   Message: {record['message']}")
            print(f"   Timestamp: {record['timestamp']}")

        driver.close()
        return True

    except Exception as e:
        print(f"❌ Neo4j connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Connection Tests")
    print("=" * 60)

    # Load environment variables from .env.example if .env doesn't exist
    if not os.path.exists('.env'):
        print("⚠️  .env file not found, using .env.example values\n")
        with open('.env.example', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

    openai_ok = test_openai()
    neo4j_ok = test_neo4j()

    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"OpenAI API: {'✅ OK' if openai_ok else '❌ FAILED'}")
    print(f"Neo4j:      {'✅ OK' if neo4j_ok else '❌ FAILED'}")
    print("=" * 60)
