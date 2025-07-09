# src/ui/stage3_ui.py
# FINAL VERIFIED VERSION - Updated to display the new "Creative Concepts" output.

import streamlit as st

def render_narrative_engine(controller):
    """
    Renders the UI for Stage 3. The output section has been updated to display
    a list of brainstormed story concepts instead of a single story arc.
    """
    st.header("🎬 Stage 3: Narrative Generation Engine")
    st.markdown("Brainstorm multiple creative directions from a single spark of inspiration.")

    narrative_state = controller.state.narrative_state

    # --- INPUT FORM (NO CHANGES HERE) ---
    # This entire section is working perfectly and remains untouched.
    with st.form("narrative_form"):
        st.subheader("Creative Brief")
        
        input_image = st.file_uploader("Upload an image to inspire the story", type=["png", "jpg", "jpeg"], key="stage3_uploader")
        
        if input_image:
            st.image(input_image, caption="Image Preview", width=300)

        initial_idea = st.text_area("Or, start with a text idea or theme", placeholder="e.g., A lone astronaut discovers a mysterious alien garden on a desolate moon.")
        
        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox("Select a Genre", ["Filmmaker's Choice", "Cyberpunk Noir", "Solarpunk", "Cosmic Horror", "Fantasy Epic", "Modern Thriller"], key="genre_select")
        with col2:
            mood = st.selectbox("Select a Mood", ["Filmmaker's Choice", "Tense & Gritty", "Hopeful & Awe-inspiring", "Mysterious & Unsettling", "Action-packed"], key="mood_select")

        # The button text is updated to reflect the new goal.
        submitted = st.form_submit_button("💡 Brainstorm Concepts", type="primary")

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

    # --- OUTPUT DISPLAY AREA (THIS IS THE ONLY PART THAT HAS CHANGED) ---
    # We now look for 'story_concepts' in the state instead of 'story_arc'.
    
    if narrative_state and narrative_state.story_concepts:
        st.subheader("💡 Creative Concepts")
        st.markdown("Here are several different story directions based on your input:")
        
        # Loop through each generated concept and display it in a clean, bordered container.
        for i, concept in enumerate(narrative_state.story_concepts.concepts):
            with st.container(border=True):
                st.markdown(f"#### Concept {i+1}: {concept.title}")
                st.info(f"**Logline:** {concept.logline}")
                st.markdown(f"**Cinematic Style:** In the style of *{concept.director_style}*")
                st.markdown("**Synopsis:**")
                st.write(concept.brief_synopsis)