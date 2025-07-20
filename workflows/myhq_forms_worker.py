async def myhq_forms_runner(stagehand):
    try:
        await stagehand.init()
        page = stagehand.page

        await page.goto("https://myhq.in/virtual-office/awfis-ambli")

        observations = await page.observe("Find the button on this page")

        return observations

    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        await stagehand.close()
