import warnings
warnings.filterwarnings('ignore')

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from tools import save_as_docx

# Load the API key from .env file
load_dotenv()

# Tell CrewAI to use Gemini as the LLM
llm_model = LLM(
    model="gemini/gemini-flash-latest",
    api_key=os.getenv("GEMINI_API_KEY")
)

# =============================================================================
# AGENTS
# Each agent has 3 key properties:
#   role      → who the agent is (acts like a job title)
#   goal      → what the agent is trying to achieve
#   backstory → context that shapes how the agent thinks and behaves
# {topic} is a placeholder filled in when the crew runs
# =============================================================================

planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}. "
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    llm=llm_model,
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're an experienced writer that knows how to writing compelling and factual articles that inform readers. You are working on writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provided by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    llm=llm_model,
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization.",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices, "
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    llm=llm_model,
    tools=[save_as_docx],
    allow_delegation=False,
    verbose=True
)

# =============================================================================
# TASKS
# Each task has 3 key properties:
#   description     → the specific instructions the agent must follow
#   expected_output → what the final deliverable should look like
#   agent           → which agent is responsible for completing this task
# Tasks run sequentially, so the order matters — each builds on the last
# =============================================================================

plan = Task(
    description=(
        "1. Identify the key points to cover on {topic}. "
            "Prioritize a topic overview, key trends and players, "
            "and any recent notable news.\n"
        "2. Specify the target audience for {topic} — consider their "
            "interests, expected sentiment toward the topic, "
            "and any pain points that may be relevant.\n"
        "3. Draft a detailed outline the writer can use to build the article. "
            "Include an introduction, key points, and a call to action.\n"
        "4. Identify relevant SEO keywords and suggest credible sources "
            "the writer can cite, including links where possible."
    ),
    expected_output="A comprehensive content plan document in markdown format, "
                    "containing an outline, audience analysis, "
                    "SEO keywords, and a list of resources with links.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally throughout the post — "
            "it should not read as AI generated.\n"
        "3. Name sections and subtitles in an engaging, human manner "
            "that draws the reader in.\n"
        "4. Structure the post with an engaging introduction, "
            "an insightful body, and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and ensure the tone "
            "aligns with the brand's voice."
    ),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication. "
                    "Each section should have 2 or 3 paragraphs. "
                    "The writing should feel natural, human, and authoritative.",
    agent=writer,
)

edit = Task(
    description=(
        "1. Proofread the blog post for grammatical errors "
            "and spelling mistakes.\n"
        "2. Apply brand considerations — ensure the tone is professional, "
            "approachable, and consistent throughout.\n"
        "3. Validate the tone and content against the audience analysis "
            "provided in the content plan. "
            "The post should speak directly to the target audience's "
            "interests, sentiment, and pain points.\n"
        "4. Edit for conciseness and clarity — remove filler, "
            "tighten sentences, and ensure every paragraph earns its place.\n"
        "5. Ensure each section contains 2 to 3 paragraphs "
            "and the document is fully ready for publication."
    ),
    expected_output="A polished, publication-ready blog post in markdown format. "
                    "Each section should have 2 to 3 paragraphs. "
                    "Tone should be professional, clear, and audience-appropriate.",
    output_file="output/article.md",
    agent=editor,
)

# =============================================================================
# CREW
# Brings agents and tasks together into a single pipeline.
#   agents  → all agents participating in the crew
#   tasks   → all tasks in the order they should run
#   process → sequential means each task waits for the previous to finish
#   verbose → prints the full execution log so you can follow along
# =============================================================================

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=True
)

# =============================================================================
# KICKOFF
# Starts the crew. The inputs dict fills in all {topic} placeholders
# across every agent and task at runtime.
# =============================================================================

result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})
print(result)
