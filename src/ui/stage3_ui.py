# src/ui/stage3_ui.py
# FINAL VERIFIED VERSION - Added image preview to the input form.

import streamlit as st

def render_narrative_engine(controller):
    """Renders the UI for Stage 3, now with an image preview."""
    st.header("🎬 Stage 3: Narrative Generation Engine")
    st.markdown("Go from a single image or idea to a complete cinematic story, script, and storyboard.")

    narrative_state = controller.state.narrative_state

    # --- INPUT FORM ---
    with st.form("narrative_form"):
        st.subheader("Creative Brief")
        
        input_image = st.file_uploader("Upload an image to inspire the story", type=["png", "jpg", "jpeg"], key="stage3_uploader")
        
        # --- THIS IS THE FEATURE ADDITION ---
        # If an image has been uploaded, display it immediately.
        if input_image:
            st.image(input_image, caption="Image Preview", width=300)

        initial_idea = st.text_area("Or, start with a text idea or theme", placeholder="e.g., A lone astronaut discovers a mysterious alien garden on a desolate moon.")
        
        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox("Select a Genre", ["Filmmaker's Choice", "Cyberpunk Noir", "Solarpunk", "Cosmic Horror", "Fantasy Epic", "Modern Thriller"], key="genre_select")
        with col2:
            mood = st.selectbox("Select a Mood", ["Filmmaker's Choice", "Tense & Gritty", "Hopeful & Awe-inspiring", "Mysterious & Unsettling", "Action-packed"], key="mood_select")

        submitted = st.form_submit_button("🚀 Generate Full Narrative", type="primary")

        if submitted:
            if not initial_idea and not input_image:
                st.warning("Please provide either a text idea or an image to begin.")
            else:
                image_data = input_image.getvalue() if input_image else None
                controller.run_narrative_workflow(
                    image_bytes=image_data, 
                    text_idea=initial_idea,
                    genre=genre,
                    mood=mood
                )
                st.rerun()

    # --- OUTPUT DISPLAY AREA (no changes here) ---
    if narrative_state and narrative_state.story_arc:
        st.subheader("📜 Story Arc")
        st.success(f"**Title:** {narrative_state.story_arc.title}")
        st.info(f"**Logline:** {narrative_state.story_arc.logline}")
        with st.expander("Show Full Story Arc Details"):
            for scene in narrative_state.story_arc.scenes:
                st.markdown("---")
                st.markdown(f"**Scene {scene.scene_number}: {scene.title}** ({scene.setting})")
                st.markdown(f"**Summary:** {scene.summary}")
                st.markdown(f"**Key Visual Moment:** *{scene.key_visual_moment}*")
    
    if narrative_state and narrative_state.screenplay:
        st.subheader("✍️ Screenplay")
        with st.expander("Show Full Screenplay"):
            for scene in narrative_state.screenplay.scenes:
                st.markdown("---")
                st.markdown(f"**{scene.scene_header}**")
                st.write(scene.action_description.replace('\n', '  \n'))
                if scene.character_dialogue:
                    for char, lines in scene.character_dialogue.items():
                        st.markdown(f"<div style='margin-left: 15%;'><strong>{char.upper()}</strong></div>", unsafe_allow_html=True)
                        for line in lines:
                            st.markdown(f"<div style='margin-left: 25%;'>{line}</div>", unsafe_allow_html=True)
    
    if narrative_state and narrative_state.storyboard:
        st.subheader("🖼️ Visual Storyboard")
        st.markdown("Your AI Cinematographer has broken down the script into key shots.")
        
        for item in narrative_state.storyboard.items:
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"##### Scene {item.scene_number}, Shot {item.shot_number}")
                    st.markdown(f"**Type:** {item.shot_type}")
                    st.markdown("**Description:**")
                    st.write(item.shot_description)
                with col2:
                    st.markdown("**Cinematic Generation Prompt**")
                    st.code(item.cinematic_prompt)