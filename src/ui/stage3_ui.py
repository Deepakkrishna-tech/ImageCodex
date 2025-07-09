# src/ui/stage3_ui.py
"""
This file renders the UI for the Stage 3 Cinematic Narrative Engine,
based on the 2025 Product Development Document.
"""
import streamlit as st
from src.core.schemas import NarrativeState

def show_stage3_ui(controller):
    """
    Renders the UI for Stage 3, the Cinematic Narrative Engine.
    Features include "Before/After" scene generation, inspiration controls,
    and a state-locking mechanism for UX consistency.
    """
    st.header("🎬 Stage 3: Cinematic Narrative Engine")
    st.markdown("Transform an image and a simple idea into a cinematic 'Before & After' scene.")

    # Get the specific state for this stage for easier access
    narrative_state: NarrativeState = controller.state.narrative_state
    is_locked = narrative_state.is_locked

    # --- INPUT FORM ---
    with st.form("cinematic_narrative_form"):
        st.subheader("Creative Brief")

        input_image = st.file_uploader(
            "Upload an image to ground the story",
            type=["png", "jpg", "jpeg"],
            key="stage3_uploader",
            disabled=is_locked,
            help="This image provides the visual anchor for the 'moment' between the Before and After scenes."
        )

        initial_idea = st.text_area(
            "Describe the core scene or moment",
            placeholder="e.g., 'A battle was lost.' or 'A secret is discovered.'",
            disabled=is_locked,
            help="A short, evocative phrase that sets the tone."
        )

        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox(
                "Select a Genre",
                ["Filmmaker's Choice", "Dark Fantasy", "Cyberpunk Noir", "Solarpunk", "Cosmic Horror", "Modern Thriller"],
                key="genre_select",
                disabled=is_locked
            )
        with col2:
            mood = st.selectbox(
                "Select a Mood",
                ["Filmmaker's Choice", "Tense & Gritty", "Hopeful & Awe-inspiring", "Mysterious & Unsettling", "Action-packed", "Somber & Reflective"],
                key="mood_select",
                disabled=is_locked
            )

        st.divider()
        st.subheader("Inspiration Source")

        inspiration_mode = st.radio(
            "Choose your creative engine:",
            options=["🧠 AI Imagination", "🎞️ Inspired By", "📚 Original Story"],
            horizontal=True,
            key="inspiration_mode",
            disabled=is_locked,
            help="Control how the story is generated. 'Original Story' will be more faithful to the source."
        )

        story_reference = None
        if inspiration_mode != "🧠 AI Imagination":
            story_reference = st.text_input(
                "Reference Story (e.g., 'Spiderman', 'Narnia', 'Mahabharata')",
                disabled=is_locked,
                help="Provide a well-known story for thematic or narrative inspiration."
            )

        submitted = st.form_submit_button("🎬 Generate Cinematic Scene", type="primary", disabled=is_locked)

        if submitted:
            if not initial_idea and not input_image:
                st.warning("Please provide either a text idea or an image to begin.")
            else:
                image_data = input_image.getvalue() if input_image else None
                # This will be passed to a new, updated controller method
                controller.run_cinematic_narrative_workflow(
                    image_bytes=image_data,
                    text_idea=initial_idea,
                    genre=genre,
                    mood=mood,
                    inspiration_mode=inspiration_mode,
                    story_reference=story_reference
                )

    # --- RESET BUTTON (appears outside the form) ---
    if is_locked:
        if st.button("🔄 Start New Scene"):
            # A new controller method will reset just this stage's state
            controller.reset_narrative_state()
            st.rerun()

    # --- OUTPUT DISPLAY AREA ---
    if narrative_state.cinematic_output:
        st.divider()
        st.subheader("Generated Cinematic Scene")

        source_info = narrative_state.cinematic_output.source_of_inspiration
        st.info(f"**Source:** {source_info} 🔒", icon="📚")

        col_before, col_after = st.columns(2)

        with col_before:
            with st.container(border=True):
                st.markdown("#### ✨ Before Scene")
                st.write(narrative_state.cinematic_output.before_scene_cinematic)
                with st.expander("🧠 View Image Prompt"):
                    st.code(narrative_state.cinematic_output.before_scene_prompt, language="text")

        with col_after:
            with st.container(border=True):
                st.markdown("#### 🔮 After Scene")
                st.write(narrative_state.cinematic_output.after_scene_cinematic)
                with st.expander("🎞️ View Image Prompt"):
                    st.code(narrative_state.cinematic_output.after_scene_prompt, language="text")