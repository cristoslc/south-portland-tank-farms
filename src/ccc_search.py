#!/usr/bin/env python3
"""Drive search.childcarechoices.me via Playwright, search around a lat/lon point."""
import sys, re, json, asyncio

async def search_around(lat, lon, address_label, out_html):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://search.childcarechoices.me/", wait_until="networkidle", timeout=60000)
        # fill address text
        await page.fill("#MainContent_txtAddress", address_label)
        # inject lat/lon into hidden fields (bypass geocode JS)
        await page.evaluate(
            "([lat, lon]) => {"
            "document.getElementById('MainContent_hdnAddressLat').value = String(lat);"
            "document.getElementById('MainContent_hdnAddressLon').value = String(lon);"
            "}",
            [lat, lon])
        # check all provider types
        for i in range(4):
            cb = page.locator(f"#MainContent_cblProviderType_{i}")
            if await cb.count() and not await cb.is_checked():
                await cb.check()
        await page.click("#MainContent_Button1")
        await page.wait_for_load_state("networkidle", timeout=60000)
        html = await page.content()
        open(out_html, "w").write(html)
        print(f"saved {out_html}, len={len(html)}")
        await browser.close()

if __name__ == "__main__":
    lat, lon = float(sys.argv[1]), float(sys.argv[2])
    label = sys.argv[3]
    out = sys.argv[4]
    asyncio.run(search_around(lat, lon, label, out))