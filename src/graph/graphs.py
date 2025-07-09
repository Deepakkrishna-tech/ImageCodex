# src/graph/graphs.py

from langgraph.graph import StateGraph, END
from typing import Literal, Dict, Any

# --- Import Core Schema for Type Hinting ---
# NEW: Import AppState to use it as the state object for better type safety.
from src.core.schemas import AppState 

# --- Import All Agent Nodes ---
from src.agents.visual_analyst import run_visual_analyst
from src.agents.prompt_engineer import run_prompt_engineer
from src.agents.inspector import run_inspector
from src.agents.refiner import run_refiner
from src.agents.video_director import run_video_director
from src.agents.film_story_writer import story_concept_generator_node
from src.agents.script_expert import script_expert_node
from src.agents.storyboard_artist import storyboard_artist_node
# NEW: Import the image generation node we created in Step 1.
from src.agents.image_generator import generate_image_node

# ==============================================================================
# == VISUAL PROMPTING WORKFLOW (STAGES 1 & 2)
# ==============================================================================

# NOTE: The logic of your existing visual graph is complex and uses Dict[str, Any]
# for its state. We will leave it as is to avoid breaking existing functionality.
# New graphs will use the strongly-typed AppState.

def visual_entry_point_router(state: Dict[str, Any]) -> Literal["visual_analyst", "video_director"]:
    """Determines the starting point of the graph based on user intent."""
    print("---VISUAL_GRAPH: Routing Entry Point---")
    if state.get("video_creative_brief"):
        print("Entry: Path for Stage 2 (Video Prompt)")
        return "video_director"
    else:
        print("Entry: Path for Stage 1 (Image Prompt)")
        return "visual_analyst"

def visual_workflow_router(state: Dict[str, Any]) -> Literal["refine", "end"]:
    """The main decision-making router after a node has run."""
    print("---VISUAL_GRAPH: Decision Point---")
    if state.get("user_feedback"):
        print("Routing to: REFINE")
        return "refine"
    print("Routing to: END")
    return "end"

def build_visual_workflow_graph():
    """Builds the complete conditional LangGraph for the Visual Prompting workflow."""
    workflow = StateGraph(Dict[str, Any]) # Using Dict for legacy compatibility

    workflow.add_node("visual_analyst", run_visual_analyst)
    workflow.add_node("prompt_engineer", run_prompt_engineer)
    workflow.add_node("inspector", run_inspector)
    workflow.add_node("refiner", run_refiner)
    workflow.add_node("video_director", run_video_director)

    workflow.set_conditional_entry_point(
        visual_entry_point_router,
        {"visual_analyst": "visual_analyst", "video_director": "video_director"}
    )
    
    workflow.add_edge("visual_analyst", "prompt_engineer")
    workflow.add_edge("prompt_engineer", "inspector")
    workflow.add_edge("refiner", "inspector")
    workflow.add_conditional_edges("inspector", visual_workflow_router, {"refine": "refiner", "end": END})
    workflow.add_conditional_edges("video_director", visual_workflow_router, {"refine": "refiner", "end": END})

    graph = workflow.compile()
    print("Visual Prompting Workflow Graph compiled successfully.")
    return graph

# ==============================================================================
# == NARRATIVE ENGINE WORKFLOW (STAGE 3)
# ==============================================================================

# NOTE: Also leaving this graph as-is.
def build_narrative_workflow_graph():
    """Builds the graph for Stage 3."""
    workflow = StateGraph(Dict[str, Any]) # Using Dict for legacy compatibility
    workflow.add_node("story_concept_generator", story_concept_generator_node)
    workflow.set_entry_point("story_concept_generator")
    workflow.add_edge("story_concept_generator", END)

    graph = workflow.compile()
    print("Narrative Engine Workflow compiled successfully.")
    return graph

# ==============================================================================
# == IMAGE GENERATION WORKFLOW (STAGE 4)
# ==============================================================================

# NEW: This is the entire graph for our new Stage 4 functionality.
def build_image_generation_graph():
    """
    Builds the graph for Stage 4: Image Generation.
    This graph uses the modern, type-safe AppState schema.
    """
    # We define the graph with our AppState pydantic model.
    # This gives us autocompletion and type checking for the state.
    workflow = StateGraph(AppState)

    # Add the single node for image generation.
    workflow.add_node("image_generator", generate_image_node)
    
    # The graph starts at the image_generator node.
    workflow.set_entry_point("image_generator")
    
    # After generation, the workflow ends.
    workflow.add_edge("image_generator", END)

    # Compile the graph and it's ready to use.
    graph = workflow.compile()
    print("Image Generation Workflow Graph compiled successfully.")
    return graph