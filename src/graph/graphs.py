# src/graph/graphs.py
# Final, verified graph factory for ImageCodeX. This version restores the
# conditional entry point for the visual workflow, fixing the Stage 2 bug.

from langgraph.graph import StateGraph, END
from typing import Literal, Dict, Any

# --- Import All Agent Nodes ---
from src.agents.visual_analyst import run_visual_analyst
from src.agents.prompt_engineer import run_prompt_engineer
from src.agents.inspector import run_inspector
from src.agents.refiner import run_refiner
from src.agents.video_director import run_video_director
from src.agents.film_story_writer import film_story_writer_node
from src.agents.script_expert import script_expert_node
from src.agents.storyboard_artist import storyboard_artist_node

# ==============================================================================
# == VISUAL PROMPTING WORKFLOW (STAGES 1 & 2)
# ==============================================================================

def visual_entry_point_router(state: Dict[str, Any]) -> Literal["visual_analyst", "video_director"]:
    """Determines the starting point of the graph based on user intent."""
    print("---VISUAL_GRAPH: Routing Entry Point---")
    # If video_creative_brief is present, the user is trying to start or run Stage 2.
    if state.get("video_creative_brief"):
        print("Entry: Path for Stage 2 (Video Prompt)")
        return "video_director"
    else:
        # Otherwise, the user is starting a Stage 1 run.
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
    workflow = StateGraph(Dict[str, Any])

    workflow.add_node("visual_analyst", run_visual_analyst)
    workflow.add_node("prompt_engineer", run_prompt_engineer)
    workflow.add_node("inspector", run_inspector)
    workflow.add_node("refiner", run_refiner)
    workflow.add_node("video_director", run_video_director)

    # --- THIS IS THE FIX: Restore conditional entry ---
    workflow.set_conditional_entry_point(
        visual_entry_point_router,
        {
            "visual_analyst": "visual_analyst",
            "video_director": "video_director"
        }
    )
    
    workflow.add_edge("visual_analyst", "prompt_engineer")
    workflow.add_edge("prompt_engineer", "inspector")

    # The refiner loops back to the inspector for a quality re-check.
    workflow.add_edge("refiner", "inspector")

    # After inspection or video direction, the only options are to refine or end.
    workflow.add_conditional_edges("inspector", visual_workflow_router, {"refine": "refiner", "end": END})
    workflow.add_conditional_edges("video_director", visual_workflow_router, {"refine": "refiner", "end": END})

    graph = workflow.compile()
    print("Visual Prompting Workflow Graph compiled successfully.")
    return graph


# ==============================================================================
# == NARRATIVE ENGINE WORKFLOW (STAGE 3)
# ==============================================================================

def build_narrative_workflow_graph():
    """Builds the linear LangGraph for the Stage 3 Narrative Engine."""
    workflow = StateGraph(Dict[str, Any])
    workflow.add_node("film_story_writer", film_story_writer_node)
    workflow.add_node("script_expert", script_expert_node)
    workflow.add_node("storyboard_artist", storyboard_artist_node)
    workflow.set_entry_point("film_story_writer")
    workflow.add_edge("film_story_writer", "script_expert")
    workflow.add_edge("script_expert", "storyboard_artist")
    workflow.add_edge("storyboard_artist", END)
    graph = workflow.compile()
    print("Narrative Engine Workflow Graph compiled successfully.")
    return graph