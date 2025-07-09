# src/graph/__init__.py
# This file defines the public API for the graph module.

# CORRECTED: We now import and export the new cinematic graph function
# instead of the old, non-existent one.
from .graphs import (
    build_visual_workflow_graph,
    build_cinematic_narrative_graph, # This replaces the old name
    build_image_generation_graph
)

# This makes the functions directly importable from src.graph
__all__ = [
    "build_visual_workflow_graph",
    "build_cinematic_narrative_graph", # And we expose the new name here
    "build_image_generation_graph"
]