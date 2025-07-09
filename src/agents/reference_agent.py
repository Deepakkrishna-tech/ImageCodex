# src/agents/reference_agent.py
"""
The Reference Agent ensures factual integrity for narratives.
FINAL CORRECTED VERSION: Fixes the bug caused by the new TavilySearch output format.
"""
from typing import List, Dict
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from src.core.schemas import AppState

class StoryMotifs(BaseModel):
    key_characters: List[str] = Field(description="List of the most important characters.")
    central_themes: List[str] = Field(description="List of the central themes or moral lessons.")
    key_plot_points: List[str] = Field(description="A short list of 3-4 key plot points or events.")
    symbolic_objects_or_places: List[str] = Field(description="List of symbolic items or locations.")

tavily_tool = TavilySearch(max_results=4)
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
parser = JsonOutputParser(pydantic_object=StoryMotifs)

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

reference_chain = prompt_template | llm | parser

def run_reference_agent(state: AppState) -> AppState:
    print("---AGENT: Running Reference Agent (Live)---")
    narrative_state = state.narrative_state
    reference = narrative_state.story_reference
    
    if not reference:
        return state

    print(f"   - Searching for motifs from '{reference}' using Tavily...")
    
    try:
        results = tavily_tool.invoke(f"Key story motifs, characters, and themes in {reference}")
        # CORRECTED: The new TavilySearch returns a list of strings directly.
        # We no longer access a 'content' key.
        search_context = "\n".join([f"- {r}" for r in results])
        print("   - Search complete. Analyzing results with GPT-4o...")

        response: Dict = reference_chain.invoke({
            "story_reference": reference,
            "search_results": search_context
        })

        inspiration_phrases = []
        for char in response.get("key_characters", []): inspiration_phrases.append(f"Character: {char}")
        for theme in response.get("central_themes", []): inspiration_phrases.append(f"Theme: {theme}")
        for plot in response.get("key_plot_points", []): inspiration_phrases.append(f"Plot Point: {plot}")
        for item in response.get("symbolic_objects_or_places", []): inspiration_phrases.append(f"Symbol: {item}")

        print(f"   - Found Motifs: {inspiration_phrases}")
        narrative_state.inspiration_phrases = inspiration_phrases

    except Exception as e:
        print(f"   - ERROR in Reference Agent: {e}")
        narrative_state.inspiration_phrases = [f"Could not retrieve details for '{reference}'."]

    state.narrative_state = narrative_state
    return state