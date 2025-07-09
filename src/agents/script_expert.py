# src/agents/script_expert.py
# DIAGNOSTIC VERSION - This will force the hidden error to be printed.

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import Screenplay, StoryArc
from ..core.prompts import SCRIPT_EXPERT_PROMPT

def script_expert_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Takes a StoryArc and writes a full Screenplay."""
    print("---AGENT: SCRIPT EXPERT---")
    
    narrative_state = state.get("narrative_state", {})
    story_arc: StoryArc = narrative_state.get("story_arc")
    if not story_arc:
        print("---AGENT: SKIPPING SCRIPT EXPERT - NO STORY ARC---")
        return state

    # --- THIS IS THE DIAGNOSTIC PROBE ---
    # We will wrap the most likely point of failure in a try...except block.
    # This will catch the silent error and print it for us to see.
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.5, model_kwargs={"response_format": {"type": "json_object"}})
        structured_llm = llm.with_structured_output(Screenplay)
        prompt_template = ChatPromptTemplate.from_template(SCRIPT_EXPERT_PROMPT)
        chain = prompt_template | structured_llm

        story_arc_json_string = json.dumps(story_arc.model_dump(), indent=2)
        
        # This is the line that is likely failing.
        response = chain.invoke({"story_arc": story_arc_json_string})
        
        print("---AGENT: Generated Screenplay---")
        
        # If successful, update the state.
        state["narrative_state"]["screenplay"] = response
    
    except Exception as e:
        # If ANY error occurs, we will print it to the terminal.
        print("\n" + "="*50)
        print("!!!!!! AGENT `script_expert` CRASHED! HERE IS THE ERROR !!!!!!")
        print(f"ERROR_TYPE: {type(e)}")
        print(f"ERROR_DETAILS: {e}")
        print("="*50 + "\n")
        # Return the state unmodified so the app doesn't crash completely.
        return state

    return state