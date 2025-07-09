# src/agents/reference_agent.py
"""
The Reference Agent ensures factual integrity for narratives based on
known sources like literature or mythology using real web search tools and an LLM.
"""
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
class StoryMotifs(BaseModel):
    """Pydantic model to structure the key motifs extracted from a story."""
    key_characters: List[str] = Field(description="List of the most important characters.")
    central_themes: List[str] = Field(description="List of the central themes or moral lessons.")
    key_plot_points: List[str] = Field(description="A short list of 3-4 key plot points or events.")
    symbolic_objects_or_places: List[str] = Field(description="List of symbolic items or locations.")

# ==============================================================================
# == 2. INITIALIZE TOOLS AND MODELS
# ==============================================================================
# This agent will use the Tavily Search tool.
tavily_tool = TavilySearchResults(max_results=4)

# We will use GPT-4o for its strong reasoning capabilities.
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Create an output parser that will convert the LLM's JSON output into our Pydantic model.
parser = JsonOutputParser(pydantic_object=StoryMotifs)

# ==============================================================================
# == 3. CREATE THE PROMPT TEMPLATE
# ==============================================================================
prompt_template = PromptTemplate(
    template="""
    You are an expert in mythology and literary analysis. Your task is to extract the core narrative elements from a given story based on web search results.

    Analyze the provided search results about the story: "{story_reference}".

    Based *only* on the information in the search results, identify the key motifs. Do not invent details.

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
# This LCEL chain connects the prompt, LLM, and parser together.
reference_chain = prompt_template | llm | parser

# ==============================================================================
# == 5. CREATE THE NODE FUNCTION FOR THE GRAPH
# ==============================================================================
def run_reference_agent(state: AppState) -> AppState:
    """
    Uses a search tool (Tavily) and an LLM (GPT-4o) to get key motifs
    from a reference story and inject them into the state.
    """
    print("---AGENT: Running Reference Agent (Live)---")
    narrative_state = state.narrative_state
    reference = narrative_state.story_reference
    
    if not reference:
        print("   - No reference provided. Skipping.")
        return state

    print(f"   - Searching for motifs from '{reference}' using Tavily...")
    
    # --- Step A: Run the Tavily search ---
    try:
        results = tavily_tool.invoke(f"Key story motifs, characters, and themes in {reference}")
        # Format the results into a single string for the LLM
        search_context = "\n".join([f"- {r['content']}" for r in results])
        print("   - Search complete. Analyzing results with GPT-4o...")

        # --- Step B: Run the LLM chain ---
        response: Dict = reference_chain.invoke({
            "story_reference": reference,
            "search_results": search_context
        })

        # --- Step C: Format the structured output into a list of strings ---
        inspiration_phrases = []
        for char in response.get("key_characters", []):
            inspiration_phrases.append(f"Character: {char}")
        for theme in response.get("central_themes", []):
            inspiration_phrases.append(f"Theme: {theme}")
        for plot in response.get("key_plot_points", []):
            inspiration_phrases.append(f"Plot Point: {plot}")
        for item in response.get("symbolic_objects_or_places", []):
            inspiration_phrases.append(f"Symbol: {item}")

        print(f"   - Found Motifs: {inspiration_phrases}")

        # Update the state with the findings
        narrative_state.inspiration_phrases = inspiration_phrases

    except Exception as e:
        print(f"   - ERROR in Reference Agent: {e}")
        # Provide a fallback message in case of API errors
        narrative_state.inspiration_phrases = [
            f"Could not retrieve details for '{reference}'.",
            "Please check API keys and network connection."
        ]

    state.narrative_state = narrative_state
    return state