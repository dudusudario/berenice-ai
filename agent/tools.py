"""
Custom tools for the SDR agent.
"""
import json
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Load knowledge base
KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

with open(KNOWLEDGE_DIR / "treatments.json", "r", encoding="utf-8") as f:
    TREATMENTS_DATA = json.load(f)

with open(KNOWLEDGE_DIR / "faqs.json", "r", encoding="utf-8") as f:
    FAQS_DATA = json.load(f)


def search_treatment(query: str) -> List[Dict[str, Any]]:
    """
    Search for treatments based on keywords.

    Args:
        query: Search query (treatment type, symptoms, etc.)

    Returns:
        List of matching treatments with details
    """
    query_lower = query.lower()
    matches = []

    for treatment in TREATMENTS_DATA["treatments"]:
        # Check if query matches treatment name or keywords
        if query_lower in treatment["name"].lower() or any(
            keyword in query_lower for keyword in treatment.get("keywords", [])
        ):
            matches.append(
                {
                    "name": treatment["name"],
                    "description": treatment["description"],
                    "duration": treatment["duration"],
                    "price_range": treatment["price_range"],
                    "benefits": treatment["benefits"],
                }
            )

    logger.info(f"Found {len(matches)} treatments for query: {query}")
    return matches


def get_treatment_info(treatment_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific treatment.

    Args:
        treatment_id: Treatment ID (e.g., 'limpeza', 'clareamento')

    Returns:
        Treatment details
    """
    for treatment in TREATMENTS_DATA["treatments"]:
        if treatment["id"] == treatment_id:
            return treatment

    return {}


def search_faq(query: str) -> List[Dict[str, str]]:
    """
    Search for FAQs matching the query.

    Args:
        query: Search query

    Returns:
        List of matching FAQs
    """
    query_lower = query.lower()
    matches = []

    for faq in FAQS_DATA["faqs"]:
        if query_lower in faq["question"].lower() or query_lower in faq["answer"].lower():
            matches.append({"question": faq["question"], "answer": faq["answer"]})

    logger.info(f"Found {len(matches)} FAQs for query: {query}")
    return matches[:3]  # Return top 3 matches


def get_objection_response(objection_type: str) -> List[str]:
    """
    Get responses for handling common objections.

    Args:
        objection_type: Type of objection (e.g., 'price', 'time', 'fear')

    Returns:
        List of suggested responses
    """
    objection_lower = objection_type.lower()

    for objection in FAQS_DATA["objection_handling"]:
        if objection_lower in objection["objection"].lower():
            return objection["responses"]

    return []


def get_payment_options() -> Dict[str, Any]:
    """
    Get available payment options.

    Returns:
        Dictionary with payment options
    """
    return TREATMENTS_DATA["payment_options"]


def get_insurance_list() -> List[str]:
    """
    Get list of accepted insurance providers.

    Returns:
        List of insurance names
    """
    return TREATMENTS_DATA["accepted_insurance"]


def calculate_installments(amount: float, months: int = 12) -> Dict[str, Any]:
    """
    Calculate installment options for a given amount.

    Args:
        amount: Total amount
        months: Number of months (default: 12)

    Returns:
        Installment calculation
    """
    installment_no_interest = amount / months
    installment_with_interest = (amount * 1.15) / 18  # 15% interest for 18 months

    return {
        "total_amount": amount,
        "no_interest": {
            "months": months,
            "monthly_payment": round(installment_no_interest, 2),
            "total": amount,
        },
        "with_interest": {
            "months": 18,
            "monthly_payment": round(installment_with_interest, 2),
            "total": round(amount * 1.15, 2),
        },
        "pix_discount": {
            "discount_percent": 5,
            "final_amount": round(amount * 0.95, 2),
        },
    }


# Mock availability checker (replace with real calendar integration)
def check_availability(preferred_period: str = None) -> List[Dict[str, str]]:
    """
    Check available appointment slots.

    Args:
        preferred_period: Preferred period (morning, afternoon, evening)

    Returns:
        List of available slots
    """
    # This is a mock - in production, integrate with real calendar
    available_slots = [
        {"date": "2025-10-08", "time": "09:00", "period": "morning"},
        {"date": "2025-10-08", "time": "14:00", "period": "afternoon"},
        {"date": "2025-10-09", "time": "10:30", "period": "morning"},
        {"date": "2025-10-09", "time": "16:00", "period": "afternoon"},
        {"date": "2025-10-10", "time": "18:30", "period": "evening"},
    ]

    if preferred_period:
        available_slots = [
            slot for slot in available_slots if slot["period"] == preferred_period
        ]

    return available_slots[:5]  # Return max 5 slots
