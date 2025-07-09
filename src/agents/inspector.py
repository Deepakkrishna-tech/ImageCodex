# src/agents/inspector.py
import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import PromptCritique, ImagePrompt, VisualAnalysis
from ..core.prompts import INSPECTOR_PROMPT

def run_inspector(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---AGENT: PROMPT INSPECTOR---")
    print(f"STATE KEYS RECEIVED BY INSPECTOR: {list(state.keys())}")
    
    analysis: VisualAnalysis = state.get("visual_analysis")
    prompt: ImagePrompt = state.get("image_prompt")
    if not analysis or not prompt:
        print("---AGENT: SKIPPING INSPECTOR - MISSING ANALYSIS OR PROMPT IN STATE---")
        return state

    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
    structured_llm = llm.with_structured_output(PromptCritique)
    prompt_template = ChatPromptTemplate.from_template(INSPECTOR_PROMPT)
    chain = prompt_template | structured_llm
    analysis_json_string = json.dumps(analysis.model_dump(), indent=2)
    prompt_json_string = json.dumps(prompt.model_dump(), indent=2)
    response = chain.invoke({"analysis": analysis_json_string, "prompt": prompt_json_string})
    
    print("---AGENT: Generated Prompt Critique---")

    # --- THIS IS THE FIX ---
    state["prompt_critique"] = response
    return state