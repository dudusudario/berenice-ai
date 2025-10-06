"""
SDR Agent for dental clinic using PydanticAI.
"""
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from config.settings import settings
from config.prompts import SDR_SYSTEM_PROMPT
from services.graphiti_service import graphiti_service
from agent.tools import (
    search_treatment,
    get_treatment_info,
    search_faq,
    get_objection_response,
    get_payment_options,
    get_insurance_list,
    calculate_installments,
    check_availability,
)

logger = logging.getLogger(__name__)


# ========== Define dependencies ==========
@dataclass
class SDRDependencies:
    """Dependencies for the SDR agent."""

    phone: str
    patient_name: str = "paciente"
    graphiti_client: Any = None


# ========== Define result models ==========
class TreatmentResult(BaseModel):
    """Model for treatment search results."""

    name: str
    description: str
    price_range: str
    duration: str
    benefits: List[str]


class PatientHistoryResult(BaseModel):
    """Model for patient history from knowledge graph."""

    uuid: str
    fact: str
    valid_at: str = ""
    invalid_at: str = ""


class AvailabilitySlot(BaseModel):
    """Model for appointment availability."""

    date: str
    time: str
    period: str


# ========== Helper function to get model configuration ==========
def get_model():
    """Configure and return the LLM model to use."""
    model_choice = settings.model_choice
    api_key = settings.openai_api_key

    return OpenAIModel(model_choice, provider=OpenAIProvider(api_key=api_key))


# ========== Create the SDR agent ==========
sdr_agent = Agent(
    get_model(),
    system_prompt=SDR_SYSTEM_PROMPT.format(clinic_name=settings.clinic_name),
    deps_type=SDRDependencies,
)


# ========== Define tools ==========
@sdr_agent.tool
async def search_patient_history(
    ctx: RunContext[SDRDependencies], query: str
) -> List[PatientHistoryResult]:
    """
    Search the patient's history in the knowledge graph.

    Use this to:
    - Check if patient has contacted before
    - See previous conversations
    - Find out what treatments they were interested in
    - Understand their preferences and objections

    Args:
        ctx: The run context containing dependencies
        query: Search query (patient phone, name, or treatment interest)

    Returns:
        List of relevant facts about the patient
    """
    try:
        if not ctx.deps.graphiti_client:
            logger.warning("Graphiti client not available")
            return []

        # Search with patient phone first
        results = await ctx.deps.graphiti_client.search_patient_history(
            f"{ctx.deps.phone} {query}", limit=5
        )

        formatted_results = []
        for result in results:
            formatted_results.append(
                PatientHistoryResult(
                    uuid=result.get("uuid", ""),
                    fact=result.get("fact", ""),
                    valid_at=result.get("valid_at", ""),
                    invalid_at=result.get("invalid_at", ""),
                )
            )

        return formatted_results
    except Exception as e:
        logger.error(f"Error searching patient history: {e}")
        return []


@sdr_agent.tool
def find_treatment_info(
    ctx: RunContext[SDRDependencies], treatment_query: str
) -> List[TreatmentResult]:
    """
    Search for dental treatments based on patient needs.

    Use this to:
    - Find treatments matching patient symptoms/needs
    - Get pricing information
    - Explain treatment benefits
    - Provide treatment duration and process

    Args:
        ctx: The run context
        treatment_query: What the patient is looking for (e.g., "clareamento", "dentes tortos", "implante")

    Returns:
        List of matching treatments with details
    """
    try:
        treatments = search_treatment(treatment_query)
        return [TreatmentResult(**t) for t in treatments]
    except Exception as e:
        logger.error(f"Error finding treatment info: {e}")
        return []


