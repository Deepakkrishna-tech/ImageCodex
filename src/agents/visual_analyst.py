# src/agents/visual_analyst.py
import base64
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ..core.schemas import VisualAnalysis
from ..core.prompts import VISUAL_ANALYST_PROMPT

def run_visual_analyst(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---AGENT: VISUAL ANALYST---")
    print(f"STATE KEYS RECEIVED BY VISUAL_ANALYST: {list(state.keys())}")

    image_bytes = state.get("original_image_bytes")
    if not image_bytes:
        print("---AGENT: SKIPPING VISUAL ANALYST - NO IMAGE---")
        return state

    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    structured_llm = llm.with_structured_output(VisualAnalysis)
    prompt = ChatPromptTemplate.from_messages([
        ("system", VISUAL_ANALYST_PROMPT),
        ("human", [{"type": "text", "text": "Analyze this image..."},
                   {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}])
    ])
    chain = prompt | structured_llm
    response = chain.invoke({})
    
    print("---AGENT: Generated Visual Analysis---")
    
    # --- THIS IS THE FIX ---
    # Add the result to the state and return the ENTIRE state.
    state["visual_analysis"] = response
    return state