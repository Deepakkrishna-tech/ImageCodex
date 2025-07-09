# src/agents/film_story_writer.py
# FINAL VERIFIED VERSION - Simplified input for maximum reliability.

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import StoryArc
from ..core.prompts import FILM_STORY_WRITER_PROMPT

def film_story_writer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Takes a creative brief and generates a full, structured StoryArc."""
    print("---AGENT: FILM STORY WRITER---")
    
    narrative_state = state.get("narrative_state", {})
    visual_analysis = state.get("visual_analysis")

    llm = ChatOpenAI(model="gpt-4o", temperature=0.7, model_kwargs={"response_format": {"type": "json_object"}})
    structured_llm = llm.with_structured_output(StoryArc)
    prompt_template = ChatPromptTemplate.from_template(FILM_STORY_WRITER_PROMPT)
    chain = prompt_template | structured_llm

    # --- THIS IS THE FIX ---
    # Instead of passing a complex JSON string, we pass a simple summary string.
    # This gives the `with_structured_output` tool the best possible chance to succeed.
    if visual_analysis:
        analysis_summary = (
            f"Subject: {visual_analysis.main_subject}. "
            f"Setting: {visual_analysis.setting_and_environment}. "
            f"Style: {visual_analysis.artistic_style}. "
            f"Mood: {visual_analysis.mood_and_atmosphere}."
        )
    else:
        analysis_summary = "N/A"
    
    response = chain.invoke({
        "visual_analysis": analysis_summary,
        "genre": narrative_state.get("genre", "Filmmaker's Choice"),
        "mood": narrative_state.get("mood", "Filmmaker's Choice"),
        "initial_idea": narrative_state.get("initial_idea", "None provided.")
    })
    
    print("---AGENT: Generated Story Arc---")
    
    # Update and return the entire state correctly
    state["narrative_state"]["story_arc"] = response
    return state