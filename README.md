# AI Agent

A one-shot Gemini-powered CLI code assistant for a sandboxed Python calculator
project. The assistant can inspect files, run Python files, and write files only
inside the `calculator/` directory.

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

Run the assistant with a prompt:

```sh
uv run python main.py "what files are in the calculator project?"
```

Add `--verbose` to print tool calls and token usage:

```sh
uv run python main.py "what files are in the calculator project?" --verbose
```
