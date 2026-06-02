# L2 - Research & Write Article

A multi-agent crew that autonomously researches a topic and produces a publication-ready blog post. Built with [CrewAI](https://www.crewai.com/) and powered by Google Gemini.

## What It Does

Three specialized agents collaborate in sequence:

| Agent | Role | Output |
|-------|------|--------|
| **Content Planner** | Researches the topic, identifies the target audience, drafts an outline, and gathers SEO keywords and source links | Content plan in markdown |
| **Content Writer** | Uses the plan to write a compelling, human-sounding blog post | Draft article in markdown |
| **Editor** | Proofreads, validates tone against the audience analysis, edits for clarity, and saves the final article as a Word document | `output/article.docx` |

## Files

```
L2-research-write-article/
├── crew.py       # Agents, tasks, crew definition, and kickoff
├── tools.py      # Custom tool: saves the final article as a .docx file
├── output/       # Final article saved here after the crew runs
└── README.md
```

## Usage

From the repo root, activate the virtual environment then run:

```bash
cd crews/L2-research-write-article
python crew.py
```

To change the topic, edit the `inputs` in `crew.py`:

```python
result = crew.kickoff(inputs={"topic": "Your Topic Here"})
```

## Output

The final edited article is saved to `output/article.docx`, formatted as a Word document ready for publication.
