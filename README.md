# 🧩 VisionPrompt Agent

  <!-- Optional: Create a short GIF of your app and upload it to a site like Imgur, then paste the link here. -->

**VisionPrompt Agent is an advanced, agentic visual prompt engineer designed to reverse-engineer images into detailed, structured, and highly effective prompts for generative AI models like Midjourney, SDXL, and DALL-E 3.**

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)](https://streamlit.io)
[![Agent Orchestration](https://img.shields.io/badge/Agents-LangGraph-E86F2C)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

<!-- Replace '#' with your deployed app's URL -->
**[▶️ View Live Demo](#)**

---

## ✨ Core Features

This tool leverages a multi-agent system built with LangGraph to provide a sophisticated analysis and prompt generation workflow:

*   **Image Upload**: Accepts `.jpg`, `.png`, and `.webp` images.
*   **Deep Visual Analysis**: A `VisualAnalystAgent` deconstructs the image into structured JSON, analyzing technical specs, composition, colors, style, and more.
*   **Expert Prompt Synthesis**: A `PromptEngineerAgent` takes the structured analysis and a user-defined style to craft a cohesive, high-quality prompt optimized for AI image generators.
*   **Iterative Refinement**: A `RefinementAgent` allows you to conversationally edit and improve the generated prompt with natural language instructions.
*   **Prompt History**: Keeps track of every version of your prompt throughout a session for easy comparison and reference.

## 🛠️ Tech Stack

This project is built with a modern, 2025-ready open-source tech stack:

*   **Frontend**: [Streamlit](https://streamlit.io/) for a fast, interactive web UI.
*   **Agent Framework**: [LangGraph](https://github.com/langchain-ai/langgraph) for building robust, stateful, and modular multi-agent workflows.
*   **LLM Integration**: [LangChain](https://www.langchain.com/) (`langchain_openai`) to connect with powerful multimodal models like GPT-4o.
*   **Environment Management**: [Poetry](https://python-poetry.org/) for deterministic dependency management and packaging.
*   **Image Processing**: [Pillow](https://python-pillow.org/) for handling image data.
*   **Secrets Management**: `python-dotenv` for secure handling of API keys.

## 🚀 Getting Started

Follow these steps to set up and run the VisionPrompt Agent locally.

### 1. Prerequisites

*   Python 3.10+
*   [Poetry](https://python-poetry.org/docs/#installation) installed on your system.
*   An [OpenAI API Key](https://platform.openai.com/api-keys).

### 2. Installation

First, clone the repository to your local machine:
```bash
git clone https://github.com/your-username/visionprompt-agent.git
cd visionprompt-agent
Use code with caution.
Markdown
Next, install the required dependencies using Poetry. This will create a virtual environment and install all packages specified in pyproject.toml.

Generated bash
poetry install
Use code with caution.
Bash
3. Configure Environment Variables
The application requires an OpenAI API key to function.

Find the .env.example file in the root directory and rename it to .env:

Generated bash
mv .env.example .env
Use code with caution.
Bash
If you don't have an example file, simply create a new file named .env.

Open the .env file and add your OpenAI API key:

Generated code
# .env
OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
Use code with caution.
4. Run the Application
Once the installation and configuration are complete, you can run the Streamlit application from the project's root directory:

Generated bash
poetry run streamlit run src/app.py
Use code with caution.
Bash
The application should now be running and accessible in your web browser, typically at http://localhost:8501.

📖 How to Use
Upload an Image: Drag and drop an image file or use the "Browse files" button in the sidebar.

Define a Style: Optionally, enter a target style you want the final prompt to reflect (e.g., "8-bit pixel art", "cinematic film still", "minimalist line art").

Analyze: Click the "✨ Analyze and Generate Prompt" button. The agentic workflow will execute, and a detailed prompt will appear.

Refine: Type a natural language instruction into the "Refine Your Prompt" box (e.g., "make it a rainy day", "add a sense of mystery"). Click the "🔄 Refine Prompt" button to get an updated version.

Review: The "Prompt History" expander shows all previous versions of your prompt for easy tracking.

📝 License
This project is licensed under the MIT License. See the LICENSE file for details.