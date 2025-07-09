# src/agents/image_generator.py

import os
import replicate
from openai import OpenAI
from typing import Dict
import logging
import io

from src.core.schemas import AppState, GeneratedImage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Model Identifiers for Replicate ---
# This dictionary has the UPDATED, working hash for SDXL
REPLICATE_MODELS = {
    "sdxl": "stability-ai/sdxl:2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2",
    "kandinsky-2.2": "ai-forever/kandinsky-2.2:ea1addaab376f4dc227f5368bbd8eff901820fd1cc14ed8cad63b29249e9d463",
}

class ImageGenerator:
    """A class to handle image generation from various models."""

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # --- Text-to-Image Methods (Existing) ---
    def _generate_openai_text2img(self, prompt: str, aspect_ratio: str) -> str:
        # ... (This function is the same as the old _generate_with_openai)
        logger.info(f"Generating image with GPT-4o (Text-to-Image). Prompt: {prompt[:50]}...")
        size_mapping = {"1:1": "1024x1024", "16:9": "1792x1024", "9:16": "1024x1792"}
        response = self.openai_client.images.generate(model="dall-e-3", prompt=prompt, n=1, size=size_mapping.get(aspect_ratio, "1024x1024"), quality="standard", style="vivid")
        image_url = response.data[0].url
        logger.info(f"GPT-4o image generated: {image_url}")
        return image_url

    def _generate_replicate_text2img(self, model_name: str, params: Dict) -> str:
        # ... (This function is the same as the old _generate_with_replicate)
        logger.info(f"Generating image with Replicate model (Text-to-Image): {model_name}. Prompt: {params['prompt'][:50]}...")
        # ... (rest of the logic is identical)
        model_version = REPLICATE_MODELS.get(model_name)
        if not model_version: raise ValueError(f"Model {model_name} not found.")
        width, height = 1024, 1024
        if params["aspect_ratio"] == "16:9": width, height = 1344, 768
        elif params["aspect_ratio"] == "9:16": width, height = 768, 1344
        input_payload = {"prompt": params["prompt"], "negative_prompt": params.get("negative_prompt", ""), "width": width, "height": height}
        output = replicate.run(model_version, input=input_payload)
        if isinstance(output, list) and len(output) > 0:
            return output[0]
        raise ConnectionError(f"Replicate API did not return a valid image URL. Output: {output}")

    # --- NEW: Image-to-Image Methods ---
    def _generate_openai_variation(self, image_bytes: bytes, aspect_ratio: str) -> str:
        """Generates a variation of an image using OpenAI's API. Note: This API ignores text prompts."""
        logger.info("Generating image variation with OpenAI...")
        size_mapping = {"1:1": "1024x1024", "16:9": "1792x1024", "9:16": "1024x1792"}
        response = self.openai_client.images.create_variation(
            image=image_bytes,
            n=1,
            model="dall-e-2", # The variation endpoint currently uses the dall-e-2 model
            size=size_mapping.get(aspect_ratio, "1024x1024")
        )
        image_url = response.data[0].url
        logger.info(f"OpenAI image variation generated: {image_url}")
        return image_url

    def _generate_replicate_img2img(self, model_name: str, params: Dict, image_bytes: bytes) -> str:
        """Generates an image from a prompt and a reference image using a Replicate model."""
        logger.info(f"Generating image with Replicate model (Image-to-Image): {model_name}. Prompt: {params['prompt'][:50]}...")
        model_version = REPLICATE_MODELS.get(model_name)
        if not model_version: raise ValueError(f"Model {model_name} not found.")
        
        input_payload = {
            "prompt": params["prompt"],
            "negative_prompt": params.get("negative_prompt", ""),
            # IMPORTANT: Pass the image bytes to the API
            "image": io.BytesIO(image_bytes),
            # Img2Img models often use a strength parameter
            "prompt_strength": 0.85, 
        }
        output = replicate.run(model_version, input=input_payload)
        if isinstance(output, list) and len(output) > 0:
            return output[0]
        raise ConnectionError(f"Replicate API did not return a valid image URL. Output: {output}")

    # --- Main Agent Router ---
    def run(self, state: AppState) -> AppState:
        """The main execution method for the agent, now routing between text2img and img2img."""
        params = state.image_gen_params
        if not params:
            state.error_message = "Image generation parameters not provided."
            return state

        try:
            image_url = ""
            prompt_for_log = params.prompt
            
            # ROUTING LOGIC: Check if a reference image was provided
            if params.reference_image:
                if params.model == "gpt-4o":
                    # OpenAI variation API ignores the prompt, so we log that.
                    prompt_for_log = "Variation of uploaded image"
                    image_url = self._generate_openai_variation(params.reference_image, params.aspect_ratio)
                else: # SDXL or Kandinsky
                    image_url = self._generate_replicate_img2img(params.model, params.model_dump(), params.reference_image)
            else: # Standard text-to-image
                if params.model == "gpt-4o":
                    image_url = self._generate_openai_text2img(params.prompt, params.aspect_ratio)
                else:
                    image_url = self._generate_replicate_text2img(params.model, params.model_dump())

            new_image = GeneratedImage(
                image_url=image_url, model_used=params.model,
                prompt_used=prompt_for_log, metadata={"aspect_ratio": params.aspect_ratio}
            )
            state.generated_images.append(new_image)
            state.error_message = None
        except Exception as e:
            error_msg = f"Failed to generate image with {params.model}: {e}"
            logger.error(error_msg, exc_info=True)
            state.error_message = error_msg
        return state

# --- CRITICAL: These lines connect the class to LangGraph ---

# 1. Create a single, shared instance of the agent's logic.
image_generator_agent = ImageGenerator()

# 2. Define the function that will be registered as a node in the graph.
# This is the function that was missing and causing the ImportError.
def generate_image_node(state: AppState) -> AppState:
    """
    LangGraph node to orchestrate image generation.
    It takes the current state, invokes the ImageGenerator, and returns the updated state.
    """
    return image_generator_agent.run(state)