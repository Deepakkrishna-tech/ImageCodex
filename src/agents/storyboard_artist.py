# src/agents/storyboard_artist.py
import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import Storyboard, Screenplay
from ..core.prompts import STORYBOARD_ARTIST_PROMPT

def storyboard_artist_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---AGENT: STORYBOARD ARTIST---")
    print(f"STATE KEYS RECEIVED BY STORYBOARD_ARTIST: {list(state.keys())}")
    
    narrative_state = state.get("narrative_state", {})
    screenplay: Screenplay = narrative_state.get("screenplay")
    if not screenplay:
        print("---AGENT: SKIPPING STORYBOARD ARTIST - NO SCREENPLAY---")
        return state

    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    structured_llm = llm.with_structured_output(Storyboard)
    prompt_template = ChatPromptTemplate.from_template(STORYBOARD_ARTIST_PROMPT)
    chain = prompt_template | structured_llm
    screenplay_json_string = json.dumps(screenplay.model_dump(), indent=2)
    response = chain.invoke({"screenplay": screenplay_json_string})
    
    print("---AGENT: Generated Storyboard---")
    
    # --- THIS IS THE FIX ---
    state["narrative_state"]["storyboard"] = response
    return state