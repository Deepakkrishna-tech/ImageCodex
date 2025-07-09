# src/app.py
# Final Refined Version - No logo, dev sidebar enabled.

import streamlit as st
from dotenv import load_dotenv

# --- RELATIVE IMPORTS ---
from .core.schemas import AppState, VideoCreativeBrief
from .graph.graphs import build_visual_workflow_graph, build_narrative_workflow_graph
from .ui.visual_prompting_ui import render_stage1_ui, render_stage2_ui
from .ui.stage3_ui import render_narrative_engine

# --- INITIAL SETUP ---
load_dotenv()
st.set_page_config(page_title="ImageCodeX", layout="wide", initial_sidebar_state="auto")


# [The AppController class remains exactly the same]
class AppController:
    """A dedicated controller to manage the application's state and logic."""
    def __init__(self):
        if 'app_state' not in st.session_state:
            st.session_state['app_state'] = AppState().model_dump()
        self.state: AppState = AppState.model_validate(st.session_state['app_state'])

    def _update_and_persist_state(self, new_state: AppState):
        self.state = new_state
        st.session_state['app_state'] = self.state.model_dump()

    def _run_graph(self, graph_builder_func, input_state_dict: dict, workflow_name: str):
        with st.spinner(f"The AI team is working... ({workflow_name})"):
            try:
                graph = graph_builder_func()
                final_state_dict = graph.invoke(input_state_dict)
                final_state = AppState.model_validate(final_state_dict)
                self._update_and_persist_state(final_state)
            except Exception as e:
                st.error(f"An error occurred in the {workflow_name}.")
                st.exception(e)

    def run_visual_workflow(self, image_bytes: bytes = None, video_brief: VideoCreativeBrief = None, feedback: str = None, refinement_target: str = None):
        state_dict = self.state.model_dump()
        if image_bytes: state_dict['original_image_bytes'] = image_bytes
        if video_brief:
            state_dict.update({
                'visual_analysis': None, 'image_prompt': None, 'prompt_critique': None,
                'video_creative_brief': video_brief.model_dump()
            })
        if feedback and refinement_target:
            state_dict['user_feedback'] = feedback
            state_dict['active_prompt_for_refinement'] = refinement_target
        self._run_graph(build_visual_workflow_graph, state_dict, "Visual Workflow")

   # In src/app.py, inside the AppController class

    def run_narrative_workflow(self, image_bytes: bytes = None, text_idea: str = None, genre: str = None, mood: str = None):
        """Handles all logic for Stage 3, now including genre and mood."""
        state_dict = self.state.model_dump()
        
        # We reset the narrative state to ensure a clean run each time
        narrative_input = {}
        
        if image_bytes: narrative_input['input_image_bytes'] = image_bytes
        if text_idea: narrative_input['initial_idea'] = text_idea
        if genre: narrative_input['genre'] = genre
        if mood: narrative_input['mood'] = mood
        
        # Overwrite the old narrative state with the new inputs
        state_dict['narrative_state'] = narrative_input
        self._run_graph(build_narrative_workflow_graph, state_dict, "Narrative Workflow")


def main():
    """The main entry point called by run_app.py."""
    controller = AppController()

    # --- DEV SIDEBAR (KEPT FOR DEBUGGING) ---
    # This is your most important tool. Do not remove it during development.
    with st.sidebar:
        st.header("Dev: App State")
        if st.button("Clear All State"):
            st.session_state.clear()
            st.rerun()
        st.json(st.session_state.get('app_state', {}), expanded=False)
    
    # --- HEADER (LOGO CODE REMOVED) ---
    st.title("ImageCodeX")
    st.markdown("#### Your AI partner for turning static images into cinematic stories.")
    st.divider()

    # --- MAIN NAVIGATION ---
    stages = ["Stage 1: Image Prompt", "Stage 2: Video Prompt", "Stage 3: Narrative Engine"]
    active_stage = st.radio(
        "Select a Stage:", stages, horizontal=True, label_visibility="collapsed"
    )

    # --- RENDER ACTIVE STAGE ---
    if active_stage == "Stage 1: Image Prompt":
        render_stage1_ui(controller)
    elif active_stage == "Stage 2: Video Prompt":
        render_stage2_ui(controller)
    elif active_stage == "Stage 3: Narrative Engine":
        render_narrative_engine(controller)

if __name__ == "__main__":
    main()