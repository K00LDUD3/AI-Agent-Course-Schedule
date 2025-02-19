from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
import asyncio
import re
from dotenv import load_dotenv
import os 

# Getting API Keys
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Create a Gemini-powered agent
model = GeminiModel('gemini-1.5-flash', api_key=API_KEY)
roulette_agent = Agent(  
    model,  # Use Gemini instead of OpenAI
    deps_type=int,
    result_type=bool,
    system_prompt=(
    #     # "Extract two numbers from the user query and return their sum and use the 'Add_Numbers' function to add two given numbers"
        "Use the `roulette_wheel` function to see if the "
        "customer has won based on the number they provide."
    ),
)


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
    """check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'


# Run the agent
success_number = 18  
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.data)  
#> True

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.data)
#> False