# AI Agent

A Gemini-powered CLI coding assistant that can inspect, edit, and run code inside a sandboxed working directory — currently pointed at a small Python `calculator/` project it can read, modify, and test.

Ask it something like "why does `3 + 5` fail?" and it will list the files, read the relevant ones, and either explain the bug or fix it directly, calling tools itself in a loop rather than just replying with a suggestion.

## How it works

- `main.py` sends your prompt to Gemini (`gemini-2.0-flash-001`) along with a system prompt (`prompts.py`) and a set of tool declarations.
- If Gemini responds with a function call instead of a final answer, the agent runs that tool locally, feeds the result back, and lets Gemini decide the next step — up to 20 turns per prompt, so it can chain multiple tool calls (e.g. list files, then read one, then fix it) before giving a final answer.
- Every tool call is scoped to a single `working_directory` (currently `./calculator`, set in `call_function.py`). Each tool resolves its target path and checks it still starts with that directory before touching anything — so the model can't read, write, or execute a file outside the sandbox, even via `../` or an absolute path.

## Tools available to the agent

| Tool | What it does |
| --- | --- |
| `get_files_info` | Lists files/directories in a path, with sizes |
| `get_file_content` | Reads a file's contents |
| `write_file` | Writes/overwrites a file, creating parent directories if needed |
| `run_python_file` | Runs a `.py` file with optional args and returns stdout/stderr/exit code (30s timeout) |

## Setup

Install dependencies:

```sh
uv sync
```

Create a local environment file from the template:

```sh
cp .env.example .env
```

Then edit `.env` and set your Gemini API key:

```sh
GEMINI_API_KEY="your_api_key_here"
```

Never commit `.env` or any real API key.

## Usage

**One-shot** — run a single prompt and exit (useful for scripting):

```sh
uv run main.py "what files are in the calculator project?"
```

**Interactive** — run with no prompt to drop into a REPL that keeps conversation history across turns, so you can ask follow-ups without losing context:

```sh
uv run main.py
```

```
AI Code Assistant (interactive mode)
Type a prompt, or "exit"/"quit" to stop.

> what does calculator/main.py do?
...
> now add a subtraction test for it
...
> exit
```

Add `--verbose` to either mode to print tool calls and token usage:

```sh
uv run main.py "what files are in the calculator project?" --verbose
```

## Note on screenshots

This README doesn't include live sample output yet — the API key currently configured in dev has hit its free-tier quota. The interactive loop itself has been verified end-to-end (prompt → error → retry loop → clean exit); once a key with quota is in place, real transcripts/screenshots should replace this section.
