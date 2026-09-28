"""
AI Briefing and Synthesis Client for MacroLens V1.
Generates dynamic, evidence-first macroeconomic briefings directly from verified indicators.
Clearly communicates the offline baseline mode without enabling premature API integration.
"""

from typing import Dict
from core.models import MacroIndicator
from core.normalizer import generate_dynamic_offline_synthesis


def get_macro_briefing(indicators: Dict[str, MacroIndicator]) -> str:
    """
    Returns the dynamic, evidence-first macroeconomic synthesis generated
    directly from the currently loaded indicators dataset.
    Guarantees zero fabrication and automatic synchronization with macro_seed.json.
    """
    return generate_dynamic_offline_synthesis(indicators)


__all__ = ["get_macro_briefing"]
