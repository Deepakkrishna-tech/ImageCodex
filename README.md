# 🎬 **ImageCodeX**

ImageCodeX is an advanced agentic, multi-agent-powered visual prompt engineering tool designed to transform static images into cinematic stories through the power of AI and human-in-the-loop collaboration. By combining cutting-edge artificial intelligence with intuitive creative workflows, ImageCodeX empowers users to craft compelling narratives, dynamic video prompts, and immersive story arcs—all tailored for creative storytelling.  

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)  
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](https://streamlit.io)  
[![Agent Orchestration](https://img.shields.io/badge/Agents-LangGraph-E86F2C)](https://langchain.com)  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)  

At its core, ImageCodeX leverages a sophisticated **multi-stage workflow** that guides users through every step of the creative process:  
- **Stage 1: Image Prompt Generation** – Analyze static images to generate detailed, model-ready text prompts enriched with artistic elements, style, mood, and composition insights.  
- **Stage 2: Cinematic Video Prompts** – Extend your visuals into dynamic video concepts by incorporating creative briefs such as mood, camera movements, and scene notes.  
- **Stage 3: Narrative Story Arcs** – Develop structured storylines and screenplay-style scenes, enabling you to bring your ideas to life with genre customization and professional polish.  

With its seamless integration of AI-driven insights and human creativity, ImageCodeX bridges the gap between imagination and execution—making it the ultimate tool for storytellers, content creators, and data scientists alike. Whether you're crafting a single scene or an entire cinematic experience, ImageCodeX provides the tools you need to turn your vision into reality.

---

## ✨ Features

- **Stage 1: Image Prompt Generation** 🖼️  
  - Upload an image and receive a detailed, model-ready text-to-image prompt.  
  - Automated analysis of artistic elements, style, mood, and composition.  
  - Prompt critique and refinement with user feedback.  

- **Stage 2: Video Prompt Generation** 🎥  
  - Extend your image into a cinematic video prompt.  
  - Provide creative briefs (mood, camera movement, notes) for tailored video prompt output.  

- **Stage 3: Narrative Engine** 📖  
  - Turn your visuals and ideas into structured story arcs and screenplay scenes.  
  - Supports genre and mood customization.  

- **Developer Tools** 🔧  
  - Dev sidebar for inspecting and clearing app state.  
  - Modular, agent-based architecture for easy extension.  

---

## 🎥 Demo

![ImageCodeX UI Screenshot](docs/screenshot.png)  
<!-- Replace with your actual screenshot path -->

[![Watch the demo](https://img.youtube.com/vi/your_video_id/0.jpg)](https://youtu.be/your_video_id)  
<!-- Replace with your actual YouTube video link -->

---

## 🚀 Usage

1. **Stage 1: Image Prompt** 🖼️  
   - Upload an image (PNG/JPG).  
   - Click "Analyze and Generate Prompt".  
   - Review the generated prompt and critique.  
   - Optionally, refine the prompt with feedback.  

2. **Stage 2: Video Prompt** 🎥  
   - Upload an image for video.  
   - Enter moods, camera movement, and notes.  
   - Click "Generate Video Prompt".  
   - Review the cinematic video prompt.  

3. **Stage 3: Narrative Engine** 📖  
   - Provide an image, idea, genre, and mood.  
   - Generate a story arc and screenplay scenes.  

---

## 💻 Tech Stack

- **Python 3.13+** 🐍  
- **Streamlit** – Interactive web UI 🌟  
- **Pydantic** – Data validation and modeling 📊  
- **LangChain / LangGraph** – Agentic workflow orchestration 🤖  
- **OpenAI API** (via `langchain-openai`) – LLM-powered agents 🧠  
- **Pillow** – Image processing 🖼️  
- **Poetry** – Dependency management 📦  
- **dotenv** – Environment variable management 🔑  

---

## 🤖 Agentic Workflow & Agent Roles

The core of ImageCodeX is a **multi-agent workflow** orchestrated by LangGraph. Each agent is an expert in a specific creative or analytical task:

| Agent Name            | Role in Workflow                                                                 |
|-----------------------|----------------------------------------------------------------------------------|
| **visual_analyst**    | Analyzes uploaded images for subject, style, mood, lighting, and composition.    |
| **prompt_engineer**   | Generates detailed text-to-image prompts based on the visual analysis.           |
| **inspector**         | Critiques the generated prompt for accuracy, clarity, and creative fit.          |
| **refiner**           | Refines prompts based on user feedback and inspector critique.                   |
| **video_director**    | Converts image prompts and creative briefs into cinematic video prompts.          |
| **film_story_writer** | Crafts narrative arcs and story beats from visual and textual input.             |
| **script_expert**     | Expands story arcs into screenplay-style scenes and dialogue.                    |
| **storyboard_artist** | Generates visual storyboard descriptions for each scene.                         |
| **utils**             | Shared utility functions for agents.                                             |

### 🔄 How the Agentic Workflow Works

- **Stage 1: Image Prompting** 🖼️  
  1. **visual_analyst** analyzes the uploaded image.  
  2. **prompt_engineer** creates a text prompt for image generation.  
  3. **inspector** critiques the prompt.  
  4. **refiner** improves the prompt if user feedback is provided.  

- **Stage 2: Video Prompting** 🎥  
  1. **video_director** uses the image prompt and a creative brief to generate a cinematic video prompt.  

- **Stage 3: Narrative Engine** 📖  
  1. **film_story_writer** builds a story arc from the visual and user input.  
  2. **script_expert** writes screenplay scenes.  
  3. **storyboard_artist** creates visual descriptions for each scene.  

All agent steps are orchestrated as a **graph** (see `graphs.py`), allowing for flexible, modular, and extensible workflows.  

---

## 🔧 Key Code Concepts

- **AppController**: Manages app state, workflow execution, and reruns.  
- **Schemas**: All data (prompts, critiques, briefs, narrative) are Pydantic models.  
- **UI**: Streamlit-based, modular per stage.  
- **Workflows**: Each stage is a graph of agentic steps (see `graph/graphs.py`).
  
---

## 📂 File Structure

```
visionprompt-agent/
│
├── .env                  # API keys and environment variables 🔑
├── pyproject.toml        # Poetry project config 📦
├── run_app.py            # Shortcut to run the app ▶️
├── test_api.py           # API test script 🧪
│
└── src/
    │
    ├── app.py            # Main Streamlit app and controller 🌟
    │
    ├── agents/           # All agent modules (see below) 🤖
    │   ├── film_story_writer.py
    │   ├── inspector.py
    │   ├── prompt_engineer.py
    │   ├── refiner.py
    │   ├── script_expert.py
    │   ├── storyboard_artist.py
    │   ├── utils.py
    │   ├── video_director.py
    │   ├── visual_analyst.py
    │   └── __init__.py
    │
    ├── core/
    │   ├── prompts.py    # Prompt templates for agents 📝
    │   ├── schemas.py    # Pydantic models for app state and data 📊
    │   └── __init__.py
    │
    ├── graph/
    │   ├── graphs.py     # Workflow graphs connecting agents 🔄
    │   └── __init__.py
    │
    └── ui/
        ├── stage3_ui.py  # UI for narrative engine 📖
        ├── visual_prompting_ui.py # UI for image/video prompt stages 🖼️🎥
        └── __init__.py
```

---

## 🛠️ Installation

**Requirements:**  
- Python 3.13+ 🐍  
- [Poetry](https://python-poetry.org/) 📦  
- Git 🌿  

**Clone and install dependencies:**  
```sh
git clone https://github.com/Deepakkrishna-tech/ImageCodex.git  
cd ImageCodex  
poetry install  
```

**Run the app:**  
```sh
# On Windows (PowerShell)  
$env:PYTHONPATH = "."  
poetry run streamlit run src/app.py  

# On Linux/macOS  
PYTHONPATH=. poetry run streamlit run src/app.py  
```

---

## 🌱 Extending & Contributing

- Fork and clone the repo.  
- Add new agents or UI stages as needed.  
- Submit pull requests for improvements or bug fixes.  

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details. 📄  

---
