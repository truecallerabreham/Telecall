"""Test LangGraph agent with mock tool - Milestone 2.3: Agent responds to plan queries."""

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from telecomcall.config import settings
from telecomcall.agent.tools.plan_search import search_plan_mock_tool

DEFAULT_SYSTEM_PROMPT = """
Your name is Lisa, and you work for TelecomCo mobile carrier company.
Your task is to provide information about mobile plans using the `search_plan_mock_tool`.
Don't use asterisks or emojis, as you are engaged in a phone call. Just return short and informative responses.
""".strip()


def test_agent():
    """Create a LangGraph agent and test it with a plan query."""
    llm = ChatGroq(
        model=settings.groq.model,
        api_key=settings.groq.api_key,
    )

    agent = create_agent(
        llm,
        checkpointer=InMemorySaver(),
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        tools=[search_plan_mock_tool],
    )

    # Test with a plan query
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What plans do you have?"}]},
        {"configurable": {"thread_id": "test-1"}},
    )

    # Print the final response
    for msg in response["messages"]:
        if hasattr(msg, "content") and msg.content:
            safe = msg.content.encode("ascii", errors="replace").decode("ascii")
            print(f"[{msg.__class__.__name__}]: {safe}")


if __name__ == "__main__":
    test_agent()