@sdr_agent.tool
def get_frequently_asked_questions(
    ctx: RunContext[SDRDependencies], question_topic: str
) -> List[Dict[str, str]]:
    """
    Search frequently asked questions and answers.

    Use this to:
    - Answer common patient questions
    - Provide accurate information about policies
    - Share clinic details

    Args:
        ctx: The run context
        question_topic: Topic or keywords from the patient's question

    Returns:
        List of relevant FAQ items
    """
    try:
        return search_faq(question_topic)
    except Exception as e:
        logger.error(f"Error searching FAQs: {e}")
        return []


@sdr_agent.tool
def handle_objection(
    ctx: RunContext[SDRDependencies], objection_type: str
) -> List[str]:
    """
    Get responses for handling common objections.

    Use this when patient expresses concerns about:
    - Price ("muito caro", "não tenho dinheiro")
    - Time ("não tenho tempo", "muito ocupado")
    - Fear ("tenho medo", "fico nervoso")
    - Indecision ("vou pensar", "preciso ver com a família")

    Args:
        ctx: The run context
        objection_type: Type of objection (price, time, fear, etc.)

    Returns:
        List of suggested responses to address the objection
    """
    try:
        return get_objection_response(objection_type)
    except Exception as e:
        logger.error(f"Error handling objection: {e}")
        return []


@sdr_agent.tool
def show_payment_options(ctx: RunContext[SDRDependencies]) -> Dict[str, Any]:
    """
    Get all available payment options.

    Use this to:
    - Explain payment methods
    - Show installment options
    - Mention discounts

    Args:
        ctx: The run context

    Returns:
        Dictionary with payment options
    """
    try:
        return get_payment_options()
    except Exception as e:
        logger.error(f"Error getting payment options: {e}")
        return {}


@sdr_agent.tool
def calculate_payment_plan(
    ctx: RunContext[SDRDependencies], amount: float, months: int = 12
) -> Dict[str, Any]:
    """
    Calculate installment options for a specific amount.

    Use this to:
    - Show monthly payment values
    - Compare different payment plans
    - Calculate PIX discount

    Args:
        ctx: The run context
        amount: Total amount in BRL
        months: Number of months for installment (default: 12)

    Returns:
        Detailed payment calculation
    """
    try:
        return calculate_installments(amount, months)
    except Exception as e:
        logger.error(f"Error calculating payment plan: {e}")
        return {}


@sdr_agent.tool
def check_insurance_accepted(ctx: RunContext[SDRDependencies]) -> List[str]:
    """
    Get list of accepted dental insurance plans.

    Use this when patient asks about:
    - Convênio odontológico
    - Plano de saúde
    - Whether we accept their insurance

    Args:
        ctx: The run context

    Returns:
        List of accepted insurance providers
    """
    try:
        return get_insurance_list()
    except Exception as e:
        logger.error(f"Error getting insurance list: {e}")
        return []


@sdr_agent.tool
def find_available_appointments(
    ctx: RunContext[SDRDependencies], preferred_period: str = None
) -> List[AvailabilitySlot]:
    """
    Check available appointment slots.

    Use this to:
    - Show available dates and times
    - Propose appointment options
    - Help patient schedule

    Args:
        ctx: The run context
        preferred_period: Patient's preferred period (morning, afternoon, evening)

    Returns:
        List of available appointment slots
    """
    try:
        slots = check_availability(preferred_period)
        return [AvailabilitySlot(**slot) for slot in slots]
    except Exception as e:
        logger.error(f"Error checking availability: {e}")
        return []


# ========== Main agent execution function ==========
async def process_patient_message(
    phone: str, patient_name: str, message: str
) -> str:
    """
    Process a patient message and generate a response.

    Args:
        phone: Patient phone number
        patient_name: Patient name
        message: Patient message

    Returns:
        Agent response
    """
    try:
        # Create dependencies
        deps = SDRDependencies(
            phone=phone, patient_name=patient_name, graphiti_client=graphiti_service
        )

        # Run agent
        result = await sdr_agent.run(message, deps=deps)

        return result.data

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return (
            "Desculpe, tive um problema ao processar sua mensagem. "
            "Pode repetir ou reformular sua pergunta? 😊"
        )
