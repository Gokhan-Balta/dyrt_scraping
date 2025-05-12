import httpx
import asyncio

async def fetch_campgrounds():
    url = "https://thedyrt.com/api/v6/locations/search-results"
    params = {
        "filter[search][bbox]": "-125.0,24.396308,-66.93457,49.384358",  
        "sort": "recommended",
        "page[number]": 1,
        "page[size]": 500
    }

    async with httpx.AsyncClient(timeout=60.0) as client:  
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Toplam Kamp Alanı: {len(data['data'])}")
            return data['data']
        else:
            print(f"Hata oluştu: {response.status_code}")
            return []

# To pull data
asyncio.run(fetch_campgrounds())
