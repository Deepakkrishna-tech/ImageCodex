# src/agents/prompt_engineer.py
import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import ImagePrompt, VisualAnalysis
from ..core.prompts import PROMPT_ENGINEER_PROMPT

def run_prompt_engineer(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---AGENT: PROMPT ENGINEER---")
    print(f"STATE KEYS RECEIVED BY PROMPT_ENGINEER: {list(state.keys())}")

    analysis: VisualAnalysis = state.get("visual_analysis")
    if not analysis:
        print("---AGENT: SKIPPING PROMPT ENGINEER - NO VISUAL ANALYSIS---")
        return state

    llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
    structured_llm = llm.with_structured_output(ImagePrompt)
    prompt = ChatPromptTemplate.from_template(PROMPT_ENGINEER_PROMPT)
    chain = prompt | structured_llm
    analysis_json_string = json.dumps(analysis.model_dump(), indent=2)
    response = chain.invoke({"analysis": analysis_json_string})
    
    print("---AGENT: Generated Image Prompt---")
    
    # --- THIS IS THE FIX ---
    state["image_prompt"] = response
    return state