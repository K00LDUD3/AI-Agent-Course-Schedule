from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
import asyncio
import re
from dotenv import load_dotenv
import os 

# Getting API Keys
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

system_prompt_v1=(
        "Extract two numbers from the user query. "
        "Use the 'Add_Numbers' function to add these numbers by passing them as a list. "
        "For example, if the query is 'Add the numbers 5 and 13', you should call the  'Add_Numbers' function while passing [5, 13]. "
        "Return the result as an integer."
    )
system_prompt_v2= """
You are an AI assistant that adds two numbers. Your task is to:
1. Extract two numbers from the user's query.
2. Call the 'Add_Numbers' function with these numbers as a list.
3. Return the result.

Example:
User query: "Add the numbers 5 and 13"
You should extract [5, 13] and call Add_Numbers([5, 13]).

Always use the Add_Numbers function to perform the addition.
"""

system_prompt_v3 = """
You are an AI assistant that adds two numbers. Your task is to:
1. Extract two numbers from the user's query.
2. Call the 'Add_Numbers' function with these numbers as a list.
3. Return the result.

Example:
User query: "Add the numbers 5 and 13"
You should extract [5, 13] and call Add_Numbers with args: {"numbers": [5, 13]}.

Always use the Add_Numbers function to perform the addition.
"""

# Create a Gemini-powered agent
model = GeminiModel('gemini-1.5-flash', api_key=API_KEY)
agent = Agent(  
    model,
    # deps_type=list[int],
    result_type=int,
    system_prompt=system_prompt_v1,
)


@agent.tool
async def Add_Numbers(ctx: RunContext[str]) -> int:  
    """return the addition of given numbers from the context"""
    # print(f"Debug: ctx = {ctx}")
    print(f"Debug: ctx.deps = {ctx.deps}")

    if ctx.deps is None:
        raise ValueError("No numbers provided for addition (ctx.deps is None)")
    if len(ctx.deps) == 0:
        raise ValueError("No numbers provided for addition (empty list)")
    return sum(ctx.deps)


# Add this after the try-except block
# print("\nTesting Add_Numbers function directly:")
# try:
#     ctx = RunContext(deps=[5, 13])
#     result = asyncio.run(Add_Numbers(ctx))
#     print(f"Direct function call result: {result}")
# except Exception as e:
#     print(f"Error in direct function call: {e}")


# Run the agent
try:
    result = agent.run_sync("Add the numbers 5 and 13")
    print(result.data)
except Exception as e:
    print(f"An error occurred: {e}")
    # print(f"Result object: {result}")  # This will print the entire result object for debugging
#> Test Case 1

# result = agent.run_sync('I bet five is the winner')
# print(result.data)
#> Test Case 2