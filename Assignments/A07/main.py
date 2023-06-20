import get_url
from pyppeteer import launch
import asyncio
from rich import print

#url = get_url.generate_url()
url = "https://www.wunderground.com/history/monthly/EGPD/date/2020-6-15"

async def scrape(url):
    browser = await launch()
    print("Launching Browswer...")
    page = await browser.newPage()
    print(f'Going to {url}')
    await page.goto(url)

    data = await page.content()
    await browser.close()

    return data
    
response = asyncio.get_event_loop().run_until_complete(scrape(url))

with open('./example.html', 'w', encoding='utf-8') as f:
    f.write(response)


