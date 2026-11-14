from typing import List, Optional
from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    tagline: Optional[str] = None
    price: int
    original_price: Optional[int] = None
    category: Optional[str] = None
    badge: Optional[str] = None
    image_url: Optional[str] = None
    description: str
    features: List[str] = []
    is_active: bool = True

# -----------------------------------------------------------------------------
# Product Catalogue (Backend as Single Source of Truth)
# -----------------------------------------------------------------------------
ALLOWED_PRODUCTS = [
    {
        "id": "desk-mat",
        "name": "Pure Black Desk Mat (XXL)",
        "tagline": "Spacious water-resistant surface with anti-fray stitching",
        "price": 799,
        "original_price": 999,
        "category": "Surface",
        "badge": "Early Bird",
        "image_url": "https://images.unsplash.com/photo-1616440347437-b1c73416efc2?auto=format&fit=crop&w=800&q=80",
        "description": "Engineered for precision tracking and desk protection. Premium micro-textured cloth with high-density stitched borders and non-slip rubber backing.",
        "features": ["900mm x 400mm x 4mm", "Water-resistant coating", "Non-slip rubber base"]
    },
    {
        "id": "headphone-stand",
        "name": "Solid Aluminum Headphone Stand",
        "tagline": "Minimalist weighted cradle for premium audio gear",
        "price": 599,
        "original_price": 799,
        "category": "Organizer",
        "badge": "Popular",
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80",
        "description": "Keep your desk clutter-free while protecting your headband. CNC-milled aluminum with curved silicone rest and anti-slip silicone feet.",
        "features": ["Weighted steel base", "Curved protective silicone", "Matte anodized black finish"]
    },
    {
        "id": "cable-kit",
        "name": "Zen Magnetic Cable Management Pack",
        "tagline": "Magnetic clips & routing channels to tame loose wires",
        "price": 399,
        "original_price": 599,
        "category": "Cables",
        "badge": "Essential",
        "image_url": "https://images.unsplash.com/photo-1588508065123-287b28e013da?auto=format&fit=crop&w=800&q=80",
        "description": "Eliminate charging cable drop-offs and messy desktop wires. Magnetic snap collars attach to desk edge mount strips for single-handed docking.",
        "features": ["5x Magnetic clips", "3x Under-desk channels", "Damage-free 3M adhesive"]
    },
    {
        "id": "keyboard",
        "name": "Custom 75% Mechanical Keyboard",
        "tagline": "Hot-swappable linear switches with acoustic dampening",
        "price": 2999,
        "original_price": 3999,
        "category": "Hardware",
        "badge": "Flagship",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
        "description": "Pre-lubed smooth linear switches, sound-dampening silicone gaskets, and per-key RGB in a compact 75% desk-saving layout.",
        "features": ["Hot-swappable 5-pin sockets", "Gasket-mounted acoustic dampening", "Detachable braided Type-C"]
    }
]

ALLOWED_PRODUCT_IDS = {p["id"] for p in ALLOWED_PRODUCTS}
