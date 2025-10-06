"""
Configuration settings for the Berenice AI SDR Agent.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Neo4j Connection
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    # OpenAI API
    openai_api_key: str = ""
    model_choice: str = "gpt-4o-mini"

    # Z-API Configuration
    zapi_instance_id: str = ""
    zapi_token: str = ""
    zapi_client_token: str = ""
    zapi_base_url: str = "https://api.z-api.io"

    # Clinic Configuration
    clinic_name: str = "Clínica Berenice"
    clinic_phone: str = ""
    clinic_address: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_settings():
    """Validate that all required settings are configured."""
    required_fields = [
        "neo4j_password",
        "openai_api_key",
        "zapi_instance_id",
        "zapi_token",
        "clinic_phone",
    ]

    missing_fields = []
    for field in required_fields:
        value = getattr(settings, field, None)
        if not value or value == f"your_{field}":
            missing_fields.append(field.upper())

    if missing_fields:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing_fields)}. "
            f"Please check your .env file."
        )


if __name__ == "__main__":
    # Test configuration
    try:
        validate_settings()
        print("✅ All settings configured correctly!")
        print(f"Neo4j URI: {settings.neo4j_uri}")
        print(f"Clinic: {settings.clinic_name}")
        print(f"Model: {settings.model_choice}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
