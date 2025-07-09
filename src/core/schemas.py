# src/core/schemas.py
# This is the final, verified schema definition for the ImageCodeX application.

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

# ==============================================================================
# == STAGE 1 & 2 SCHEMAS (Visual & Cinematic Prompting)
# ==============================================================================

class VideoCreativeBrief(BaseModel):
    """A structured brief from the user to guide the VideoDirectorAgent."""
    moods: Optional[List[str]] = None
    camera_movement: Optional[str] = None
    additional_notes: Optional[str] = None

class VisualAnalysis(BaseModel):
    """Structured analysis from the VisualAnalystAgent."""
    main_subject: str = Field(..., description="The primary subject or focal point of the image.")
    setting_and_environment: str = Field(..., description="The environment where the subject is located.")
    artistic_style: str = Field(..., description="e.g., 'photorealistic', 'oil painting', 'anime', '3D render'.")
    mood_and_atmosphere: str = Field(..., description="The dominant emotion or feeling conveyed.")
    lighting_style: str = Field(..., description="e.g., 'cinematic lighting', 'soft natural light', 'dramatic shadows'.")
    color_scheme: List[str] = Field(..., description="A list of dominant or notable colors.")
    compositional_notes: str = Field(..., description="Notes on camera angle, shot type, and framing.")

class ImagePrompt(BaseModel):
    """The structured text-to-image prompt (Prompt A) generated in Stage 1."""
    prompt_body: str = Field(..., description="The main descriptive part of the prompt.")
    technical_parameters: str = Field(default="--ar 16:9 --v 6.0 --style raw", description="Technical flags for the image model.")

class PromptCritique(BaseModel):
    """A structured critique from the InspectorAgent."""
    is_accurate: bool = Field(..., description="A simple boolean on whether the prompt accurately reflects the analysis.")
    accuracy_score: int = Field(..., ge=1, le=10, description="A score from 1 (poor) to 10 (perfect).")
    critique: str = Field(..., description="A brief explanation of the score and any discrepancies.")
    suggested_improvement: str = Field(..., description="Actionable suggestions to improve the prompt.")

# ==============================================================================
# == STAGE 3 SCHEMAS (Narrative Engine)
# ==============================================================================

class StoryArcScene(BaseModel):
    """A single scene within a larger story arc."""
    scene_number: int
    title: str
    summary: str
    setting: str
    key_visual_moment: str

class StoryArc(BaseModel):
    """A complete, structured story arc with a beginning, middle, and end."""
    title: str
    logline: str
    theme: str
    genre: str
    scenes: List[StoryArcScene]

class ScreenplayScene(BaseModel):
    """A scene formatted in standard screenplay structure."""
    scene_header: str
    action_description: str
    character_dialogue: Optional[Dict[str, List[str]]] = None

class Screenplay(BaseModel):
    """A complete short screenplay, composed of multiple scenes."""
    title: str
    scenes: List[ScreenplayScene]

class StoryboardItem(BaseModel):
    """A single storyboard panel, representing a key shot in a scene."""
    scene_number: int
    shot_number: int
    shot_type: str
    shot_description: str
    cinematic_prompt: str

class Storyboard(BaseModel):
    """A container for a complete storyboard, which consists of a list of individual items."""
    items: List[StoryboardItem]

# ==============================================================================
# == MASTER STATE OBJECT
# ==============================================================================

class NarrativeState(BaseModel):
    """A nested state object that holds all data related to the Stage 3 Narrative Engine workflow."""
    input_image_bytes: Optional[bytes] = None
    initial_idea: Optional[str] = None
    genre: str = "Filmmaker's Choice"
    mood: str = "Filmmaker's Choice"
    story_arc: Optional[StoryArc] = None
    screenplay: Optional[Screenplay] = None
    storyboard: Optional[Storyboard] = None

class AppState(BaseModel):
    """The complete, stateful 'story' of a user's session. It holds all data for all stages."""
    # STAGES 1 & 2
    original_image_bytes: Optional[bytes] = None
    visual_analysis: Optional[VisualAnalysis] = None
    image_prompt: Optional[ImagePrompt] = None
    prompt_critique: Optional[PromptCritique] = None
    video_creative_brief: Optional[VideoCreativeBrief] = None
    video_prompt: Optional[str] = None
    
    # REFINEMENT
    user_feedback: Optional[str] = None
    active_prompt_for_refinement: Optional[Literal["image", "video"]] = None

    # STAGE 3
    narrative_state: NarrativeState = Field(default_factory=NarrativeState)

    class Config:
        arbitrary_types_allowed = True