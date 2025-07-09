# src/core/schemas.py
"""
This file contains the final, unified Pydantic schemas for the ImageCodeX application.
This version restores all original schemas and integrates the new Stage 3 and Stage 4 components.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

# ==============================================================================
# == STAGE 1 & 2 SCHEMAS (Visual Prompting)
# ==============================================================================

class VideoCreativeBrief(BaseModel):
    moods: Optional[List[str]] = None
    camera_movement: Optional[str] = None
    additional_notes: Optional[str] = None

class VisualAnalysis(BaseModel):
    main_subject: str
    setting_and_environment: str
    artistic_style: str
    mood_and_atmosphere: str
    lighting_style: str
    color_scheme: List[str]
    compositional_notes: str

class ImagePrompt(BaseModel):
    prompt_body: str
    technical_parameters: str = Field(default="--ar 16:9 --v 6.0 --style raw")

class PromptCritique(BaseModel):
    is_accurate: bool
    accuracy_score: int = Field(ge=1, le=10)
    critique: str
    suggested_improvement: str

# ==============================================================================
# == STAGE 3 SCHEMAS (Narrative Engine) - FULLY RESTORED AND UPDATED
# ==============================================================================

# --- Legacy V2 Schemas (Restored for compatibility) ---
class StoryConcept(BaseModel):
    title: str
    logline: str
    director_style: str
    brief_synopsis: str

class StoryConceptCollection(BaseModel):
    concepts: List[StoryConcept]

class ScreenplayScene(BaseModel):
    scene_header: str
    action_description: str
    character_dialogue: Optional[Dict[str, List[str]]] = None

class Screenplay(BaseModel): # RESTORED
    title: str
    scenes: List[ScreenplayScene]

class StoryArc(BaseModel): # RESTORED
    title: str
    premise: str
    protagonist: str
    conflict: str
    resolution: str
    themes: List[str] = Field(default_factory=list)
    genre: str = Field(default="Drama")
    tone: str = Field(default="Neutral")

class StoryboardItem(BaseModel):
    scene_number: int
    shot_number: int
    shot_type: str
    shot_description: str
    cinematic_prompt: str

class Storyboard(BaseModel): # RESTORED
    items: List[StoryboardItem]
    
# --- V3 Cinematic Narrative Engine Schemas (New) ---
class CinematicNarrativeOutput(BaseModel):
    before_scene_cinematic: str = Field(description="The cinematic scene describing what happened just before the image.")
    after_scene_cinematic: str = Field(description="The cinematic scene describing what happens next.")
    before_scene_prompt: str = Field(description="A refined, high-quality prompt for generating the 'Before' scene image.")
    after_scene_prompt: str = Field(description="A refined, high-quality prompt for generating the 'After' scene image.")
    source_of_inspiration: str = Field(description="Records the inspiration mode used (e.g., AI, Inspired by 'Spiderman').")

# ==============================================================================
# == STAGE 4 SCHEMAS (Image Generation)
# ==============================================================================

class ImageGenerationParams(BaseModel):
    model: Literal["gpt-4o", "sdxl", "kandinsky-2.2"] = Field("gpt-4o")
    prompt: str
    negative_prompt: Optional[str] = None
    aspect_ratio: Literal["1:1", "16:9", "9:16"] = Field("1:1")
    reference_image: Optional[bytes] = Field(
        None, 
        description="Optional reference image for img2img or variation generation.",
        exclude=True
    )

class GeneratedImage(BaseModel):
    image_url: str
    model_used: str
    prompt_used: str
    metadata: dict = Field(default_factory=dict)

# ==============================================================================
# == MASTER APPLICATION STATE OBJECT
# ==============================================================================

class NarrativeState(BaseModel):
    # --- V3 Cinematic Engine Inputs ---
    input_image_bytes: Optional[bytes] = Field(None, exclude=True)
    initial_idea: Optional[str] = None
    genre: str = "Filmmaker's Choice"
    mood: str = "Filmmaker's Choice"
    inspiration_mode: Literal["🧠 AI Imagination", "🎞️ Inspired By", "📚 Original Story"] = "🧠 AI Imagination"
    story_reference: Optional[str] = None

    # --- V3 Cinematic Engine Outputs ---
    cinematic_output: Optional[CinematicNarrativeOutput] = None

    # --- V3 Internal Agent State (for dev view) ---
    context_summary: Optional[str] = None
    inspiration_phrases: Optional[List[str]] = None
    
    # --- V3 UI State ---
    is_locked: bool = False
    
    # --- V2 Legacy Outputs (kept for compatibility) ---
    story_concepts: Optional[StoryConceptCollection] = None
    screenplay: Optional[Screenplay] = None
    storyboard: Optional[Storyboard] = None
    story_arc: Optional[StoryArc] = None

class AppState(BaseModel):
    # STAGES 1 & 2 STATE
    original_image_bytes: Optional[bytes] = None
    visual_analysis: Optional[VisualAnalysis] = None
    image_prompt: Optional[ImagePrompt] = None
    prompt_critique: Optional[PromptCritique] = None
    video_creative_brief: Optional[VideoCreativeBrief] = None
    video_prompt: Optional[str] = None
    
    # REFINEMENT STATE
    user_feedback: Optional[str] = None
    active_prompt_for_refinement: Optional[Literal["image", "video"]] = None

    # STAGE 3 STATE
    narrative_state: NarrativeState = Field(default_factory=NarrativeState)
    
    # STAGE 4 STATE
    image_gen_params: Optional[ImageGenerationParams] = None
    generated_images: List[GeneratedImage] = Field(default_factory=list)

    # UTILITY STATE
    error_message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True