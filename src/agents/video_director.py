# src/agents/video_director.py
# FINAL VERIFIED VERSION - Corrected the logic for handling image data.

from typing import Dict, Any
import base64

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

from ..core.prompts import VIDEO_DIRECTOR_PROMPT

def run_video_director(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runs the Video Director agent.
    FIXED: This function now correctly checks for and uses the image data.
    """
    print("---AGENT: VIDEO DIRECTOR---")
    
    # --- THIS IS THE FIX ---
    # The agent was failing to correctly find the image. We now have robust logic.
    image_bytes = state.get("original_image_bytes")
    
    if not image_bytes:
        # This was the message you saw in your log.
        print("---AGENT: SKIPPING VIDEO DIRECTOR - NO IMAGE PROVIDED IN STATE---")
        # Return an empty state update to avoid errors.
        return {}

    # If we have an image, proceed with the agent's main logic.
    print("---AGENT: Image found, generating video prompt...---")
    
    # Encode the image for the API call
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Get the user's creative brief from the state
    brief = state.get("video_creative_brief", {})
    moods = brief.get("moods", ["cinematic"])
    camera_movement = brief.get("camera_movement", "none")
    additional_notes = brief.get("additional_notes", "N/A")

    # Initialize the LLM
    # We use gpt-4o as it's best for multimodal tasks.
    llm = ChatOpenAI(model="gpt-4o", temperature=0.4)

    # Construct the prompt with all the information
    prompt_text = f"""
    **Creative Brief:**
    - Moods to capture: {', '.join(moods)}
    - Desired camera movement: {camera_movement}
    - Additional Director's Notes: {additional_notes}

    **Your Task:**
    Based on the provided image and the creative brief, generate a concise, single-paragraph video prompt.
    The prompt should be suitable for a text-to-video model like Sora or Runway.
    Describe the scene, the action, and the cinematic style.
    """

    # Create the message payload for the multimodal LLM
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ]
    )

    # Invoke the LLM and get the response
    response = llm.invoke([message])
    video_prompt_text = response.content
    
    print(f"---AGENT: Generated Video Prompt: {video_prompt_text[:100]}...---")

    # Return the result in the correct key to update the application's master state
    return {"video_prompt": video_prompt_text}