# src/ui/stage4_ui.py

import streamlit as st
import requests
import time
from src.core.schemas import AppState, ImageGenerationParams

# --- Helper function to get image data from a URL (Unchanged) ---
@st.cache_data(show_spinner=False)
def get_image_bytes(url: str) -> bytes:
    """Fetches an image from a URL and returns its content as bytes."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        st.error(f"Failed to download image from URL: {e}")
        return b""

# --- Model options dictionary (Unchanged) ---
MODEL_OPTIONS = {
    "GPT-4o (via DALL-E 3)": "gpt-4o",
    "Stable Diffusion XL": "sdxl",
    "Kandinsky 2.2": "kandinsky-2.2",
}

def show_stage4_ui(app_state: AppState, controller):
    """
    Renders the UI for Stage 4, now with an optional image-to-image feature.
    """
    st.header("Stage 4: Generate Image from Prompt")
    st.markdown("Bring your prompt to life. Select a model and generate a visual representation of your idea.")

    # --- Prompt Input (Unchanged) ---
    stage1_prompt = ""
    if app_state.image_prompt and app_state.image_prompt.prompt_body:
        stage1_prompt = f"{app_state.image_prompt.prompt_body} {app_state.image_prompt.technical_parameters}"
    if 'stage4_prompt' not in st.session_state:
        st.session_state.stage4_prompt = stage1_prompt
    prompt = st.text_area(
        "📝 **Prompt for Image Generation**",
        value=st.session_state.stage4_prompt,
        height=150,
        help="This prompt is pre-filled from Stage 1 if available. You can edit it directly."
    )
    st.session_state.stage4_prompt = prompt

    st.divider()

    # --- NEW: Optional Image-to-Image Controls ---
    with st.container(border=True):
        use_img2img = st.checkbox("Use Reference Image (Image-to-Image / Variation)")
        reference_image_bytes = None
        
        if use_img2img:
            st.info("When using a reference image with **GPT-4o**, the text prompt is ignored and a variation will be created. For **SDXL/Kandinsky**, the prompt will guide the new image generation.", icon="ℹ️")
            uploaded_ref_image = st.file_uploader(
                "Upload Reference Image", 
                type=["png", "jpg", "jpeg"], 
                key="ref_uploader"
            )
            if uploaded_ref_image:
                st.image(uploaded_ref_image, caption="Your reference image.", width=200)
                reference_image_bytes = uploaded_ref_image.getvalue()
    
    # --- Generation Parameters (Unchanged) ---
    st.subheader("Generation Settings")
    col1, col2 = st.columns(2)
    with col1:
        selected_model_display = st.selectbox("🤖 **Select Model**", options=MODEL_OPTIONS.keys(), help="Choose the AI model.")
        model_backend = MODEL_OPTIONS[selected_model_display]
    with col2:
        aspect_ratio = st.selectbox("🖼️ **Aspect Ratio**", options=["1:1", "16:9", "9:16"], help="Select the desired aspect ratio.")
    negative_prompt = st.text_input("🚫 **Negative Prompt (Optional)**", placeholder="e.g., blurry, low quality, text, watermark")

    # --- Generate Button (Logic Updated) ---
    if st.button("Generate Image ✨", type="primary", use_container_width=True):
        if not prompt:
            st.error("Please enter a prompt before generating an image.")
        elif use_img2img and not reference_image_bytes:
            st.error("Please upload a reference image when the checkbox is selected.")
        else:
            params = ImageGenerationParams(
                prompt=prompt,
                model=model_backend,
                aspect_ratio=aspect_ratio,
                negative_prompt=negative_prompt if negative_prompt else None,
                # NEW: Pass the image bytes to the backend
                reference_image=reference_image_bytes
            )
            # This part is now an attribute assignment, not a direct state modification
            controller.state.image_gen_params = params
            controller.run_image_generation_workflow()

    st.divider()

    # --- Display Logic (Unchanged) ---
    if app_state.error_message:
        st.error(f"An error occurred: {app_state.error_message}")

    if app_state.generated_images:
        st.subheader("Generated Images")
        for i, img in enumerate(reversed(app_state.generated_images)):
            with st.container(border=True):
                display_name = next((name for name, backend_name in MODEL_OPTIONS.items() if backend_name == img.model_used), img.model_used)
                st.image(img.image_url, caption=f"Generated with {display_name} ({img.metadata.get('aspect_ratio', 'N/A')})")
                
                image_bytes = get_image_bytes(img.image_url)
                if image_bytes:
                    filename = f"imagecodex_{img.model_used}_{int(time.time())}.png"
                    st.download_button(
                        label="Download Image 📥",
                        data=image_bytes,
                        file_name=filename,
                        mime="image/png",
                        key=f"download_btn_{i}"
                    )
                
                with st.expander("View Prompt Used"):
                    st.code(img.prompt_used, language='text')