# src/agents/utils.py
# This file contains utility functions shared across different agents.

from langchain_openai import ChatOpenAI
from src.core.schemas import VisualAnalysis
import base64

# --- Import the correct message classes from LangChain ---
from langchain_core.messages import HumanMessage

def analyze_image_for_narrative(image_bytes: bytes) -> str:
    """
    Analyzes an image using a vision model and returns a structured analysis
    as a string, ready to be injected into a subsequent prompt.
    """
    # 1. Select the right model. gpt-4o is the modern, preferred choice for this.
    # It fully supports structured output and is generally faster and cheaper.
    vision_llm = ChatOpenAI(model="gpt-4o", max_tokens=1024)
    structured_llm = vision_llm.with_structured_output(VisualAnalysis)

    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    image_url = f"data:image/png;base64,{encoded_image}"

    # 2. THIS IS THE FIX: Construct the message using the correct "envelope".
    # We create a single HumanMessage that contains a list of content blocks (text and image).
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "You are a master art director. Analyze this image for its narrative potential. Deconstruct its visual and emotional components into the structured format requested. Focus on details a filmmaker would find invaluable.",
            },
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            },
        ]
    )
    
    try:
        # 3. Invoke the model with the correctly formatted message.
        # We pass the message inside a list, as the invoke method expects an iterable.
        analysis_result = structured_llm.invoke([message])
        
        # 4. Convert the Pydantic object to a nicely formatted JSON string for the next LLM.
        return analysis_result.model_dump_json(indent=2)
    except Exception as e:
        print(f"Error during image analysis: {e}")
        # This print will now show up in your terminal if something else goes wrong.
        return "Error: The provided image could not be analyzed."