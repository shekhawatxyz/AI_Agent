import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set. Create a .env file from .env.example.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    if args:
        # One-shot mode: `python main.py "prompt"` runs a single prompt and
        # exits. Useful for scripting/piping since there's no interactive
        # session to manage.
        run_prompt(client, " ".join(args), verbose)
        return

    # Interactive mode: `python main.py` with no prompt drops into a REPL.
    # Unlike one-shot mode, `messages` here lives outside the loop, so
    # earlier turns stay in context for follow-up prompts.
    print("AI Code Assistant (interactive mode)")
    print('Type a prompt, or "exit"/"quit" to stop.\n')

    messages = []
    while True:
        try:
            user_prompt = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D / Ctrl+C exits the REPL instead of crashing.
            print()
            break

        if not user_prompt:
            continue
        if user_prompt.lower() in ("exit", "quit"):
            break

        messages.append(
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        )
        generate_content(client, messages, verbose)


def run_prompt(client, user_prompt, verbose):
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    # A single user prompt can take several back-and-forth turns with the
    # model: it calls a tool, we run it and hand back the result, it may
    # call another tool, and so on. The cap at 20 turns exists so a model
    # that keeps calling tools without ever settling on a final answer
    # can't loop forever.
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            # Append the model's turn (text and/or function calls) so the
            # next request in this loop has full context of what happened.
            for candidate in response.candidates:
                messages.append(candidate.content)
            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

            some_list = []
            if response.function_calls:
                # The model asked to run one or more tools. Execute each one
                # locally (call_function.py enforces the working-directory
                # sandbox) and collect the results to send back.
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception(
                            "Function call did not return expected response"
                        )
                    some_list.append(function_call_result.parts[0])
                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )
                # Function results go back in as a "user" turn — that's the
                # Gemini API's convention for feeding tool output back to
                # the model, not an actual user message.
                messages.append(types.Content(role="user", parts=some_list))
            if not response.function_calls and response.text:
                # No more tool calls and there's text: the model is done.
                print(response.text)
                break
        except Exception as e:
            print(f"Error: {e}")
            return


if __name__ == "__main__":
    main()
