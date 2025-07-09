# src/agents/refiner.py
# FINAL VERIFIED VERSION - Corrected the prompt import and added robust logic.

from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import ImagePrompt

# --- THIS IS THE FIX ---
# We are now importing the correct variable name from the prompts file.
from ..core.prompts import PROMPT_REFINER_PROMPT

def run_refiner(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes user feedback and refines an existing prompt (either image or video).
    """
    print("---AGENT: PROMPT REFINER---")
    
    user_feedback = state.get("user_feedback")
    refinement_target = state.get("active_prompt_for_refinement")
    
    if not user_feedback or not refinement_target:
        print("---AGENT: SKIPPING REFINER - NO FEEDBACK OR TARGET---")
        return {}

    # Determine which prompt to refine based on the target
    if refinement_target == "image":
        original_prompt_obj: ImagePrompt = state.get("image_prompt")
        if not original_prompt_obj:
            return {"user_feedback": None} # Nothing to refine, clear feedback
        original_prompt_text = original_prompt_obj.prompt_body
    elif refinement_target == "video":
        original_prompt_text = state.get("video_prompt")
        if not original_prompt_text:
            return {"user_feedback": None} # Nothing to refine, clear feedback
    else:
        return {"user_feedback": None} # Invalid target, clear feedback

    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

    # --- THIS IS THE SECOND PART OF THE FIX ---
    # Create the prompt template using the CORRECT variable name.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_REFINER_PROMPT)
    
    chain = prompt_template | llm

    # Invoke the chain to get the refined prompt string
    refined_prompt_str = chain.invoke({
        "original_prompt": original_prompt_text,
        "user_feedback": user_feedback
    }).content
    
    print(f"---AGENT: Refined prompt to: {refined_prompt_str[:100]}...---")

    # Prepare the state update dictionary
    update_dict = {
        "user_feedback": None,  # Clear feedback to prevent loops
        "active_prompt_for_refinement": None # Clear target
    }

    # Update the correct part of the state with the new prompt
    if refinement_target == "image":
        # When refining an image prompt, we only update the body, keeping the tech parameters.
        original_prompt_obj.prompt_body = refined_prompt_str
        update_dict["image_prompt"] = original_prompt_obj
    elif refinement_target == "video":
        update_dict["video_prompt"] = refined_prompt_str
        
    return update_dict