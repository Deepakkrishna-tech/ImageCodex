# src/ui/stage4_ui.py

import streamlit as st
import requests # NEW: Add import for making HTTP requests
from src.core.schemas import AppState, ImageGenerationParams
import time # NEW: Add import for creating unique filenames

# --- NEW: Helper function to get image data from a URL ---
@st.cache_data(show_spinner=False) # Cache the result to avoid re-downloading
def get_image_bytes(url: str) -> bytes:
    """Fetches an image from a URL and returns its content as bytes."""
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.content
    except requests.RequestException as e:
        st.error(f"Failed to download image from URL: {e}")
        return b"" # Return empty bytes on failure

MODEL_OPTIONS = {
    "GPT-4o (via DALL-E 3)": "gpt-4o",
    "Stable Diffusion XL": "sdxl",
    "Kandinsky 2.2": "kandinsky-2.2",
}

def show_stage4_ui(app_state: AppState, controller):
    """
    Renders the UI for the Image Generation stage, now with a download button.
    """
    st.header("Stage 4: Generate Image from Prompt")
    st.markdown("Bring your prompt to life. Select a model and generate a visual representation of your idea.")

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

    col1, col2 = st.columns(2)
    with col1:
        selected_model_display = st.selectbox(
            "🤖 **Select Model**",
            options=MODEL_OPTIONS.keys(),
            help="Choose the AI model. GPT-4o provides the best prompt understanding."
        )
        model_backend = MODEL_OPTIONS[selected_model_display]
        
    with col2:
        aspect_ratio = st.selectbox(
            "🖼️ **Aspect Ratio**",
            options=["1:1", "16:9", "9:16"],
            help="Select the desired aspect ratio for your image."
        )
    
    negative_prompt = st.text_input(
        "🚫 **Negative Prompt (Optional)**",
        placeholder="e.g., blurry, low quality, text, watermark",
        help="Describe what you DON'T want in the image. Mainly for SDXL and Kandinsky."
    )

    if st.button("Generate Image ✨", type="primary", use_container_width=True):
        if not prompt:
            st.error("Please enter a prompt before generating an image.")
        else:
            params = ImageGenerationParams(
                prompt=prompt,
                model=model_backend,
                aspect_ratio=aspect_ratio,
                negative_prompt=negative_prompt if negative_prompt else None
            )
            # The controller state is an object, so we assign to its attributes
            app_state.image_gen_params = params
            controller.run_image_generation_workflow()

    st.divider()

    if app_state.error_message:
        st.error(f"An error occurred: {app_state.error_message}")

    if app_state.generated_images:
        st.subheader("Generated Images")
        for i, img in enumerate(reversed(app_state.generated_images)):
            with st.container(border=True):
                display_name = next((name for name, backend_name in MODEL_OPTIONS.items() if backend_name == img.model_used), img.model_used)
                st.image(img.image_url, caption=f"Generated with {display_name} ({img.metadata.get('aspect_ratio', 'N/A')})")
                
                # --- NEW: Download Button Logic ---
                image_bytes = get_image_bytes(img.image_url)
                if image_bytes:
                    # Create a unique filename based on model and timestamp
                    filename = f"imagecodex_{img.model_used}_{int(time.time())}.png"
                    
                    st.download_button(
                        label="Download Image 📥",
                        data=image_bytes,
                        file_name=filename,
                        mime="image/png", # Set the file type
                        key=f"download_btn_{i}" # Unique key for each button
                    )
                # --- END NEW ---
                
                with st.expander("View Prompt Used"):
                    st.code(img.prompt_used, language='text')