# 🎬 ImageCodeX

ImageCodeX is an advanced agentic, multi-agent-powered visual engineering tool designed to transform static images and text prompts into a complete creative workflow. By combining cutting-edge artificial intelligence with intuitive human-in-the-loop collaboration, ImageCodeX empowers users to craft compelling narratives, dynamic video prompts, and high-quality AI-generated images.

![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)
![Agents](https://img.shields.io/badge/Agents-LangGraph-E86F2C)
![License](https://img.shields.io/badge/License-MIT-green.svg)

At its core, ImageCodeX leverages a sophisticated multi-stage workflow that guides users through every step of the creative process:

-   **Stage 1 & 2: Visual Prompt Engineering** – Analyze static images to generate and refine detailed text prompts for image and video generation.
-   **Stage 3: Cinematic Narrative Engine** – Transform an image into a cinematic "Before/After" scene with genre control and reference-based inspiration from live web searches.
-   **Stage 4: AI Image Generation** – Close the creative loop by generating high-quality images directly from your engineered prompts.

With its seamless integration of AI-driven insights and human creativity, ImageCodeX bridges the gap between imagination and execution—making it the ultimate tool for storytellers, content creators, and AI enthusiasts.

## ✨ Features

### Stage 1 & 2: Visual Prompting 🖼️ 🎥
- Upload an image to receive a detailed, model-ready text-to-image prompt.
- Automated analysis of artistic elements, style, mood, and composition.
- Prompt critique and refinement with user feedback.

### Stage 3: Cinematic Narrative Engine 📖 🎬
- **Before & After Scenes:** Generates a cinematic "Before Scene" (what just happened) and "After Scene" (what happens next) from a single image and idea.
- **Genre & Mood Control:** Shape your narrative with specific genres (e.g., *Dark Fantasy*) and moods (e.g., *Somber & Reflective*).
- **Three Powerful Inspiration Modes:**
    - `🧠 AI Imagination`: Purely AI-driven creativity.
    - `🎞️ Inspired By`: Draws thematic and stylistic inspiration from a reference story (e.g., "Narnia," "Avengers").
    - `📚 Original Story`: Fetches key factual motifs from a reference (e.g., "Mahabharata") to ensure accuracy.
- **Live Web Search:** Uses the **Tavily API** to gather real-time context for the "Inspired By" and "Original Story" modes.
- **Dual-Prompt Output:** Generates two distinct, high-quality image prompts, one for the "Before Scene" and one for the "After Scene".

### Stage 4: AI Image Generation 🎨
- **Multi-Model Support:** Generate images using GPT-4o, Stable Diffusion XL, and Kandinsky 2.2.
- **Text-to-Image:** Create visuals directly from your crafted prompts.
- **Image-to-Image & Variations:** Provide an optional reference image to guide generation.

### Developer Tools 🔧
- **Live State Inspector:** A sidebar for inspecting and clearing the application's real-time state.
- **Modular Architecture:** Built with LangGraph for easy extension and agent management.

## 🎥 Demo

![Screenshot of ImageCodeX Stage 3 UI](docs/screenshot_stage3.png)
<!-- TODO: Replace with an updated screenshot showing the new Stage 3 UI with a generated Before/After scene. -->

[![YouTube Video Demo](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
<!-- TODO: Replace with your actual YouTube video link -->

## 🚀 Usage

### Visual Prompting Tab (Stages 1 & 2)
1.  **Image Prompt:** Upload an image and click "Analyze and Generate Prompt".
2.  **Video Prompt:** Provide a creative brief and click "Generate Video Prompt".

### Cinematic Narrative Engine Tab (Stage 3)
1.  Upload an image and provide a short description of the core moment (e.g., "A secret is discovered.").
2.  Select a **Genre** and **Mood**.
3.  Choose your **Inspiration Mode** (`AI Imagination`, `Inspired By`, or `Original Story`).
4.  If using inspiration, provide a **Reference Story** (e.g., "Spiderman").
5.  Click `🎬 Generate Cinematic Scene` and review the "Before/After" scenes and their corresponding image prompts.
6.  Click `🔄 Start New Scene` to unlock the UI and begin again.

### Image Generation Tab (Stage 4) 🎨
1.  The prompts from Stage 3 can be copied and pasted here.
2.  Select your desired AI model and aspect ratio.
3.  Click "Generate Image" and review the result.

## 💻 Tech Stack

-   **Python 3.10+** 🐍
-   **Streamlit** – Interactive web UI 🌟
-   **Pydantic** – Data validation and modeling 📊
-   **LangChain / LangGraph** – Agentic workflow orchestration 🤖
-   **OpenAI & Replicate APIs** – Powering LLM and image generation agents 🧠
-   **Tavily API** – For live web search to provide reference context 🌐
-   **Poetry** – Dependency management 📦
-   **dotenv** – Environment variable management 🔑

## 🤖 Agentic Workflow & Agent Roles

The core of ImageCodeX is a multi-agent workflow orchestrated by LangGraph. The new Stage 3 workflow is highly conditional and context-aware.

### Stage 3: Cinematic Narrative Agents

| Agent Name | Role in Workflow |
| :--- | :--- |
| `reference_agent` | **(Live)** Uses Tavily Search to fetch factual motifs and plot points for the "Original Story" mode. |
| `inspiration_agent` | **(Live)** Uses Tavily Search to find thematic and stylistic inspiration for the "Inspired By" mode. |
| `context_engineer` | Fuses the user's idea, genre, mood, and any gathered inspiration into a coherent creative brief. |
| `storytelling_agent` | The "Master Storyteller." Uses GPT-4o to synthesize the full context into the final "Before/After" scenes and image prompts. |

### How the Cinematic Workflow Works

The Stage 3 graph is orchestrated by an `inspiration_router` that directs the flow based on the user's selected mode:
1.  **If "Original Story":** The flow starts with the `reference_agent` to gather facts.
2.  **If "Inspired By":** The flow starts with the `inspiration_agent` to gather themes.
3.  **If "AI Imagination":** The flow skips the search agents and goes directly to the next step.

All paths converge on the `context_engineer`, which prepares the final brief for the `storytelling_agent` to generate the output.

## 🛠️ Installation

**Requirements:**
-   Python 3.10+ 🐍
-   Poetry 📦
-   Git 🌿

**1. Clone the repository:**
```sh
git clone https://github.com/Deepakkrishna-tech/ImageCodeX.git
cd ImageCodeX

2. Create the Environment File:
Create a file named .env in the root of the project directory and add your API keys. The TAVILY_API_KEY is now required for Stage 3.

Of course. Creating a comprehensive and updated `README.md` is a critical final step to reflect all the amazing work you've done. I will generate a new README inspired by your previous version, but with all the new features, agents, and technical requirements fully documented.

This updated README will explain the new Stage 3 Cinematic Narrative Engine, the inspiration modes, the new agents, the updated tech stack, and the revised installation instructions.

Here is the complete, updated `README.md` file. You can copy the entire content from the code block below and paste it directly into your `README.md` file.

```markdown
# 🎬 ImageCodeX

ImageCodeX is an advanced agentic, multi-agent-powered visual engineering tool designed to transform static images and text prompts into a complete creative workflow. By combining cutting-edge artificial intelligence with intuitive human-in-the-loop collaboration, ImageCodeX empowers users to craft compelling narratives, dynamic video prompts, and high-quality AI-generated images.

![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)
![Agents](https://img.shields.io/badge/Agents-LangGraph-E86F2C)
![License](https://img.shields.io/badge/License-MIT-green.svg)

At its core, ImageCodeX leverages a sophisticated multi-stage workflow that guides users through every step of the creative process:

-   **Stage 1 & 2: Visual Prompt Engineering** – Analyze static images to generate and refine detailed text prompts for image and video generation.
-   **Stage 3: Cinematic Narrative Engine** – Transform an image into a cinematic "Before/After" scene with genre control and reference-based inspiration from live web searches.
-   **Stage 4: AI Image Generation** – Close the creative loop by generating high-quality images directly from your engineered prompts.

With its seamless integration of AI-driven insights and human creativity, ImageCodeX bridges the gap between imagination and execution—making it the ultimate tool for storytellers, content creators, and AI enthusiasts.

## ✨ Features

### Stage 1 & 2: Visual Prompting 🖼️ 🎥
- Upload an image to receive a detailed, model-ready text-to-image prompt.
- Automated analysis of artistic elements, style, mood, and composition.
- Prompt critique and refinement with user feedback.

### Stage 3: Cinematic Narrative Engine 📖 🎬
- **Before & After Scenes:** Generates a cinematic "Before Scene" (what just happened) and "After Scene" (what happens next) from a single image and idea.
- **Genre & Mood Control:** Shape your narrative with specific genres (e.g., *Dark Fantasy*) and moods (e.g., *Somber & Reflective*).
- **Three Powerful Inspiration Modes:**
    - `🧠 AI Imagination`: Purely AI-driven creativity.
    - `🎞️ Inspired By`: Draws thematic and stylistic inspiration from a reference story (e.g., "Narnia," "Avengers").
    - `📚 Original Story`: Fetches key factual motifs from a reference (e.g., "Mahabharata") to ensure accuracy.
- **Live Web Search:** Uses the **Tavily API** to gather real-time context for the "Inspired By" and "Original Story" modes.
- **Dual-Prompt Output:** Generates two distinct, high-quality image prompts, one for the "Before Scene" and one for the "After Scene".

### Stage 4: AI Image Generation 🎨
- **Multi-Model Support:** Generate images using GPT-4o, Stable Diffusion XL, and Kandinsky 2.2.
- **Text-to-Image:** Create visuals directly from your crafted prompts.
- **Image-to-Image & Variations:** Provide an optional reference image to guide generation.

### Developer Tools 🔧
- **Live State Inspector:** A sidebar for inspecting and clearing the application's real-time state.
- **Modular Architecture:** Built with LangGraph for easy extension and agent management.

## 🎥 Demo

![Screenshot of ImageCodeX Stage 3 UI](docs/screenshot_stage3.png)
<!-- TODO: Replace with an updated screenshot showing the new Stage 3 UI with a generated Before/After scene. -->

[![YouTube Video Demo](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
<!-- TODO: Replace with your actual YouTube video link -->

## 🚀 Usage

### Visual Prompting Tab (Stages 1 & 2)
1.  **Image Prompt:** Upload an image and click "Analyze and Generate Prompt".
2.  **Video Prompt:** Provide a creative brief and click "Generate Video Prompt".

### Cinematic Narrative Engine Tab (Stage 3)
1.  Upload an image and provide a short description of the core moment (e.g., "A secret is discovered.").
2.  Select a **Genre** and **Mood**.
3.  Choose your **Inspiration Mode** (`AI Imagination`, `Inspired By`, or `Original Story`).
4.  If using inspiration, provide a **Reference Story** (e.g., "Spiderman").
5.  Click `🎬 Generate Cinematic Scene` and review the "Before/After" scenes and their corresponding image prompts.
6.  Click `🔄 Start New Scene` to unlock the UI and begin again.

### Image Generation Tab (Stage 4) 🎨
1.  The prompts from Stage 3 can be copied and pasted here.
2.  Select your desired AI model and aspect ratio.
3.  Click "Generate Image" and review the result.

## 💻 Tech Stack

-   **Python 3.10+** 🐍
-   **Streamlit** – Interactive web UI 🌟
-   **Pydantic** – Data validation and modeling 📊
-   **LangChain / LangGraph** – Agentic workflow orchestration 🤖
-   **OpenAI & Replicate APIs** – Powering LLM and image generation agents 🧠
-   **Tavily API** – For live web search to provide reference context 🌐
-   **Poetry** – Dependency management 📦
-   **dotenv** – Environment variable management 🔑

## 🤖 Agentic Workflow & Agent Roles

The core of ImageCodeX is a multi-agent workflow orchestrated by LangGraph. The new Stage 3 workflow is highly conditional and context-aware.

### Stage 3: Cinematic Narrative Agents

| Agent Name | Role in Workflow |
| :--- | :--- |
| `reference_agent` | **(Live)** Uses Tavily Search to fetch factual motifs and plot points for the "Original Story" mode. |
| `inspiration_agent` | **(Live)** Uses Tavily Search to find thematic and stylistic inspiration for the "Inspired By" mode. |
| `context_engineer` | Fuses the user's idea, genre, mood, and any gathered inspiration into a coherent creative brief. |
| `storytelling_agent` | The "Master Storyteller." Uses GPT-4o to synthesize the full context into the final "Before/After" scenes and image prompts. |

### How the Cinematic Workflow Works

The Stage 3 graph is orchestrated by an `inspiration_router` that directs the flow based on the user's selected mode:
1.  **If "Original Story":** The flow starts with the `reference_agent` to gather facts.
2.  **If "Inspired By":** The flow starts with the `inspiration_agent` to gather themes.
3.  **If "AI Imagination":** The flow skips the search agents and goes directly to the next step.

All paths converge on the `context_engineer`, which prepares the final brief for the `storytelling_agent` to generate the output.

## 🛠️ Installation

**Requirements:**
-   Python 3.10+ 🐍
-   Poetry 📦
-   Git 🌿

**1. Clone the repository:**
```sh
git clone https://github.com/Deepakkrishna-tech/ImageCodeX.git
cd ImageCodeX
```

**2. Create the Environment File:**
Create a file named `.env` in the root of the project directory and add your API keys. The `TAVILY_API_KEY` is now required for Stage 3.
```env
# For OpenAI models like GPT-4o
OPENAI_API_KEY="sk-..."

# For Replicate models (e.g., SDXL)
REPLICATE_API_TOKEN="r8_..."

# For the Tavily web search tool (used in Stage 3)
TAVILY_API_KEY="tvly-..."
```

**3. Install Dependencies:**
This command will create a virtual environment and install all necessary packages, including the new `langchain-tavily` library.
```sh
poetry install
```

**4. Run the App:**
Use the unified `run_app.py` script. This works on Windows, macOS, and Linux.
```sh
poetry run streamlit run run_app.py
```

## 🌱 Extending & Contributing

-   Fork and clone the repo.
-   Add new agents or UI stages as needed.
-   Submit pull requests for improvements or bug fixes.

## 📜 License

MIT License. See `LICENSE` for details. 📄
