import httpx
from pprint import pprint
from src.models.campground import Campground
from pydantic import ValidationError
from src.models.db_model import campground_to_db
from src.db.session import AsyncSessionLocal, save_campgrounds_to_db

async def fetch_campgrounds(page=1):
    url = "https://thedyrt.com/api/v6/locations/search-results"
    params = {
        "filter[search][bbox]": "-125.0,24.396308,-66.93457,49.384358",
        "sort": "recommended",
        "page[number]": page,
        "page[size]": 500
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://thedyrt.com/search",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        raw_data = json_data.get("data", [])

        valid = []
        for item in raw_data:
            try:
                camp = Campground(
                    **item["attributes"],         
                    id=item["id"],                
                    type=item["type"],            
                    links=item["links"]           
                )
                valid.append(camp)
            except ValidationError as e:
                print(f"Validation error: {e}")

        print(f"\n Page {page} — Total: {len(raw_data)} | Valid: {len(valid)}")
        pprint([c.name for c in valid[:3]])  
        return valid


async def fetch_and_save(page=1):
    camps = await fetch_campgrounds(page)
    db_objs = [campground_to_db(c) for c in camps]

    async with AsyncSessionLocal() as session:
        await save_campgrounds_to_db(db_objs, session)


