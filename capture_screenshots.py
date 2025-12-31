
import asyncio
from playwright.async_api import async_playwright
import time

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        print("Navigating to dashboard...")
        await page.goto("http://localhost:8501", wait_until="domcontentloaded", timeout=60000)
        try:
             await page.wait_for_selector("text=Study Roadmap", timeout=20000)
        except:
             print("Could not find Study Roadmap text, capturing anyway.")
        await page.wait_for_timeout(2000) # Wait for animations
        await page.screenshot(path="assets/img/dashboard_screenshot.png", full_page=False)
        print("Captured dashboard.")

        # Writing Clinic
        print("Navigating to Writing Clinic...")
        # Since it's a streamlit app with option_menu, we might need to click the navigation
        # Finding the element might be tricky if IDs involve random hashes. 
        # But `streamlit-option-menu` usually renders as list items.
        # Let's try to click by text.
        await page.get_by_text("Writing Clinic").click()
        await page.wait_for_selector("text=TEF Writing Clinic", timeout=5000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path="assets/img/writing_clinic_screenshot.png", full_page=False)
        print("Captured writing clinic.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
