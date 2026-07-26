import os
import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent


# 1. Load environment variables (.env)
load_dotenv()

# 2. Configure Logfire and instrument Pydantic AI
# Logfire automatically reads LOGFIRE_TOKEN from the environment
logfire.configure()
logfire.instrument_pydantic_ai()

# 3. Initialize the Agent (using Gemini Pro)
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt="You are a helpful assistant. Use tools when looking up instructions or guides."
)

# 4. Define a search/retrieval tool to trigger a tool span
@agent.tool_plain
def search_docs(query: str) -> str:
    """Search documentation for local software setup guides."""
    print(f"\n[Tool Executed] Searching docs for: {query}")
    if "ollama" in query.lower():
        return (
            "To run Ollama locally:\n"
            "1. Download it from https://ollama.com\n"
            "2. Install it on your OS (macOS, Linux, or Windows).\n"
            "3. Run 'ollama run llama3' or 'ollama run qwen2.5-coder' in your terminal."
        )
    return "No documentation found."

# 5. Run the query
if __name__ == "__main__":
    prompt = "How do I run Ollama locally?"
    print(f"User Prompt: {prompt}\n")

    # This call generates the full trace with all 5 spans in Logfire
    result = agent.run_sync(prompt)

    print("\n--- Final Agent Response ---")
    print(result.output)