import asyncio
from patchright.async_api import async_playwright, BrowserContext, Page



# https://drive.google.com/file/d/15zKMwbE6jEAi20-yjpzB_GqIK3C9JsDc/view?usp=sharing
# Drive Video Link


Correct = 0

for i in range(10):
    try:
        async def main():
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(
                    channel="chrome",
                    headless=False,
                    args=["--disable-blink-features=AutomationControlled"]
                )

                context: BrowserContext = await browser.new_context()
                page: Page = await context.new_page()

                await page.goto("https://cd.captchaaiplus.com/turnstile.html")

                token_element = await page.wait_for_function("""
                    () => {
                        const input = document.querySelector('input[name="cf-turnstile-response"]');
                        return input?.value?.length > 100 ? input.value : null;
                    }
                """, timeout=30000)

                token_value = await token_element.json_value()
                print(f"The Token for trial num [{i+1}]: {token_value}")
                print("_"*50)

                submit_button = await page.query_selector('#turnstile-form input[type="submit"]')
                if not submit_button:
                    submit_button = await page.query_selector('input[type="submit"]')

                if submit_button:
                    await submit_button.click()

                await asyncio.sleep(2)  

                await browser.close()   

        asyncio.run(main())
        Correct += 1

    except Exception as e:
        print("Error:", e)

print("_"*50)
print(f"The Accuracy is: {Correct/10:.2%}")