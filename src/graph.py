 # src/graph.py

# --- 1. IMPORTS ---
# Group all imports at the top for clarity.
import os
import base64
from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Import our custom prompts from the prompts.py file in the same directory.
from src import prompts


# --- 2. GRAPH STATE DEFINITION ---
# This is the single source of truth for the data structure of our workflow.
class GraphState(TypedDict):
    """
    Represents the state of our agentic workflow.
    """
    image_data: str
    target_style: str
    initial_analysis: dict
    initial_prompt: str
    refinement_instruction: str  # This will be populated by the UI
    refined_prompt: str
    prompt_history: List[str]


# --- 3. LLM AND PARSERS SETUP ---
# Initialize the model and parsers once to be reused by all nodes.
model = ChatOpenAI(temperature=0, model="gpt-4o", max_retries=3)
string_parser = StrOutputParser()
json_parser = JsonOutputParser()


# --- 4. AGENT NODE FUNCTIONS ---
# Each function represents a "worker" in our agentic system.
# It takes the state, performs an action, and returns a dictionary
# with the fields to update in the state.

def visual_analyst_node(state: GraphState) -> dict:
    """Analyzes the image and extracts a structured JSON breakdown."""
    print("--- 🧠 EXECUTING VISUAL ANALYST NODE ---")
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompts.VISUAL_ANALYST_PROMPT},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{state['image_data']}"},
            },
        ]
    )
    chain = model | json_parser
    analysis = chain.invoke([message])
    print("--- ✅ VISUAL ANALYSIS COMPLETE ---")
    return {"initial_analysis": analysis}


def prompt_engineer_node(state: GraphState) -> dict:
    """Generates a high-quality prompt from the analysis and style."""
    print("--- 🎨 EXECUTING PROMPT ENGINEER NODE ---")
    
    analysis_json = state['initial_analysis']
    
    # This is the fix: We are creating a dictionary with the exact
    # keys our new prompt template expects. We are "flattening" the nested data.
    prompt_data = {
        "analysis": analysis_json, # The full JSON for the main body
        "target_style": state['target_style'],
        # We add this specifically for the --ar flag
        "aspect_ratio": analysis_json.get("technical_specs", {}).get("aspect_ratio", "16:9")
    }

    # Now we use the .format(**prompt_data) method. The ** operator
    # "unpacks" the dictionary, so .format() receives analysis=...,
    # target_style=..., and aspect_ratio=... as arguments.
    prompt_template = prompts.PROMPT_ENGINEER_PROMPT.format(**prompt_data)
    
    message = HumanMessage(content=prompt_template)
    chain = model | string_parser
    generated_prompt = chain.invoke([message])
    print("--- ✅ PROMPT GENERATION COMPLETE ---")
    
    current_history = state.get("prompt_history", [])
    new_history = current_history + [generated_prompt]
    
    return {
        "initial_prompt": generated_prompt,
        "prompt_history": new_history
    }


def refinement_node(state: GraphState) -> dict:
    """Refines an existing prompt based on user feedback."""
    print("--- 🔄 EXECUTING REFINEMENT NODE ---")
    last_prompt = state["prompt_history"][-1]
    refinement_instruction = state["refinement_instruction"]
    
    prompt_template = prompts.REFINEMENT_PROMPT.format(
        current_prompt=last_prompt,
        refinement_instruction=refinement_instruction
    )
    message = HumanMessage(content=prompt_template)
    chain = model | string_parser
    refined_prompt = chain.invoke([message])
    print("--- ✅ PROMPT REFINEMENT COMPLETE ---")

    new_history = state["prompt_history"] + [refined_prompt]
    
    return {
        "refined_prompt": refined_prompt,
        "prompt_history": new_history
    }


# --- 5. GRAPH ASSEMBLY ---
# We define the workflow structure and compile it into a runnable app.
def build_graph():
    """Builds the LangGraph state machine."""
    workflow = StateGraph(GraphState)

    # Add nodes: map a string name to a function
    workflow.add_node("visual_analyst", visual_analyst_node)
    workflow.add_node("prompt_engineer", prompt_engineer_node)
    workflow.add_node("refiner", refinement_node)

    # Define edges: the flow of control
    workflow.set_entry_point("visual_analyst")
    workflow.add_edge("visual_analyst", "prompt_engineer")
    workflow.add_edge("prompt_engineer", END)

    # Compile the graph into a runnable object
    app = workflow.compile()
    return app

# Create a single, compiled instance of the graph for our app to use.
graph_app = build_graph()