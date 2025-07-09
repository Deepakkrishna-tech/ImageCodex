# src/agents/context_engineer.py
"""
The Context Engineer agent fuses visual analysis, user prompts, genre, mood,
and reference story motifs into a unified narrative context.
"""
from typing import Dict, Any

# --- CORRECTED: Import AppState for type-safe function signature ---
from src.core.schemas import AppState

# --- CORRECTED: The function now correctly uses AppState for input and output ---
def run_context_engineer(state: AppState) -> AppState:
    """
    Combines all inputs into a coherent context summary for the prompt engineer.
    """
    print("---AGENT: Running Context Engineer---")
    narrative_state = state.narrative_state
    
    initial_idea = narrative_state.initial_idea or 'An unknown moment.'
    genre = narrative_state.genre
    mood = narrative_state.mood
    mode = narrative_state.inspiration_mode
    reference = narrative_state.story_reference

    context_parts = [
        f"The core idea is: '{initial_idea}'.",
        f"The genre is {genre} with a {mood} mood.",
    ]
    if reference:
        context_parts.append(f"The narrative is '{mode}' the story of '{reference}'.")
    else:
        context_parts.append("The narrative should be pure AI imagination.")

    # Add any phrases from the inspiration/reference agents to the context
    if narrative_state.inspiration_phrases:
        context_parts.append("\nInspirational Motifs:")
        for phrase in narrative_state.inspiration_phrases:
            context_parts.append(f"- {phrase}")

    context_summary = "\n".join(context_parts)
    print(f"   - Generated Context Summary:\n{context_summary}")

    # Update the state object directly
    narrative_state.context_summary = context_summary
    state.narrative_state = narrative_state
    
    return state