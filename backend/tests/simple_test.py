import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.api.products import get_products

async def main():
    print("Fetching products...")
    prods = await get_products()
    print("Products fetched successfully:", len(prods))

asyncio.run(main())
