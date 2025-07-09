# src/graph/graphs.py
# FINAL, VERIFIED VERSION - This file contains the complete and correct agentic workflow.

from langgraph.graph import StateGraph, END
from typing import Literal, Dict, Any

# --- Import Core Schema ---
from src.core.schemas import AppState 

# --- Import All Agent Nodes ---
# Original agents needed for legacy workflows
from src.agents.visual_analyst import run_visual_analyst
from src.agents.prompt_engineer import run_prompt_engineer
from src.agents.inspector import run_inspector
from src.agents.refiner import run_refiner
from src.agents.video_director import run_video_director
from src.agents.image_generator import generate_image_node
from src.agents.film_story_writer import story_concept_generator_node # Kept for compatibility

# NEW: Imports for the Stage 3 Cinematic agents
from src.agents.context_engineer import run_context_engineer
from src.agents.inspiration_agent import run_inspiration_agent
from src.agents.reference_agent import run_reference_agent
from src.agents.storytelling_agent import run_cinematic_prompt_engineer

# ==============================================================================
# == VISUAL PROMPTING WORKFLOW (STAGES 1 & 2) - UNCHANGED
# ==============================================================================
def visual_entry_point_router(state: Dict[str, Any]) -> Literal["visual_analyst", "video_director"]:
    if state.get("video_creative_brief"): return "video_director"
    return "visual_analyst"

def visual_workflow_router(state: Dict[str, Any]) -> Literal["refine", "end"]:
    if state.get("user_feedback"): return "refine"
    return "end"

def build_visual_workflow_graph():
    workflow = StateGraph(Dict[str, Any])
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
    return workflow.compile()

# ==============================================================================
# == V3 CINEMATIC NARRATIVE WORKFLOW (STAGE 3) - NEW
# ==============================================================================
def inspiration_router(state: AppState) -> Literal["reference_agent", "inspiration_agent", "context_engineer"]:
    mode = state.narrative_state.inspiration_mode
    if mode == "📚 Original Story": return "reference_agent"
    if mode == "🎞️ Inspired By": return "inspiration_agent"
    return "context_engineer"

def build_cinematic_narrative_graph():
    workflow = StateGraph(AppState)
    workflow.add_node("reference_agent", run_reference_agent)
    workflow.add_node("inspiration_agent", run_inspiration_agent)
    workflow.add_node("context_engineer", run_context_engineer)
    workflow.add_node("cinematic_prompt_engineer", run_cinematic_prompt_engineer)
    workflow.set_conditional_entry_point(
        inspiration_router,
        {
            "reference_agent": "reference_agent",
            "inspiration_agent": "inspiration_agent",
            "context_engineer": "context_engineer"
        }
    )
    workflow.add_edge("reference_agent", "context_engineer")
    workflow.add_edge("inspiration_agent", "context_engineer")
    
    # --- THIS IS THE CRITICAL LINE OF CODE ---
    workflow.add_edge("context_engineer", "cinematic_prompt_engineer")
    
    workflow.add_edge("cinematic_prompt_engineer", END)
    graph = workflow.compile()
    print("V3 Cinematic Narrative Workflow graph compiled successfully.")
    return graph

# ==============================================================================
# == IMAGE GENERATION WORKFLOW (STAGE 4) - UNCHANGED
# ==============================================================================
def build_image_generation_graph():
    workflow = StateGraph(AppState)
    workflow.add_node("image_generator", generate_image_node)
    workflow.set_entry_point("image_generator")
    workflow.add_edge("image_generator", END)
    return workflow.compile()