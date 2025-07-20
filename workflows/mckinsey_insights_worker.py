from pydantic import BaseModel, Field

class Insight(BaseModel):
    title: str = Field(..., description="Heading of the insight article")
    summary: str = Field(..., description="summary of the insight article")

class Insights(BaseModel):
    insights: list[Insight] = Field(..., description="list of insights")

async def mckinsey_insights_runner(stagehand):
    try:

        await stagehand.init()
        page = stagehand.page

        await page.goto("https://www.mckinsey.com/featured-insights")
        await page.act("click on 'accept all cookies'")
        data = await page.extract(
          "Extract title, summarize the insight on mckinsey page",
          schema=Insights
        )

        return data

    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        await stagehand.close()
