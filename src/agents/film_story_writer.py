# src/agents/film_story_writer.py
# FINAL VERIFIED VERSION - Now acts as a Story Concept Generator.

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import StoryConceptCollection # Import the new schema
from ..core.prompts import STORY_CONCEPT_GENERATOR_PROMPT # Import the new prompt

def story_concept_generator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Takes a creative brief and generates a collection of distinct story concepts."""
    print("---AGENT: STORY CONCEPT GENERATOR---")
    
    narrative_state = state.get("narrative_state", {})
    visual_analysis = state.get("visual_analysis")

    llm = ChatOpenAI(model="gpt-4o", temperature=0.8, model_kwargs={"response_format": {"type": "json_object"}})
    # Tell the tool to output our new collection schema
    structured_llm = llm.with_structured_output(StoryConceptCollection)
    prompt_template = ChatPromptTemplate.from_template(STORY_CONCEPT_GENERATOR_PROMPT)
    chain = prompt_template | structured_llm

    if visual_analysis:
        analysis_summary = (f"Subject: {visual_analysis.main_subject}. Setting: {visual_analysis.setting_and_environment}. Style: {visual_analysis.artistic_style}. Mood: {visual_analysis.mood_and_atmosphere}.")
    else:
        analysis_summary = "N/A"
    
    response = chain.invoke({
        "visual_analysis": analysis_summary,
        "genre": narrative_state.get("genre", "Filmmaker's Choice"),
        "mood": narrative_state.get("mood", "Filmmaker's Choice"),
        "initial_idea": narrative_state.get("initial_idea", "None provided.")
    })
    
    print("---AGENT: Generated Story Concepts---")
    
    # Update the state with the new concepts
    state["narrative_state"]["story_concepts"] = response
    return state