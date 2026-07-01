import os
import sys
import argparse
from dotenv import load_dotenv
import anthropic
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not found. Make sure you have a .env file "
            "with ANTHROPIC_API_KEY='your_key_here'"
        )

    parser = argparse.ArgumentParser(
        description="A toy AI coding agent powered by Claude"
    )
    parser.add_argument("user_prompt", type=str, help="The task or question for the agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    client = anthropic.Anthropic(api_key=api_key)

    messages = [
        {"role": "user", "content": args.user_prompt}
    ]

    for _ in range(20):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8096,
            system=system_prompt,
            tools=available_functions,
            messages=messages,
        )

        if args.verbose:
            print(f"Input tokens: {response.usage.input_tokens}")
            print(f"Output tokens: {response.usage.output_tokens}")

        # أضف رد الـ Claude للـ history
        messages.append({"role": "assistant", "content": response.content})

        # لو stop_reason = "end_turn" يعني جواب نهائي بدون tool calls
        if response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            print("Final response:")
            print(final_text)
            return

        # لو stop_reason = "tool_use" يعني في function calls
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = call_function(block.name, block.input, args.verbose)

                    if args.verbose:
                        print(f"-> {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # أضف نتائج الـ tools للـ history
            messages.append({"role": "user", "content": tool_results})

        else:
            # stop_reason غير متوقع
            print(f"Unexpected stop reason: {response.stop_reason}")
            sys.exit(1)

    print("Error: Maximum iterations reached without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
