from langchain.tools import tool


@tool
def search_plan_mock_tool(location: str) -> str:
    """Retrieve mobile plan details for plans in a given category or area."""
    return (
        "I found three plans for you. The Starter plan costs 29 dollars per month "
        "with 20GB data. The Plus plan costs 49 dollars per month with 60GB data. "
        "The Unlimited plan costs 79 dollars per month with unlimited data."
    )
