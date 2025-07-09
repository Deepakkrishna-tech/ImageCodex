# src/core/schemas.py
"""
This file contains the final, unified Pydantic schemas for the ImageCodeX application,
defining the data structures for all stages and the master application state.
This version restores all original schemas and integrates Stage 4 components.
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
# == STAGE 3 SCHEMAS (Narrative Engine)
# ==============================================================================

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

class Screenplay(BaseModel):
    title: str
    scenes: List[ScreenplayScene]

class StoryArc(BaseModel):
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

class Storyboard(BaseModel):
    items: List[StoryboardItem]

# ==============================================================================
# == STAGE 4 SCHEMAS (Image Generation)
# ==============================================================================

class ImageGenerationParams(BaseModel):
    """Parameters for the image generation request."""
    model: Literal["gpt-4o", "sdxl", "kandinsky-2.2"] = Field("gpt-4o")
    prompt: str
    negative_prompt: Optional[str] = None
    aspect_ratio: Literal["1:1", "16:9", "9:16"] = Field("1:1")

class GeneratedImage(BaseModel):
    """Represents a single generated image and its metadata."""
    image_url: str
    model_used: str
    prompt_used: str
    metadata: dict = Field(default_factory=dict)

# ==============================================================================
# == MASTER APPLICATION STATE OBJECT
# ==============================================================================

class NarrativeState(BaseModel):
    # Inputs
    input_image_bytes: Optional[bytes] = None
    initial_idea: Optional[str] = None
    genre: str = "Filmmaker's Choice"
    mood: str = "Filmmaker's Choice"
    # Brainstorming Output
    story_concepts: Optional[StoryConceptCollection] = None
    # Future Development Outputs
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
    
    # STAGE 4 STATE - INTEGRATED
    image_gen_params: Optional[ImageGenerationParams] = None
    generated_images: List[GeneratedImage] = Field(default_factory=list)

    # UTILITY STATE - INTEGRATED
    error_message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True