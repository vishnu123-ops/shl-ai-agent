from services.parser import (
    analyze_conversation
)

from services.retriever import (
    retrieve_assessments
)

import json


# Load catalog
with open(
    "data/shl_catalog.json",
    "r"
) as f:

    catalog = json.load(f)


def compare_assessments(query):

    query = query.lower()

    if "opq" in query and "gsa" in query:

        return {
            "reply": (
                "OPQ32r is a personality assessment "
                "focused on workplace behavior and "
                "preferences, while GSA evaluates "
                "general cognitive and reasoning ability."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    return None


def process_chat(messages):

    latest_user_message = (
        messages[-1].content
    )

    analysis = analyze_conversation(
        messages
    )

    full_text = analysis["full_text"]

    # =========================
    # Prompt Injection Protection
    # =========================

    if analysis["prompt_injection"]:

        return {
            "reply": (
                "I can only help with "
                "SHL assessment recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =========================
    # Off-topic Refusal
    # =========================

    if analysis["off_topic"]:

        return {
            "reply": (
                "I can only help with "
                "SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =========================
    # Comparison Questions
    # =========================

    comparison_response = (
        compare_assessments(full_text)
    )

    if comparison_response:

        return comparison_response

    # =========================
    # Dynamic Clarifications
    # =========================

    if not analysis["has_role"]:

        return {
            "reply": (
                "What role are you hiring for?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    if analysis["experience"] is None:

        return {
            "reply": (
                "What experience level are "
                "you targeting? "
                "(Entry, Mid, or Senior)"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    if (
        not analysis["needs_coding"]
        and not analysis["needs_personality"]
    ):

        return {
            "reply": (
                "Do you need coding assessments, "
                "personality assessments, "
                "or both?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =========================
    # Retrieval
    # =========================

    results = retrieve_assessments(
        full_text,
        analysis
    )

    recommendations = []

    for item in results:

        recommendations.append({

            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]

        })

    # =========================
    # Empty Results
    # =========================

    if len(recommendations) == 0:

        return {
            "reply": (
                "I could not find strong "
                "matching SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # =========================
    # Better Explanation
    # =========================

    explanation_parts = []

    if analysis["needs_coding"]:

        explanation_parts.append(
            "technical coding requirements"
        )

    if analysis["needs_personality"]:

        explanation_parts.append(
            "personality and communication requirements"
        )

    explanation = (
        "These assessments match your "
        + " and ".join(explanation_parts)
        + "."
    )

    # =========================
    # Final Response
    # =========================

    return {
        "reply": explanation,
        "recommendations": recommendations,
        "end_of_conversation": True
    }