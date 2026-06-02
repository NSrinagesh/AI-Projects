# AI Projects

A collection of AI agent projects and course work, built using [CrewAI](https://www.crewai.com/) as part of the DeepLearning.AI course on multi-agent systems. Each project demonstrates a different use case for orchestrating autonomous AI agents that collaborate to complete complex tasks.

## Projects

| Project | Description |
|--------|-------------|
| [L2 - Research & Write Article](crews/L2-research-write-article/) | A 3-agent crew that researches a topic, writes a blog post, and edits it for publication |

## Setup

Each project has its own folder under `crews/`. To run any project:

1. **Clone the repo**
   ```bash
   git clone https://github.com/NSrinagesh/AI-Projects.git
   cd AI-Projects
   ```

2. **Create a virtual environment with Python 3.13**
   ```bash
   py -3.13 -m venv .venv
   .venv\Scripts\Activate.ps1   # Windows
   source .venv/bin/activate    # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install crewai crewai_tools langchain_community "crewai[google-genai]"
   ```

4. **Add your API key**  
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_key_here
   ```

5. **Run a crew**
   ```bash
   cd crews/L2-research-write-article
   python crew.py
   ```

## Requirements

- Python 3.10–3.13
- Gemini API key (free tier available at [aistudio.google.com](https://aistudio.google.com))
