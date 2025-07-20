import asyncio
import os
from dotenv import load_dotenv
from stagehand import StagehandConfig, Stagehand
from agno.agent import Agent
from agno.models.google import Gemini
from workflows.myhq_forms_worker import myhq_forms_runner
from workflows.aigrant_companies_worker import aigrant_companies_runner
from workflows.mckinsey_insights_worker import mckinsey_insights_runner

load_dotenv()

async def run_myhq_forms() -> str:
    config = StagehandConfig(
        verbose=1,
        env = "LOCAL",
        model_name="google/gemini-2.5-flash",
        model_api_key=os.getenv("GOOGLE_API_KEY"),
        **{},
    )
    stagehand = Stagehand(config)
    try:
        await stagehand.init()
        return await myhq_forms_runner(stagehand)
    finally:
        await stagehand.close()

async def run_mckinsey_insights() -> str:
    config = StagehandConfig(
        verbose=1,
        env = "LOCAL",
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("GOOGLE_API_KEY"),
        **{},
    )
    stagehand = Stagehand(config)
    try:
        await stagehand.init()
        return await mckinsey_insights_runner(stagehand)
    finally:
        await stagehand.close()

async def run_aigrant_companies() -> str:
    config = StagehandConfig(
        verbose=1,
        env = "LOCAL",
        model_name="google/gemini-2.5-flash-preview-05-20",
        model_api_key=os.getenv("GOOGLE_API_KEY"),
        **{},
    )
    stagehand = Stagehand(config)
    try:
        await stagehand.init()
        return await aigrant_companies_runner(stagehand)
    finally:
        await stagehand.close()


agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key = os.getenv("GOOGLE_API_KEY")),
    tools=[
        run_myhq_forms,
        run_aigrant_companies,
        run_mckinsey_insights,
    ],
    show_tool_calls=True,
    markdown=True,
)

async def main():
    await agent.aprint_response(
            "can you tell me about insights on mckinsey match them with companies in ai grant",
            stream=True,
        )

if __name__ == "__main__":
    asyncio.run(main())
