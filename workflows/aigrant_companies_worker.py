from pydantic import BaseModel, Field

# Define Pydantic models for structured data extraction
class Company(BaseModel):
    name: str = Field(..., description="Company name")
    description: str = Field(..., description="Brief company description")

class Companies(BaseModel):
    companies: list[Company] = Field(..., description="List of companies")

async def aigrant_companies_runner(stagehand):
    try:

        await stagehand.init()
        page = stagehand.page

        await page.goto("https://www.aigrant.com")
        companies_data = await page.extract(
          "Extract names and descriptions of companies",
          schema=Companies
        )

        return companies_data

    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        await stagehand.close()
