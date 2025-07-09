# src/agents/inspiration_agent.py
"""
The Inspiration Agent enriches narrative prompts with poetic metaphors,
stylistic tone, and motifs from reference stories using both local files and live AI.
"""
import json
from pathlib import Path
from typing import List, Dict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# --- Import AppState for type-safe access to the state ---
from src.core.schemas import AppState

# ==============================================================================
# == 1. DEFINE THE STRUCTURE FOR THE LLM'S OUTPUT
# ==============================================================================
class CreativeInspiration(BaseModel):
    """Pydantic model to structure the creative inspiration extracted from a story."""
    thematic_elements: List[str] = Field(description="A list of 2-3 core thematic elements or feelings (e.g., 'a sense of inevitable loss', 'the triumph of community').")
    visual_style_notes: List[str] = Field(description="A list of 2-3 visual style notes or motifs (e.g., 'high-contrast shadows and neon lights', 'sweeping natural landscapes').")
    poetic_metaphors: List[str] = Field(description="A list of 2-3 original, poetic metaphors inspired by the story's themes (e.g., 'a city that breathes chrome and sorrow').")

# ==============================================================================
# == 2. INITIALIZE TOOLS AND MODELS
# ==============================================================================
# This agent will use the Tavily Search tool.
tavily_tool = TavilySearchResults(max_results=3)

# We will use GPT-4o for its strong creative capabilities.
llm = ChatOpenAI(model="gpt-4o", temperature=0.7) # Higher temp for more creativity

# Create an output parser for the structured creative output.
parser = JsonOutputParser(pydantic_object=CreativeInspiration)

# ==============================================================================
# == 3. CREATE THE PROMPT TEMPLATE
# ==============================================================================
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

# ==============================================================================
# == 4. BUILD THE AGENTIC CHAIN
# ==============================================================================
inspiration_chain = prompt_template | llm | parser

# ==============================================================================
# == 5. SETUP LOCAL STYLE BANK (for AI Imagination mode)
# ==============================================================================
STYLE_BANK_PATH = Path(__file__).parent.parent / "data" / "style_bank.json"

def load_style_bank() -> Dict:
    """Loads the genre-mood-symbol style bank from the JSON file."""
    try:
        with open(STYLE_BANK_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# ==============================================================================
# == 6. CREATE THE NODE FUNCTION FOR THE GRAPH
# ==============================================================================
def run_inspiration_agent(state: AppState) -> AppState:
    """
    This node function enriches the narrative state with creative phrases
    based on the selected inspiration mode.
    """
    print("---AGENT: Running Inspiration Agent---")
    narrative_state = state.narrative_state
    
    genre = narrative_state.genre
    mood = narrative_state.mood
    mode = narrative_state.inspiration_mode
    reference = narrative_state.story_reference
    
    inspiration_phrases = []

    # --- Mode 1: Local StyleBank (Fast, Offline) ---
    if mode == "🧠 AI Imagination" and genre != "Filmmaker's Choice":
        print("   - Using local StyleBank for inspiration.")
        style_bank = load_style_bank()
        phrases = style_bank.get(genre, {}).get(mood, {}).get("default", [])
        if phrases:
            inspiration_phrases.extend(phrases)
            print(f"   - Found {len(phrases)} phrases in StyleBank for {genre}/{mood}")

    # --- Mode 2: Inspired By (Live Web-Augmented AI) ---
    elif mode == "🎞️ Inspired By" and reference:
        print(f"   - Querying for inspiration from '{reference}' using Tavily + GPT-4o...")
        try:
            # Step A: Run Tavily search for creative inspiration
            results = tavily_tool.invoke(f"Thematic elements, visual style, and atmosphere of the story {reference}")
            search_context = "\n".join([f"- {r['content']}" for r in results])
            
            # Step B: Run the LLM chain to generate creative ideas
            response: Dict = inspiration_chain.invoke({
                "story_reference": reference,
                "search_results": search_context
            })

            # Step C: Format the structured output into a list of strings
            for theme in response.get("thematic_elements", []):
                inspiration_phrases.append(f"Thematic Element: {theme}")
            for style in response.get("visual_style_notes", []):
                inspiration_phrases.append(f"Visual Style: {style}")
            for metaphor in response.get("poetic_metaphors", []):
                inspiration_phrases.append(f"Poetic Metaphor: {metaphor}")

            print(f"   - Generated creative phrases: {inspiration_phrases}")

        except Exception as e:
            print(f"   - ERROR in Inspiration Agent: {e}")
            inspiration_phrases.append(f"Could not get creative inspiration for '{reference}'.")
    
    else:
        print("   - No specific inspiration path triggered for this agent.")

    # Update the state with the findings
    # If phrases were found, append them to any existing ones (e.g., from another agent)
    if inspiration_phrases:
        if narrative_state.inspiration_phrases:
            narrative_state.inspiration_phrases.extend(inspiration_phrases)
        else:
            narrative_state.inspiration_phrases = inspiration_phrases
            
    state.narrative_state = narrative_state
    return state