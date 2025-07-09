# src/app.py
# FINAL CORRECTED VERSION - Contains all required controller methods for the new UI.

import streamlit as st

# --- RELATIVE IMPORTS ---
# This line is now corrected to import the new cinematic graph builder
from src.core.schemas import AppState, VideoCreativeBrief, NarrativeState
from src.graph import build_visual_workflow_graph, build_cinematic_narrative_graph, build_image_generation_graph
from src.ui import show_visual_prompting_ui, show_stage3_ui, show_stage4_ui

class AppController:
    """A dedicated controller to manage the application's state and logic."""
    def __init__(self):
        if 'app_state' not in st.session_state:
            st.session_state['app_state'] = AppState().model_dump()
        self.state: AppState = AppState.model_validate(st.session_state['app_state'])

    def _update_and_persist_state(self, new_state: AppState):
        self.state = new_state
        st.session_state['app_state'] = self.state.model_dump()

    def _run_and_update(self, graph_builder, input_payload, workflow_name):
        with st.spinner(f"The AI team is working on the '{workflow_name}'..."):
            try:
                graph = graph_builder()
                final_state_data = graph.invoke(input_payload)
                validated_state = AppState.model_validate(final_state_data)
                self._update_and_persist_state(validated_state)
            except Exception as e:
                st.error(f"An error occurred during the {workflow_name}.")
                st.exception(e)
        st.rerun()

    # --- NEW METHOD to run the Stage 3 cinematic workflow ---
    def run_cinematic_narrative_workflow(self, image_bytes: bytes, text_idea: str, genre: str, mood: str, inspiration_mode: str, story_reference: str):
        """Prepares and runs the new Stage 3 cinematic narrative workflow."""
        current_state = self.state
        
        # Update the narrative state with fresh inputs from the UI
        current_state.narrative_state.input_image_bytes = image_bytes
        current_state.narrative_state.initial_idea = text_idea
        current_state.narrative_state.genre = genre
        current_state.narrative_state.mood = mood
        current_state.narrative_state.inspiration_mode = inspiration_mode
        current_state.narrative_state.story_reference = story_reference
        
        self._run_and_update(build_cinematic_narrative_graph, current_state.model_dump(), "Cinematic Narrative Workflow")

    # --- NEW METHOD to reset the UI ---
    def reset_narrative_state(self):
        """Resets only the narrative state to allow the user to start a new scene."""
        current_state = self.state
        current_state.narrative_state = NarrativeState() # Reset to a new, empty state
        self._update_and_persist_state(current_state)

    # --- LEGACY METHODS (Unchanged) ---
    def run_visual_workflow(self, image_bytes: bytes = None, video_brief: VideoCreativeBrief = None, feedback: str = None, refinement_target: str = None):
        state_dict = self.state.model_dump()
        if image_bytes: state_dict['original_image_bytes'] = image_bytes
        if video_brief: state_dict.update({'video_creative_brief': video_brief.model_dump()})
        if feedback:
            state_dict['user_feedback'] = feedback
            state_dict['active_prompt_for_refinement'] = refinement_target
        # This will call the old graph using a different graph builder
        self._run_and_update(build_visual_workflow_graph, state_dict, "Visual Workflow")

    def run_image_generation_workflow(self):
        """Runs the image generation workflow (Stage 4)."""
        self._run_and_update(build_image_generation_graph, self.state, "Image Generation")


def main():
    st.set_page_config(layout="wide")
    controller = AppController()

    with st.sidebar:
        st.header("Dev: App State")
        if st.button("Clear All State"):
            st.session_state.clear()
            st.rerun()
        st.json(controller.state.model_dump(), expanded=False)
    
    st.title("🎬 ImageCodeX")
    st.markdown("#### An AI-powered partner for turning static images into cinematic stories.")
    st.divider()

    stages = ["🖼️ Visual Prompting", "📖 Cinematic Narrative Engine", "🎨 Image Generation"]
    tab1, tab2, tab3 = st.tabs(stages)

    with tab1:
        show_visual_prompting_ui(controller)
    with tab2:
        show_stage3_ui(controller)
    with tab3:
        show_stage4_ui(controller.state, controller)

if __name__ == "__main__":
    main()