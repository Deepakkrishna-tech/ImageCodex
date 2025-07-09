# src/agents/inspiration_agent.py
"""
The Inspiration Agent enriches narrative prompts with poetic metaphors.
FINAL CORRECTED VERSION: Fixes the bug caused by the new TavilySearch output format.
"""
import json
from pathlib import Path
from typing import List, Dict
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from src.core.schemas import AppState

class CreativeInspiration(BaseModel):
    thematic_elements: List[str] = Field(description="A list of 2-3 core thematic elements or feelings (e.g., 'a sense of inevitable loss', 'the triumph of community').")
    visual_style_notes: List[str] = Field(description="A list of 2-3 visual style notes or motifs (e.g., 'high-contrast shadows and neon lights', 'sweeping natural landscapes').")
    poetic_metaphors: List[str] = Field(description="A list of 2-3 original, poetic metaphors inspired by the story's themes (e.g., 'a city that breathes chrome and sorrow').")

tavily_tool = TavilySearch(max_results=3)
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
parser = JsonOutputParser(pydantic_object=CreativeInspiration)

prompt_template = PromptTemplate(
    template="""
    You are a creative director and poet, skilled at distilling the essence of a story into evocative, inspirational phrases.
    Based *only* on the provided web search results about "{story_reference}", generate a list of thematic elements, visual styles, and original poetic metaphors. Capture the *feeling* and *atmosphere*, not just the plot.
    SEARCH RESULTS:
    {search_results}
    {format_instructions}
    """,
    input_variables=["story_reference", "search_results"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

inspiration_chain = prompt_template | llm | parser

STYLE_BANK_PATH = Path(__file__).parent.parent / "data" / "style_bank.json"

def load_style_bank() -> Dict:
    try:
        with open(STYLE_BANK_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def run_inspiration_agent(state: AppState) -> AppState:
    print("---AGENT: Running Inspiration Agent---")
    narrative_state = state.narrative_state
    inspiration_phrases = []

    if narrative_state.inspiration_mode == "🧠 AI Imagination" and narrative_state.genre != "Filmmaker's Choice":
        print("   - Using local StyleBank for inspiration.")
        style_bank = load_style_bank()
        phrases = style_bank.get(narrative_state.genre, {}).get(narrative_state.mood, {}).get("default", [])
        if phrases:
            inspiration_phrases.extend(phrases)

    elif narrative_state.inspiration_mode == "🎞️ Inspired By" and narrative_state.story_reference:
        print(f"   - Querying for inspiration from '{narrative_state.story_reference}' using Tavily + GPT-4o...")
        try:
            results = tavily_tool.invoke(f"Thematic elements, visual style, and atmosphere of the story {narrative_state.story_reference}")
            # CORRECTED: The new TavilySearch returns a list of strings directly.
            search_context = "\n".join([f"- {r}" for r in results])
            
            response: Dict = inspiration_chain.invoke({
                "story_reference": narrative_state.story_reference,
                "search_results": search_context
            })
            for theme in response.get("thematic_elements", []): inspiration_phrases.append(f"Thematic Element: {theme}")
            for style in response.get("visual_style_notes", []): inspiration_phrases.append(f"Visual Style: {style}")
            for metaphor in response.get("poetic_metaphors", []): inspiration_phrases.append(f"Poetic Metaphor: {metaphor}")
        except Exception as e:
            print(f"   - ERROR in Inspiration Agent: {e}")
            inspiration_phrases.append(f"Could not get creative inspiration for '{narrative_state.story_reference}'.")
    
    if inspiration_phrases:
        if narrative_state.inspiration_phrases:
            narrative_state.inspiration_phrases.extend(inspiration_phrases)
        else:
            narrative_state.inspiration_phrases = inspiration_phrases
            
    state.narrative_state = narrative_state
    return state