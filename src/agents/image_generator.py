# src/agents/image_generator.py

import os
import replicate
from openai import OpenAI
from typing import Dict
import logging

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
        """Initializes the OpenAI client."""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _generate_with_openai(self, prompt: str, aspect_ratio: str) -> str:
        """Generates an image using OpenAI's DALL-E 3."""
        logger.info(f"Generating image with GPT-4o (DALL-E 3). Prompt: {prompt[:50]}...")
        
        size_mapping = { "1:1": "1024x1024", "16:9": "1792x1024", "9:16": "1024x1792" }
        
        response = self.openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=size_mapping.get(aspect_ratio, "1024x1024"),
            quality="standard",
            style="vivid"
        )
        image_url = response.data[0].url
        logger.info(f"GPT-4o image generated: {image_url}")
        return image_url

    def _generate_with_replicate(self, model_name: str, params: Dict) -> str:
        """Generates an image using a model on Replicate."""
        logger.info(f"Generating image with Replicate model: {model_name}. Prompt: {params['prompt'][:50]}...")
        model_version = REPLICATE_MODELS.get(model_name)
        if not model_version:
            raise ValueError(f"Model {model_name} not found in Replicate model list.")
        width, height = 1024, 1024
        if params["aspect_ratio"] == "16:9": width, height = 1344, 768
        elif params["aspect_ratio"] == "9:16": width, height = 768, 1344
        input_payload = {
            "prompt": params["prompt"],
            "negative_prompt": params.get("negative_prompt", ""),
            "width": width, "height": height
        }
        output = replicate.run(model_version, input=input_payload)
        if isinstance(output, list) and len(output) > 0:
            image_url = output[0]
            logger.info(f"Replicate image generated: {image_url}")
            return image_url
        else:
            raise ConnectionError(f"Replicate API did not return a valid image URL. Output: {output}")

    def run(self, state: AppState) -> AppState:
        """The main execution method for the agent."""
        params = state.image_gen_params
        if not params:
            state.error_message = "Image generation parameters not provided."
            return state
        try:
            image_url = ""
            if params.model == "gpt-4o":
                image_url = self._generate_with_openai(prompt=params.prompt, aspect_ratio=params.aspect_ratio)
            elif params.model in REPLICATE_MODELS:
                image_url = self._generate_with_replicate(params.model, params.model_dump())
            else:
                raise ValueError(f"Unsupported model: {params.model}")
            new_image = GeneratedImage(
                image_url=image_url,
                model_used=params.model,
                prompt_used=params.prompt,
                metadata={"aspect_ratio": params.aspect_ratio}
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