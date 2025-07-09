# src/ui/visual_prompting_ui.py
"""
Contains the unified Streamlit UI for the Visual Prompting tab,
covering both Stage 1 (Image Prompt) and Stage 2 (Video Prompt).
"""

import streamlit as st
from ..core.schemas import VideoCreativeBrief

def show_visual_prompting_ui(controller):
    """
    Renders the complete UI for the "Visual Prompting" tab.
    This function consolidates the original render_stage1_ui and render_stage2_ui.
    """
    st.header("Stages 1 & 2: Visual Prompting")
    st.markdown("Use AI to analyze an image, generate a text-to-image prompt, and then extend it into a cinematic video concept.")
    
    # --- STAGE 1: IMAGE PROMPT GENERATION ---
    st.subheader("Stage 1: Generate Image Prompt", divider='rainbow')
    
    uploaded_image_s1 = st.file_uploader("Upload Original Image", type=["png", "jpg", "jpeg"], key="stage1_uploader")

    if uploaded_image_s1:
        st.image(uploaded_image_s1, caption="Your uploaded image.", width=300)
        
        if st.button("Analyze and Generate Prompt", type="primary", key="generate_prompt_a_button"):
            controller.run_visual_workflow(image_bytes=uploaded_image_s1.getvalue())
            # st.rerun() is handled by the controller now

    if controller.state.image_prompt:
        st.write("##### Generated Image Prompt")
        st.text_area("Prompt Body", value=controller.state.image_prompt.prompt_body, height=150, key="s1_prompt_body")
        st.code(controller.state.image_prompt.technical_parameters)
        
        if controller.state.prompt_critique:
            st.markdown("---")
            st.write("##### 🕵️‍♂️ Prompt Inspection")
            critique = controller.state.prompt_critique
            score = critique.accuracy_score
            color = "green" if score >= 8 else "orange" if score >= 5 else "red"
            st.markdown(f"**Accuracy Score:** <span style='color:{color}; font-weight:bold;'>{score}/10</span>", unsafe_allow_html=True)
            st.info(f"**Critique:** {critique.critique}")
            st.warning(f"**Suggestion:** {critique.suggested_improvement}")

        with st.form("refine_prompt_a_form"):
            feedback = st.text_input("Want changes? Provide feedback.", placeholder="e.g., make it more futuristic, add a sense of urgency")
            submitted = st.form_submit_button("Refine Prompt A")
            if submitted and feedback:
                controller.run_visual_workflow(feedback=feedback, refinement_target='image')
                # st.rerun() is handled by the controller
                
    st.divider()

    # --- STAGE 2: VIDEO PROMPT GENERATION ---
    st.subheader("Stage 2: Generate Video Prompt", divider='rainbow')
    st.markdown("Use an image and a creative brief to generate a cinematic video prompt.")
    
    # Check if we have an image from Stage 1 to use
    image_for_stage2_available = controller.state.original_image_bytes is not None
    st.info("💡 You can use the image from Stage 1 or upload a new one below.", icon="ℹ️")

    uploaded_image_s2 = st.file_uploader("Upload Image for Video (Optional)", type=["png", "jpg", "jpeg"], key="stage2_uploader")
    
    if uploaded_image_s2:
        st.image(uploaded_image_s2, caption="Image for video generation.", width=300)

    st.write("##### Creative Brief")
    moods = st.text_input("Moods (comma-separated)", "tense, dreamy, epic", key="s2_moods")
    camera = st.text_input("Camera Movement", "slow dolly zoom", key="s2_camera")
    notes = st.text_area("Additional Notes", "Focus on the character's eyes.", key="s2_notes")
    
    if st.button("Generate Video Prompt", type="primary", key="generate_prompt_b_button"):
        brief = VideoCreativeBrief(
            moods=[m.strip() for m in moods.split(',')],
            camera_movement=camera, 
            additional_notes=notes
        )
        
        # Use new image if uploaded, otherwise fall back to Stage 1 image
        image_data = uploaded_image_s2.getvalue() if uploaded_image_s2 else controller.state.original_image_bytes
        
        if not image_data:
            st.warning("Please upload an image or run Stage 1 first.")
        else:
            controller.run_visual_workflow(image_bytes=image_data, video_brief=brief)
            # st.rerun() is handled by the controller

    if controller.state.video_prompt:
        st.write("##### Generated Video Prompt")
        st.success(controller.state.video_prompt)