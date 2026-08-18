# agent-1

A code-executing AI agent with a chat UI, built on [smolagents](https://github.com/huggingface/smolagents) and [Gradio](https://www.gradio.app/). The agent reasons in a Thought → Code → Observation loop, writing and running actual Python at each step to work toward an answer.

Based on the starter template from Hugging Face's [Agents Course](https://huggingface.co/learn/agents-course).

## What it can do

- **Search the web** — looks things up via DuckDuckGo
- **Read webpages** — visits a URL and pulls out its content as readable text
- **Check the time** — reports the current time in any timezone
- **Reason step by step** — plans, writes code, checks the result, and adjusts before giving a final answer

The model backing it is `Qwen/Qwen2.5-Coder-32B-Instruct`, served through Hugging Face's Inference API.

## Setup

**Prerequisites:** Python 3.10+, and a free [Hugging Face account](https://huggingface.co/join) with an [access token](https://huggingface.co/settings/tokens).

1. Clone the repo:
   ```bash
   git clone https://github.com/soopark723/agent-1.git
   cd agent-1
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate # macOS/Linux
   pip install -r requirements.txt
   ```

3. Add your Hugging Face token. Create a `.env` file in this folder:
   ```
   HF_TOKEN=hf_your_token_here
   ```

## Usage

```bash
python app.py
```

This starts a local Gradio server (usually at `http://127.0.0.1:7860`) and also opens a temporary public link, since the app launches with `share=True`. Open either link in a browser to chat with the agent.

## Project structure

```
agent-1/
├── app.py              # Entry point — builds the agent and launches the UI
├── Gradio_UI.py         # Chat interface wrapper around the agent
├── model.py             # Alternate local-model config (Ollama, unused by default)
├── prompts.yaml          # System prompt / reasoning templates
├── requirements.txt      # Python dependencies
├── agent.json            # Exported agent config snapshot (not used at runtime)
└── tools/
    ├── final_answer.py     # Returns the agent's final answer
    ├── web_search.py        # DuckDuckGo search tool
    └── visit_webpage.py     # Webpage-reading tool
```

## Notes

- The first run downloads an image-generation tool from the Hugging Face Hub, so it needs an internet connection.
- Since `share=True` is set in `Gradio_UI.py`, anyone with the temporary public link can interact with the agent (and use your token's quota) while it's running. Set `share=False` there if you'd rather keep it local-only.
