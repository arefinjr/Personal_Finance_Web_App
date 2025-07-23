"""
Compute a simple, human-readable financial-health score
based on monthly income vs. expenses.

score = (income - expenses) / income   (if income > 0)
"""

from typing import Literal

Score = Literal["Very Bad", "Bad", "Moderate", "Good", "Very Good"]

def calculate_health_score(income: float, expenses: float) -> Score:
    """
    income  – total monthly income
    expenses – total monthly expenses
    Returns one of five qualitative ratings.
    """
    if income <= 0:
        return "Very Bad"

    ratio = expenses / income

    if ratio > 1.0:
        return "Very Bad"
    elif ratio > 0.8:
        return "Bad"
    elif ratio > 0.6:
        return "Moderate"
    elif ratio > 0.4:
        return "Good"
    else:
        return "Very Good"


def health_color(score: Score) -> str:
    """Bootstrap colour class for UI badges."""
    mapping = {
        "Very Bad": "danger",
        "Bad": "warning",
        "Moderate": "secondary",
        "Good": "success",
        "Very Good": "primary",
    }
    return mapping[score]