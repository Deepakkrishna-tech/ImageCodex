# src/ui/visual_prompting_ui.py
# FINAL VERIFIED VERSION - Stage 2 refactored to match Stage 1's working pattern.

import streamlit as st
from ..core.schemas import VideoCreativeBrief

def render_stage1_ui(controller):
    """Renders the UI for Stage 1. This pattern is correct and working."""
    st.header("Generate Image Prompt")
    st.markdown("Upload an image to analyze its artistic elements and generate a new text-to-image prompt.")
    
    uploaded_image = st.file_uploader("Upload Original Image", type=["png", "jpg", "jpeg"], key="stage1_uploader")

    if uploaded_image:
        st.image(uploaded_image, caption="Your uploaded image.", width=300)
        
        if st.button("Analyze and Generate Prompt", type="primary", key="generate_prompt_a_button"):
            controller.run_visual_workflow(image_bytes=uploaded_image.getvalue())
            st.rerun()

    if controller.state.image_prompt:
        st.subheader("Generated Image Prompt (Prompt A)")
        st.text_area("Prompt Body", value=controller.state.image_prompt.prompt_body, height=150)
        st.code(controller.state.image_prompt.technical_parameters)
        
        if controller.state.prompt_critique:
            st.markdown("---")
            st.subheader("🕵️‍♂️ Prompt Inspection")
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
                st.rerun()

def render_stage2_ui(controller):
    """
    Renders the UI for Stage 2. 
    FIXED: This function has been refactored to remove st.form and use a direct st.button,
    matching the reliable pattern from Stage 1.
    """
    st.header("Generate Video Prompt")
    st.markdown("Upload an image and provide a creative brief to generate a cinematic video prompt.")
    
    uploaded_image = st.file_uploader("Upload Image for Video", type=["png", "jpg", "jpeg"], key="stage2_uploader")
    if uploaded_image:
        st.image(uploaded_image, caption="Image for video generation.", width=300)
    
    # --- THIS IS THE FIX ---
    # We remove the `st.form` wrapper. The input widgets now live directly on the page.
    # Streamlit automatically maintains their state across reruns.
    st.subheader("Creative Brief")
    moods = st.text_input("Moods (comma-separated)", "tense, dreamy, epic", key="s2_moods")
    camera = st.text_input("Camera Movement", "slow dolly zoom", key="s2_camera")
    notes = st.text_area("Additional Notes", "Focus on the character's eyes.", key="s2_notes")
    
    # We use a standard button. When clicked, it will execute the code inside the `if` block.
    # This is a much more direct and reliable way to trigger the workflow.
    if st.button("Generate Video Prompt", type="primary", key="generate_prompt_b_button"):
        # The logic that was previously inside the form is now here.
        brief = VideoCreativeBrief(
            moods=[m.strip() for m in moods.split(',')],
            camera_movement=camera, 
            additional_notes=notes
        )
        
        # This logic is unchanged, it correctly finds the image to use.
        image_data = uploaded_image.getvalue() if uploaded_image else controller.state.original_image_bytes
        
        if not image_data:
            st.warning("Please upload an image or run Stage 1 first to provide an image.")
        else:
            # The controller is now guaranteed to be called.
            # You will see the "The AI team is working..." spinner.
            controller.run_visual_workflow(image_bytes=image_data, video_brief=brief)
            st.rerun()

    # The display logic for the output is unchanged.
    if controller.state.video_prompt:
        st.subheader("Generated Video Prompt (Prompt B)")
        st.success(controller.state.video_prompt)