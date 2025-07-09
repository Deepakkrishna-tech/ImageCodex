# src/app.py
# Final version with robust state management in the AppController.

import streamlit as st

# --- RELATIVE IMPORTS ---
from src.core.schemas import AppState, VideoCreativeBrief
from src.graph import build_visual_workflow_graph, build_narrative_workflow_graph, build_image_generation_graph
from src.ui import show_visual_prompting_ui, show_stage3_ui, show_stage4_ui

class AppController:
    """A dedicated controller to manage the application's state and logic."""
    def __init__(self):
        """
        Initializes the controller. Enforces a clear separation between the
        Pydantic model state (self.state) and the dictionary state stored
        in Streamlit's session (st.session_state).
        """
        if 'app_state' not in st.session_state:
            # First run: create a new AppState and store its DICT version.
            st.session_state['app_state'] = AppState().model_dump()
        
        # Every run: load the DICT from session and validate it into a
        # Pydantic model. This GUARANTEES self.state is always a Pydantic object.
        self.state: AppState = AppState.model_validate(st.session_state['app_state'])

    def _update_and_persist_state(self, new_state: AppState):
        """
        Updates the internal Pydantic state and persists the DICT version
        to Streamlit's session_state.
        """
        self.state = new_state
        st.session_state['app_state'] = self.state.model_dump()

    def _run_and_update(self, graph_builder, input_payload, workflow_name):
        """A standardized method to run any graph and handle state updates."""
        with st.spinner(f"The AI team is working on '{workflow_name}'..."):
            try:
                graph = graph_builder()
                # LangGraph might return a dict or a pydantic model.
                # model_validate handles both cases gracefully.
                final_state_data = graph.invoke(input_payload)
                validated_state = AppState.model_validate(final_state_data)
                self._update_and_persist_state(validated_state)
            except Exception as e:
                st.error(f"An error occurred in the {workflow_name}.")
                st.exception(e)
        st.rerun()

    def run_visual_workflow(self, image_bytes: bytes = None, video_brief: VideoCreativeBrief = None, feedback: str = None, refinement_target: str = None):
        """Prepares state and runs the visual prompting workflow (Stages 1 & 2)."""
        state_dict = self.state.model_dump()
        if image_bytes: state_dict['original_image_bytes'] = image_bytes
        if video_brief:
            state_dict.update({'video_creative_brief': video_brief.model_dump()})
        if feedback and refinement_target:
            state_dict['user_feedback'] = feedback
            state_dict['active_prompt_for_refinement'] = refinement_target
        
        self._run_and_update(build_visual_workflow_graph, state_dict, "Visual Workflow")

    def run_narrative_workflow(self, image_bytes: bytes = None, text_idea: str = None, genre: str = None, mood: str = None):
        """Prepares state and runs the narrative workflow (Stage 3)."""
        state_dict = self.state.model_dump()
        state_dict['narrative_state'].update({
            'input_image_bytes': image_bytes,
            'initial_idea': text_idea,
            'genre': genre,
            'mood': mood
        })
        self._run_and_update(build_narrative_workflow_graph, state_dict, "Narrative Workflow")

    def run_image_generation_workflow(self):
        """Runs the image generation workflow (Stage 4)."""
        # This graph expects the Pydantic model state directly.
        self._run_and_update(build_image_generation_graph, self.state, "Image Generation")


def main():
    """The main entry point for the Streamlit app."""
    controller = AppController()

    with st.sidebar:
        st.header("Dev: App State")
        if st.button("Clear All State"):
            st.session_state.clear()
            st.rerun()
        # This will now work because controller.state is always a Pydantic model.
        st.json(controller.state.model_dump(), expanded=False)
    
    st.title("ImageCodeX")
    st.markdown("#### Your AI partner for turning static images into cinematic stories.")
    st.divider()

    stages = ["Visual Prompting", "Narrative Engine", "Image Generation"]
    tab1, tab2, tab3 = st.tabs(stages)

    with tab1:
        show_visual_prompting_ui(controller) 
    with tab2:
        show_stage3_ui(controller)
    with tab3:
        # Pass the Pydantic state object directly to the UI function.
        show_stage4_ui(controller.state, controller)

if __name__ == "__main__":
    main()