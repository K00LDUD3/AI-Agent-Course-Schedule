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
        "Extract two numbers given in a user query. "
        "Use the 'Print_ExtractedNumbers' function to display the extracted numbers. "
        "Extract the numbers in the form of a list. "
        "For example, if the extracted numbers are 2 and 5, pass them into 'Print_ExtractedNumbers' as a list: [2,5]"
    )

system_prompt_v2 = (
    "Extract two numbers given in a user query. Do not perform the action requested. Do not do anything apart from what is told. Do not say anything extra. Do what is told once. " #Why tf does this cause an infinite loop????????
    "Use the 'Print_ExtractedNumbers' function to display the extracted numbers. "
    "Pass the extracted numbers as a list of integers to the function. "
    "For example, if the extracted numbers are 2 and 5, call Print_ExtractedNumbers([2, 5])"
)

# Create a Gemini-powered agent
model = GeminiModel('gemini-1.5-flash', api_key=API_KEY)
agent = Agent(  
    model,
    deps_type=list[int], 
    # result_type=None, #Uncommenting this gives an error yet to be resolved
    system_prompt=system_prompt_v2,
)


@agent.tool
async def Print_ExtractedNumbers(ctx: RunContext[list[int]], numbers: list[int]) -> None:  
    """print the extracted numbers"""
    print(f"Debug: {numbers=}")
    return None



# Run the agent
try:
    result = agent.run_sync("Add the numbers 1115 and 13")
    print(result.data)
except Exception as e:
    print(f"An error occurred: {e}")
    # print(f"Result object: {result}")  # This will print the entire result object for debugging
#> Test Case 1

# result = agent.run_sync('I bet five is the winner')
# print(result.data)
#> Test Case 2