"""
Realistic FlowerZone.ae e-commerce data.
Used when GOOGLE_CLOUD_PROJECT is not set, or as seed data via POST /demo.
"""
import random
import uuid
from datetime import datetime, timedelta, timezone

_NOW = datetime.now(timezone.utc)
random.seed(42)

def _ts(dt: datetime) -> str:
    """Format timestamp as BigQuery-compatible UTC string."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Catalogue ─────────────────────────────────────────────────────────────────

PRODUCTS = [
    {"product_id": "FZ-001", "title": "Red Rose Bouquet (12 stems)",     "sku": "RRB-012", "category": "Bouquets",    "price": 89.00,  "reorder_threshold": 15},
    {"product_id": "FZ-002", "title": "White Lily Arrangement",           "sku": "WLA-001", "category": "Arrangements","price": 120.00, "reorder_threshold": 10},
    {"product_id": "FZ-003", "title": "Pink Tulip Bundle (20 stems)",     "sku": "PTB-020", "category": "Bouquets",    "price": 75.00,  "reorder_threshold": 20},
    {"product_id": "FZ-004", "title": "Orchid Plant – Purple",            "sku": "ORP-001", "category": "Plants",      "price": 145.00, "reorder_threshold": 8},
    {"product_id": "FZ-005", "title": "Sunflower Cheerful Mix",           "sku": "SCM-001", "category": "Bouquets",    "price": 65.00,  "reorder_threshold": 25},
    {"product_id": "FZ-006", "title": "Luxury Rose Box (24 stems)",       "sku": "LRB-024", "category": "Gift Boxes",  "price": 220.00, "reorder_threshold": 10},
    {"product_id": "FZ-007", "title": "Mixed Wildflower Bouquet",         "sku": "MWB-001", "category": "Bouquets",    "price": 55.00,  "reorder_threshold": 20},
    {"product_id": "FZ-008", "title": "Peony & Rose Blush Arrangement",  "sku": "PRB-001", "category": "Arrangements","price": 195.00, "reorder_threshold": 8},
    {"product_id": "FZ-009", "title": "Succulent Garden Box",             "sku": "SGB-001", "category": "Plants",      "price": 110.00, "reorder_threshold": 12},
    {"product_id": "FZ-010", "title": "Lavender Tied Bouquet",            "sku": "LTB-001", "category": "Bouquets",    "price": 70.00,  "reorder_threshold": 15},
    {"product_id": "FZ-011", "title": "Red & White Valentine Box",        "sku": "RWV-001", "category": "Gift Boxes",  "price": 260.00, "reorder_threshold": 20},
    {"product_id": "FZ-012", "title": "Hydrangea Blue Vase",              "sku": "HBV-001", "category": "Arrangements","price": 135.00, "reorder_threshold": 10},
    {"product_id": "FZ-013", "title": "Yellow Daffodil Spring Bundle",    "sku": "YDS-001", "category": "Bouquets",    "price": 60.00,  "reorder_threshold": 18},
    {"product_id": "FZ-014", "title": "Cactus Trio Pot",                  "sku": "CTP-001", "category": "Plants",      "price": 85.00,  "reorder_threshold": 10},
    {"product_id": "FZ-015", "title": "White Roses Premium Box (50)",     "sku": "WRP-050", "category": "Gift Boxes",  "price": 420.00, "reorder_threshold": 5},
    {"product_id": "FZ-016", "title": "Gerbera Daisy Bright Mix",         "sku": "GDB-001", "category": "Bouquets",    "price": 58.00,  "reorder_threshold": 20},
    {"product_id": "FZ-017", "title": "Bonsai Tree – Ficus",              "sku": "BTF-001", "category": "Plants",      "price": 320.00, "reorder_threshold": 5},
    {"product_id": "FZ-018", "title": "Mother's Day Pastel Bouquet",      "sku": "MDP-001", "category": "Bouquets",    "price": 95.00,  "reorder_threshold": 30},
    {"product_id": "FZ-019", "title": "Eucalyptus & Rose Wreath",         "sku": "ERW-001", "category": "Arrangements","price": 150.00, "reorder_threshold": 8},
    {"product_id": "FZ-020", "title": "Birthday Balloon & Flower Box",    "sku": "BBF-001", "category": "Gift Boxes",  "price": 175.00, "reorder_threshold": 12},
    {"product_id": "FZ-021", "title": "Carnation Rainbow Bouquet",        "sku": "CRB-001", "category": "Bouquets",    "price": 50.00,  "reorder_threshold": 25},
    {"product_id": "FZ-022", "title": "Peace Lily Indoor Plant",          "sku": "PLI-001", "category": "Plants",      "price": 90.00,  "reorder_threshold": 10},
    {"product_id": "FZ-023", "title": "Rose & Chocolate Hamper",          "sku": "RCH-001", "category": "Gift Boxes",  "price": 310.00, "reorder_threshold": 8},
    {"product_id": "FZ-024", "title": "Dried Flower Pampas Arrangement",  "sku": "DFP-001", "category": "Arrangements","price": 130.00, "reorder_threshold": 10},
    {"product_id": "FZ-025", "title": "Magnolia White Luxury Bouquet",    "sku": "MWL-001", "category": "Bouquets",    "price": 180.00, "reorder_threshold": 8},
]

CUSTOMERS = [
    ("CUST-001", "Aisha Al Mansoori",    "aisha.mansoori@gmail.com"),
    ("CUST-002", "Mohammed Al Rashidi",  "m.rashidi@outlook.com"),
    ("CUST-003", "Fatima Hassan",        "fatima.hassan@gmail.com"),
    ("CUST-004", "Omar Abdullah",        "omar.abdullah@yahoo.com"),
    ("CUST-005", "Layla Al Zaabi",       "layla.zaabi@gmail.com"),
    ("CUST-006", "Khalid Al Nuaimi",     "khalid.nuaimi@hotmail.com"),
    ("CUST-007", "Sara Al Mazrouei",     "sara.mazrouei@gmail.com"),
    ("CUST-008", "Ahmed Al Shamsi",      "ahmed.shamsi@gmail.com"),
    ("CUST-009", "Noor Al Qasimi",       "noor.qasimi@outlook.com"),
    ("CUST-010", "Hamad Al Marri",       "hamad.marri@gmail.com"),
    ("CUST-011", "Reem Al Ketbi",        "reem.ketbi@gmail.com"),
    ("CUST-012", "Yusuf Al Suwaidi",     "yusuf.suwaidi@yahoo.com"),
    ("CUST-013", "Maryam Al Blooshi",    "maryam.blooshi@gmail.com"),
    ("CUST-014", "Saif Al Darmaki",      "saif.darmaki@hotmail.com"),
    ("CUST-015", "Hessa Al Muhairi",     "hessa.muhairi@gmail.com"),
    ("CUST-016", "Rashid Al Falasi",     "rashid.falasi@gmail.com"),
    ("CUST-017", "Maitha Al Junaibi",    "maitha.junaibi@outlook.com"),
    ("CUST-018", "Obaid Al Kaabi",       "obaid.kaabi@gmail.com"),
    ("CUST-019", "Latifa Al Qubaisi",    "latifa.qubaisi@gmail.com"),
    ("CUST-020", "Faisal Al Hammadi",    "faisal.hammadi@yahoo.com"),
    ("CUST-021", "Ayesha Al Marzouqi",   "ayesha.marzouqi@gmail.com"),
    ("CUST-022", "Tariq Al Shamsi",      "tariq.shamsi@gmail.com"),
    ("CUST-023", "Badria Al Neyadi",     "badria.neyadi@hotmail.com"),
    ("CUST-024", "Mansoor Al Owais",     "mansoor.owais@gmail.com"),
    ("CUST-025", "Amna Al Hajeri",       "amna.hajeri@outlook.com"),
    ("CUST-026", "Shaheen Al Khoori",    "shaheen.khoori@gmail.com"),
    ("CUST-027", "Dalal Al Romaithi",    "dalal.romaithi@gmail.com"),
    ("CUST-028", "Jassim Al Mazrouei",   "jassim.mazrouei@yahoo.com"),
    ("CUST-029", "Noura Al Kuwaiti",     "noura.kuwaiti@gmail.com"),
    ("CUST-030", "Abdulla Al Ghurair",   "abdulla.ghurair@gmail.com"),
    ("CUST-031", "Hind Al Maktoum",      "hind.maktoum@gmail.com"),
    ("CUST-032", "Waleed Al Serkal",     "waleed.serkal@outlook.com"),
    ("CUST-033", "Shaikha Al Habtoor",   "shaikha.habtoor@gmail.com"),
    ("CUST-034", "Khalifa Al Tayer",     "khalifa.tayer@hotmail.com"),
    ("CUST-035", "Lubna Al Olama",       "lubna.olama@gmail.com"),
    ("CUST-036", "Mariam Al Mehairi",    "mariam.mehairi@gmail.com"),
    ("CUST-037", "Sultan Al Nasseri",    "sultan.nasseri@yahoo.com"),
    ("CUST-038", "Wafa Al Hashimi",      "wafa.hashimi@gmail.com"),
    ("CUST-039", "Eisa Al Mazroui",      "eisa.mazroui@gmail.com"),
    ("CUST-040", "Najla Al Muaini",      "najla.muaini@outlook.com"),
    ("CUST-041", "Sarah Mitchell",       "sarah.mitchell@gmail.com"),
    ("CUST-042", "James Rodriguez",      "james.rodriguez@yahoo.com"),
    ("CUST-043", "Emma Thompson",        "emma.thompson@gmail.com"),
    ("CUST-044", "David Chen",           "david.chen@outlook.com"),
    ("CUST-045", "Priya Sharma",         "priya.sharma@gmail.com"),
    ("CUST-046", "Lucas Oliveira",       "lucas.oliveira@hotmail.com"),
    ("CUST-047", "Sofia Al Amine",       "sofia.alamine@gmail.com"),
    ("CUST-048", "Karim Benali",         "karim.benali@gmail.com"),
    ("CUST-049", "Yasmine Nakamura",     "yasmine.nakamura@yahoo.com"),
    ("CUST-050", "Nicolas Fontaine",     "nicolas.fontaine@gmail.com"),
]

REVIEW_BODIES = {
    5: [
        "Absolutely stunning arrangement! The roses were so fresh and beautifully packaged. Delivered on time for our anniversary.",
        "FlowerZone never disappoints. These orchids are thriving two weeks later. Will definitely order again.",
        "Ordered for my mother's birthday and she was in tears — in the best way! Perfect flowers, perfect delivery.",
        "The luxury rose box was breathtaking. Every stem was perfect. My wife loved it.",
        "Excellent quality and very fast delivery to Dubai. The packaging kept everything pristine.",
        "Third time ordering and still impressed. The mixed bouquet was vibrant and fragrant.",
        "Best flower shop in the UAE. Same-day delivery worked perfectly for our surprise.",
    ],
    4: [
        "Very beautiful flowers, arrived fresh. Packaging was excellent. One stem was slightly bruised but overall great.",
        "Great quality for the price. Delivery was slightly delayed but the flowers were worth waiting for.",
        "Really lovely arrangement. The colours were exactly as shown. Would have been 5 stars with better communication.",
        "Good flowers and decent packaging. Delivery driver was professional. Will order again.",
        "Nice bouquet, my girlfriend loved it. Petals were fresh but the vase was a bit small.",
    ],
    3: [
        "Flowers were okay. Not as full as the website photo suggested. Delivery was on time though.",
        "Average quality for a premium price. Expected better from a high-end florist.",
        "Decent flowers but the arrangement was less impressive in person. The lavender wilted within 2 days.",
        "Okay experience overall. The box was damaged on arrival but the flowers inside were fine.",
    ],
    2: [
        "Disappointed with the delivery time. Ordered for a birthday and it arrived 3 hours late. Flowers were fresh but the experience ruined the surprise.",
        "Half the roses were already wilting when they arrived. For this price I expected better quality control.",
        "The arrangement didn't match what I ordered. Customer service was slow to respond.",
    ],
    1: [
        "Flowers arrived completely wilted and brown. This was supposed to be a gift for a funeral — absolutely unacceptable. Requesting a refund.",
        "Never arrived! Ordered 2 days ago and still waiting. No response from customer service. This is fraud.",
        "Broken stems, dead flowers, wrong product. Total waste of money. Never ordering again.",
    ],
}


def _days_ago(n: int) -> str:
    return _ts(_NOW - timedelta(days=n))


def mock_products() -> list[dict]:
    products = []
    for p in PRODUCTS:
        units = random.randint(0, 60)
        pending = random.randint(0, 18) if units < p["reorder_threshold"] + 5 else random.randint(0, 5)
        products.append({
            **p,
            "units_available": units,
            "pending_orders": pending,
            "updated_at": _days_ago(random.randint(0, 2)),
        })
    return products


def mock_orders() -> list[dict]:
    orders = []
    product_map = {p["product_id"]: p for p in PRODUCTS}

    for cust_id, name, email in CUSTOMERS:
        n_orders = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[15, 20, 20, 18, 12, 8, 5, 2])[0]

        is_at_risk = random.random() < 0.30
        if is_at_risk:
            last_order_days_ago = random.randint(65, 180)
        else:
            last_order_days_ago = random.randint(1, 60)

        order_dates = sorted(
            [last_order_days_ago + random.randint(0, 20) * i for i in range(n_orders)],
            reverse=True,
        )

        for i, days_ago in enumerate(order_dates):
            prod = random.choice(PRODUCTS)
            is_recent_unfulfilled = days_ago > 1 and random.random() < 0.12
            status = "unfulfilled" if is_recent_unfulfilled else "fulfilled"
            orders.append({
                "order_id":       f"ORD-{cust_id[5:]}-{i:02d}",
                "customer_id":    cust_id,
                "customer_name":  name,
                "customer_email": email,
                "product_id":     prod["product_id"],
                "product_title":  prod["title"],
                "total_price":    round(prod["price"] * random.uniform(0.9, 1.1), 2),
                "status":         status,
                "created_at":     _days_ago(days_ago),
            })
    return orders


def mock_reviews() -> list[dict]:
    reviews = []
    product_ids = [p["product_id"] for p in PRODUCTS]
    customer_names = [c[1] for c in CUSTOMERS]

    rating_weights = {5: 45, 4: 30, 3: 12, 2: 8, 1: 5}
    ratings = list(rating_weights.keys())
    weights = list(rating_weights.values())

    for i in range(200):
        rating = random.choices(ratings, weights=weights)[0]
        body   = random.choice(REVIEW_BODIES[rating])
        reviews.append({
            "review_id":     f"REV-{i+1:04d}",
            "product_id":    random.choice(product_ids),
            "customer_name": random.choice(customer_names),
            "rating":        rating,
            "body":          body,
            "created_at":    _days_ago(random.randint(0, 60)),
        })
    return reviews


def mock_at_risk_customers() -> list[dict]:
    orders = mock_orders()
    from src.modules.churn.scorer import compute_rfm
    threshold = int(__import__('os').environ.get("CHURN_RFM_THRESHOLD", "30"))
    all_scores = compute_rfm(orders)
    at_risk = [c for c in all_scores if c["rfm_score"] < threshold]
    return sorted(at_risk, key=lambda x: x["rfm_score"])[:15]
