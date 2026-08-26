"""Test basic LLM call - Milestone 1.8: First LLM response."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from telecomcall.config import settings


def test_llm():
    """Make a basic LLM call and print the response."""
    llm = ChatGroq(
        model=settings.groq.model,
        api_key=settings.groq.api_key,
    )

    response = llm.invoke([
        HumanMessage(content="Say exactly: 'Hello, I am TelecomCall. How can I help you today?'")
    ])

    print(f"Agent response: {response.content}")


if __name__ == "__main__":
    test_llm()
