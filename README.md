# E-Commerce Intelligence Hub

A production-grade business intelligence platform for e-commerce — powered by **Google BigQuery**, **GPT-4o**, and a live **React dashboard**.

---

## Quick Start (No API Keys Required)

```bash
git clone https://github.com/AbdullahYounas0/Business-Intelligence-for-Ecommerce.git
cd Business-Intelligence-for-Ecommerce
python -m venv venv
venv\Scripts\activate    # Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Open http://localhost:8000 — the dashboard loads immediately with realistic mock data.

Seed or refresh mock data at any time:
```bash
curl -X POST http://localhost:8000/demo
```

---

## Three Intelligence Modules

| Module | Schedule | Output |
|---|---|---|
| Churn & Retention | Daily | GPT-4o win-back emails + Slack `#retention` |
| Order & Inventory | Every 15 min | Live dashboard alerts + Slack `#inventory-ops` |
| Review Sentiment | Daily + weekly | Sentiment charts + Monday email digest |

---

## Author

**Abdullah Younas** — f191010@nu.edu.pk — [GitHub](https://github.com/AbdullahYounas0)
