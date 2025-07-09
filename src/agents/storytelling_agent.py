# src/agents/storytelling_agent.py
"""
The "Master Storyteller" agent for the Cinematic Narrative Engine (Stage 3).
This is the final, corrected version that resolves the 'multiple values' error.
"""
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# --- Import schemas for type-safety and structured output ---
from src.core.schemas import AppState, CinematicNarrativeOutput

# ==============================================================================
# == 1. DEFINE THE LLM'S OUTPUT STRUCTURE (INTERNAL-ONLY)
# ==============================================================================
# THIS IS THE FIX: We create a model for the LLM that does NOT include the
# 'source_of_inspiration' field, so the LLM won't try to generate it.
class LLMStorytellerOutput(BaseModel):
    """Internal Pydantic model for the LLM's output."""
    before_scene_cinematic: str = Field(description="The cinematic scene describing what happened just before the image.")
    after_scene_cinematic: str = Field(description="The cinematic scene describing what happens next.")
    before_scene_prompt: str = Field(description="A refined, high-quality prompt for generating the 'Before' scene image.")
    after_scene_prompt: str = Field(description="A refined, high-quality prompt for generating the 'After' scene image.")

# ==============================================================================
# == 2. INITIALIZE THE LLM AND OUTPUT PARSER
# ==============================================================================
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# The parser now uses our new internal model, telling the LLM the correct format.
parser = JsonOutputParser(pydantic_object=LLMStorytellerOutput)

# ==============================================================================
# == 3. CREATE THE MASTER PROMPT TEMPLATE
# ==============================================================================
system_template = """
You are an expert screenwriter and a master of visual storytelling. Your task is to create a powerful, cinematic "Before and After" scene based on a creative brief.

**RULES:**
1.  **Write the scenes first:** Create a short, evocative "Before Scene" (what happened just before the key moment) and an "After Scene" (what happens immediately after).
2.  **Ground in the brief:** The scenes must be consistent with the user's core idea, genre, mood, and any inspirational motifs provided.
3.  **Create image prompts:** After writing the scenes, create two distinct, highly-detailed text-to-image prompts suitable for a model like Midjourney or DALL-E 3.
    - The "Before Prompt" must visually represent the "Before Scene".
    - The "After Prompt" must visually represent the "After Scene".
    - Prompts should be rich in visual detail, camera angles, lighting, and mood.
4.  **Format your output:** You must format your entire response as a single JSON object that perfectly matches the requested schema.

{format_instructions}
"""

human_template = """
**CREATIVE BRIEF:**
- **Core Idea:** {initial_idea}
- **Genre:** {genre}
- **Mood:** {mood}

**INSPIRATIONAL MOTIFS & CONTEXT:**
{inspiration_phrases}

**YOUR TASK:**
Based on the complete brief above, generate the cinematic scenes and their corresponding image prompts.
"""

master_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template, partial_variables={"format_instructions": parser.get_format_instructions()}),
    HumanMessagePromptTemplate.from_template(human_template)
])

# ==============================================================================
# == 4. BUILD THE FINAL AGENTIC CHAIN
# ==============================================================================
storyteller_chain = master_prompt | llm | parser

# ==============================================================================
# == 5. CREATE THE NODE FUNCTION FOR THE GRAPH
# ==============================================================================
def run_cinematic_prompt_engineer(state: AppState) -> AppState:
    """
    This is the final creative step. It calls the LLM with all gathered context
    to generate the final cinematic output.
    """
    print("---AGENT: Running Master Storyteller (Cinematic Prompt Engineer)---")
    narrative_state = state.narrative_state
    
    inspiration_text = "No specific inspiration provided."
    if narrative_state.inspiration_phrases:
        inspiration_text = "\n".join([f"- {phrase}" for phrase in narrative_state.inspiration_phrases])

    print("   - Synthesizing all context and calling GPT-4o...")
    try:
        # The LLM now returns a dict matching LLMStorytellerOutput.
        llm_response_dict: Dict = storyteller_chain.invoke({
            "initial_idea": narrative_state.initial_idea,
            "genre": narrative_state.genre,
            "mood": narrative_state.mood,
            "inspiration_phrases": inspiration_text,
        })
        
        # We now safely construct the final CinematicNarrativeOutput object.
        # There is no conflict because the LLM response doesn't contain the 'source_of_inspiration' key.
        final_output = CinematicNarrativeOutput(
            **llm_response_dict, # Unpack the LLM's response
            source_of_inspiration=f"{narrative_state.inspiration_mode} - {narrative_state.story_reference or 'N/A'}"
        )
        
        print("   - GPT-4o generation complete.")
        narrative_state.cinematic_output = final_output

    except Exception as e:
        print(f"   - ERROR in Storyteller Agent: {e}")
        narrative_state.cinematic_output = CinematicNarrativeOutput(
            before_scene_cinematic="An error occurred while generating the story.",
            after_scene_cinematic="Please check your API keys and try again.",
            before_scene_prompt="error",
            after_scene_prompt="error",
            source_of_inspiration="Error"
        )
    
    # Lock the UI and update the state
    narrative_state.is_locked = True
    state.narrative_state = narrative_state
    
    return state