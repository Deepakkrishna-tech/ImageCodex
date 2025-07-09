🎬 ImageCodeX

ImageCodeX is an advanced agentic, multi-agent-powered visual engineering tool designed to transform static images and text prompts into a complete creative workflow. By combining cutting-edge artificial intelligence with intuitive human-in-the-loop collaboration, ImageCodeX empowers users to craft compelling narratives, dynamic video prompts, and high-quality AI-generated images.

![alt text](https://img.shields.io/badge/Python-3.10+-blue.svg)


![alt text](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)


![alt text](https://img.shields.io/badge/Agents-LangGraph-E86F2C)


![alt text](https://img.shields.io/badge/License-MIT-green.svg)

At its core, ImageCodeX leverages a sophisticated multi-stage workflow that guides users through every step of the creative process:

Stage 1 & 2: Visual Prompt Engineering – Analyze static images to generate and refine detailed, model-ready text prompts for both image and cinematic video generation.

Stage 3: Narrative Brainstorming – Expand a visual or text-based idea into multiple high-level story concepts, complete with loglines and director-style pitches.

Stage 4: AI Image Generation – Close the creative loop by generating high-quality images directly from your engineered prompts using a variety of state-of-the-art models.

With its seamless integration of AI-driven insights and human creativity, ImageCodeX bridges the gap between imagination and execution—making it the ultimate tool for storytellers, content creators, and AI enthusiasts.

✨ Features

Stage 1 & 2: Visual Prompting 🖼️ 🎥

Upload an image to receive a detailed, model-ready text-to-image prompt.

Automated analysis of artistic elements, style, mood, and composition.

Extend prompts with creative briefs (mood, camera movement) for cinematic video concepts.

Prompt critique and refinement with user feedback.

Stage 3: Narrative Engine 📖

Brainstorm multiple distinct story concepts from a single image or text idea.

Generate unique titles, loglines, synopses, and director styles for each concept.

Supports genre and mood customization.

Stage 4: AI Image Generation 🎨

Multi-Model Support: Generate images using GPT-4o, Stable Diffusion XL, and Kandinsky 2.2.

Text-to-Image: Create visuals directly from your crafted prompts.

Image-to-Image & Variations: Provide an optional reference image to guide generation or create variations.

Download Functionality: Easily save your generated images with a single click.

Developer Tools 🔧

Dev sidebar for inspecting and clearing the application's real-time state.

Modular, agent-based architecture built with LangGraph for easy extension.

🎥 Demo

![alt text](docs/screenshot.png)

<!-- TODO: Replace with an updated screenshot showing the Stage 4 tab with a generated image. -->


![alt text](https://img.youtube.com/vi/your_video_id/0.jpg)

<!-- TODO: Replace with your actual YouTube video link -->

🚀 Usage

Visual Prompting Tab (Stages 1 & 2)

Image Prompt: Upload an image and click "Analyze and Generate Prompt".

Video Prompt: Provide a creative brief and click "Generate Video Prompt" using either the first image or a new one.

Narrative Engine Tab (Stage 3)

Provide an image, text idea, genre, and mood.

Click "Brainstorm Concepts" to receive multiple story ideas.

Image Generation Tab (Stage 4) 🎨

The prompt from Stage 1 is pre-filled, or you can write a new one.

Select your desired AI model (e.g., GPT-4o) and aspect ratio.

(Optional) Tick "Use Reference Image" and upload an image for img2img/variation.

Click "Generate Image" and review the result.

Click "Download Image" to save your creation.

💻 Tech Stack

Python 3.10+ 🐍

Streamlit – Interactive web UI 🌟

Pydantic – Data validation and modeling 📊

LangChain / LangGraph – Agentic workflow orchestration 🤖

OpenAI & Replicate APIs – Powering LLM and image generation agents 🧠

Pillow – Image processing 🖼️

Requests - HTTP requests for downloading generated images

Poetry – Dependency management 📦

dotenv – Environment variable management 🔑

🤖 Agentic Workflow & Agent Roles

The core of ImageCodeX is a multi-agent workflow orchestrated by LangGraph. Each agent is an expert in a specific creative or analytical task:

Agent Name	Role in Workflow
visual_analyst	Analyzes uploaded images for subject, style, mood, and composition.
prompt_engineer	Generates detailed text-to-image prompts based on the visual analysis.
inspector	Critiques the generated prompt for accuracy, clarity, and creative fit.
refiner	Refines prompts based on user feedback and inspector critique.
video_director	Converts image prompts and creative briefs into cinematic video prompts.
film_story_writer	Brainstorms multiple high-level story concepts from visual and textual input.
image_generator	Generates images using various models (GPT-4o, SDXL) via text-to-image or image-to-image.
script_expert	(Future) Expands story concepts into screenplay-style scenes and dialogue.
storyboard_artist	(Future) Generates visual storyboard descriptions for each scene.
🔄 How the Agentic Workflow Works

Visual Prompting (Stages 1 & 2)

visual_analyst analyzes the uploaded image.

prompt_engineer creates a text prompt.

inspector critiques the prompt.

refiner improves the prompt if user feedback is provided.

video_director uses the prompt and a creative brief to generate a video concept.

Narrative Engine (Stage 3)

film_story_writer builds multiple story concepts from the visual and user input.

Image Generation (Stage 4)

image_generator uses the final prompt (and optional reference image) to call the selected AI model (OpenAI or Replicate).

All agent steps are orchestrated as independent graphs (see src/graph/graphs.py), allowing for flexible, modular, and extensible workflows.

📂 File Structure
Generated code
ImageCodeX/
│
├── .env                  # API keys and environment variables 🔑
├── pyproject.toml        # Poetry project config 📦
├── run_app.py            # Main application entry point ▶️
│
└── src/
    │
    ├── app.py            # Main Streamlit app and controller 🌟
    │
    ├── agents/
    │   ├── film_story_writer.py
    │   ├── image_generator.py      # <-- ADDED
    │   ├── inspector.py
    │   ├── prompt_engineer.py
    │   ├── refiner.py
    │   ├── script_expert.py
    │   ├── storyboard_artist.py
    │   ├── video_director.py
    │   └── visual_analyst.py
    │
    ├── core/
    │   ├── prompts.py    # Prompt templates for agents 📝
    │   └── schemas.py    # Pydantic models for app state and data 📊
    │
    ├── graph/
    │   └── graphs.py     # Workflow graphs connecting agents 🔄
    │
    └── ui/
        ├── stage3_ui.py            # UI for narrative engine 📖
        ├── stage4_ui.py            # UI for image generation 🎨  <-- ADDED
        └── visual_prompting_ui.py  # UI for image/video prompt stages 🖼️🎥

🛠️ Installation

Requirements:

Python 3.10+ 🐍

Poetry 📦

Git 🌿

1. Clone the repository:

Generated sh
git clone https://github.com/Deepakkrishna-tech/ImageCodeX.git
cd ImageCodeX
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

2. Create the Environment File:
Create a file named .env in the root of the project directory and add your API keys:

Generated env
OPENAI_API_KEY="sk-..."
REPLICATE_API_TOKEN="r8_..."
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Env
IGNORE_WHEN_COPYING_END

3. Install Dependencies:
This command will create a virtual environment and install all necessary packages.

Generated sh
poetry install
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END

4. Run the App:
Use the unified run_app.py script. This works on Windows, macOS, and Linux.

Generated sh
poetry run streamlit run run_app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END
🌱 Extending & Contributing

Fork and clone the repo.

Add new agents or UI stages as needed.

Submit pull requests for improvements or bug fixes.

📜 License

MIT License. See LICENSE for details. 📄